import sys
from read_file import *
from collections import deque

EPSILON = ""


class NFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states)

    def _get_epsilon_closure(self, states_set):
        """
        Computes the epsilon closure for a set of states by finding all states
        reachable via one or more epsilon transitions.
        """
        closure = set(states_set)
        queue = deque(list(states_set))
        processed = set(states_set)

        while queue:
            current_state = queue.popleft()
            epsilon_next_states = self.transitions.get(
                (current_state, EPSILON), set())

            for state in epsilon_next_states:
                if state not in processed:
                    closure.add(state)
                    queue.append(state)
                    processed.add(state)
        return closure

    def simulate(self, input_string):
        """
        Simulates the NFA on the input string.
        Handles non-determinism by tracking a set of possible current states.
        """
        current_states = self._get_epsilon_closure({self.start_state})

        for symbol in input_string:
            next_states_after_symbol = set()
            for state in current_states:
                next_states_after_symbol.update(
                    self.transitions.get((state, symbol), set()))

            if not next_states_after_symbol:
                return False

            current_states = self._get_epsilon_closure(
                next_states_after_symbol)

        return not current_states.isdisjoint(self.final_states)


def parse_nfa_json(json_path):
    load_rules(json_path)

    required_sections = {'states', 'alphabet',
                         'transitions', 'start_state', 'final_states'}
    sections = get_sections(json_path)
    missing = required_sections - set(sections)
    if missing:
        raise ValueError(f"Missing required sections in JSON: {missing}")

    states = get_section_data(json_path, 'states')
    alphabet = get_section_data(json_path, 'alphabet')
    transitions_data = get_section_data(json_path, 'transitions')
    start_state = get_section_data(json_path, 'start_state')
    final_states = get_section_data(json_path, 'final_states')

    transitions = {}
    for t in transitions_data:
        required = ['current_state', 'input', 'next_state']
        if any(k not in t for k in required):
            raise ValueError("Transition missing required keys")

        curr = t['current_state']
        inp = t['input']
        next_s = t['next_state']

        next_states_list = next_s if isinstance(next_s, list) else [next_s]

        transition_key = (curr, inp)
        if transition_key not in transitions:
            transitions[transition_key] = set()
        transitions[transition_key].update(next_states_list)

    if not isinstance(final_states, list):
        final_states = [final_states]

    return NFA(states, alphabet, transitions, start_state, final_states)


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 3:
            rules_file = sys.argv[1]
            input_string = sys.argv[2]
        else:
            rules_file = input("Input your rule filename: ")
            input_string = input("Input your input string: ")
        nfa = parse_nfa_json(rules_file)
        result = nfa.simulate(input_string)
        print(
            f"The string \"{input_string}\" parsed through the NFA emulator returns: {'Accepted' if result else 'Rejected'}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
