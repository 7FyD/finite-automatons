import sys
from read_file import *
from collections import deque

EPSILON = ""


class PDA:
    def __init__(self, states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, final_states):
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.stack_alphabet = set(stack_alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.final_states = set(final_states)

        # --- Validation ---
        if self.start_state not in self.states:
            raise ValueError(
                f"Start state '{self.start_state}' not in states {self.states}")
        if self.start_stack_symbol not in self.stack_alphabet:
            raise ValueError(
                f"Start stack symbol '{self.start_stack_symbol}' not in stack alphabet {self.stack_alphabet}")
        if not self.final_states.issubset(self.states):
            raise ValueError(
                f"Final states {self.final_states - self.states} not in states {self.states}")

    def _get_epsilon_closure(self, config_set):
        """
        Computes the epsilon closure for a set of configurations (state, stack).
        A configuration is reachable by epsilon if we can move from a current
        state to another using only epsilon transitions without consuming input.
        """
        closure = set(config_set)
        queue = deque([(s, list(st)) for s, st in config_set])
        processed = set(config_set)

        while queue:
            current_state, current_stack_list = queue.popleft()
            current_stack_top = current_stack_list[-1] if current_stack_list else None

            transition_key = (current_state, EPSILON, current_stack_top)
            if transition_key in self.transitions:
                for next_state, push_symbols_str in self.transitions[transition_key]:
                    new_stack_list = current_stack_list[:-1]  # Pop
                    new_stack_list.extend(list(push_symbols_str[::-1]))

                    new_config = (next_state, tuple(new_stack_list))

                    if new_config not in processed:
                        processed.add(new_config)
                        closure.add(new_config)
                        queue.append((next_state, new_stack_list))
        return closure

    def simulate(self, input_string):
        initial_stack = [self.start_stack_symbol]
        current_configs = set()
        current_configs.add((self.start_state, tuple(initial_stack)))

        current_configs = self._get_epsilon_closure(current_configs)

        for symbol in input_string:
            if symbol not in self.input_alphabet:
                print(
                    f"Warning: Symbol '{symbol}' not in input alphabet. String will be rejected.", file=sys.stderr)
                return False

            next_configs = set()
            for state, stack_tuple in current_configs:
                stack_list = list(stack_tuple)
                stack_top = stack_list[-1] if stack_list else None

                transition_key = (state, symbol, stack_top)
                if transition_key in self.transitions:
                    for next_state, push_symbols_str in self.transitions[transition_key]:
                        new_stack_list = stack_list[:-1]
                        new_stack_list.extend(
                            list(push_symbols_str[::-1]))

                        next_configs.add((next_state, tuple(new_stack_list)))

            if not next_configs:
                return False
            current_configs = self._get_epsilon_closure(next_configs)

        for state, stack in current_configs:
            if state in self.final_states:
                return True

        return False


def parse_pda_json(json_path):
    """Parses a JSON file defining a PDA."""
    load_rules(json_path)

    required_sections = {'states', 'input_alphabet', 'stack_alphabet',
                         'transitions', 'start_state', 'start_stack_symbol', 'final_states'}
    actual_sections = set(get_sections(json_path))
    missing = required_sections - actual_sections
    if missing:
        raise ValueError(f"Missing required sections in JSON: {missing}")

    states = get_section_data(json_path, 'states')
    input_alphabet = get_section_data(json_path, 'input_alphabet')
    stack_alphabet = get_section_data(json_path, 'stack_alphabet')
    transitions_data = get_section_data(json_path, 'transitions')
    start_state = get_section_data(json_path, 'start_state')
    start_stack_symbol = get_section_data(json_path, 'start_stack_symbol')
    final_states = get_section_data(json_path, 'final_states')

    if not isinstance(states, list):
        raise ValueError("states must be a list")
    if not isinstance(input_alphabet, list):
        raise ValueError("input_alphabet must be a list")
    if not isinstance(stack_alphabet, list):
        raise ValueError("stack_alphabet must be a list")
    if not isinstance(transitions_data, list):
        raise ValueError("transitions must be a list")
    if not isinstance(start_state, str):
        raise ValueError("start_state must be a string")
    if not isinstance(start_stack_symbol, str):
        raise ValueError("start_stack_symbol must be a string")
    if not isinstance(final_states, list):
        raise ValueError("final_states must be a list")

    transitions = {}
    for t in transitions_data:
        required_keys = {'current_state', 'input',
                         'stack_top', 'next_state', 'push_symbols'}
        if not required_keys.issubset(t.keys()):
            raise ValueError(
                f"Transition missing required keys: {t}. Required: {required_keys}")

        curr = t['current_state']
        inp = t['input']
        stack_top = t['stack_top']
        next_s = t['next_state']
        push = t['push_symbols']

        # basic validation
        if curr not in states:
            raise ValueError(
                f"Transition state '{curr}' not in defined states.")
        if inp != EPSILON and inp not in input_alphabet:
            raise ValueError(
                f"Transition input '{inp}' not in defined input alphabet.")
        if stack_top not in stack_alphabet:
            raise ValueError(
                f"Transition stack_top '{stack_top}' not in defined stack alphabet.")
        if next_s not in states:
            raise ValueError(
                f"Transition next_state '{next_s}' not in defined states.")
        for char in push:
            if char not in stack_alphabet:
                raise ValueError(
                    f"Transition push_symbols '{push}' contains '{char}' not in defined stack alphabet.")
        # end validation

        transition_key = (curr, inp, stack_top)
        transition_result = (next_s, push)

        if transition_key not in transitions:
            transitions[transition_key] = set()
        transitions[transition_key].add(transition_result)

    return PDA(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, final_states)


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 3:
            rules_file = sys.argv[1]
            input_string = sys.argv[2]
        else:
            rules_file = input("Input your rule filename: ")
            input_string = input("Input your input string: ")

        print(f"Loading PDA rules from: {rules_file}")
        pda = parse_pda_json(rules_file)
        print(f"Simulating string: \"{input_string}\"")

        result = pda.simulate(input_string)

        print(
            f"\nThe string \"{input_string}\" parsed through the PDA emulator is: {'Accepted' if result else 'Rejected'}")

    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
