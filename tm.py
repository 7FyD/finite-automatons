import sys
from read_file import *


class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state, blank_symbol='_'):
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.tape = {}
        self.head_position = 0
        self.current_state = self.start_state

        if not self.input_alphabet.issubset(self.tape_alphabet):
            raise ValueError(
                "Input alphabet must be a subset of the tape alphabet.")
        if self.blank_symbol not in self.tape_alphabet:
            raise ValueError("Blank symbol must be in the tape alphabet.")

    def _initialize_tape(self, input_string):
        self.tape.clear()
        for i, symbol in enumerate(input_string):
            if symbol not in self.input_alphabet:
                raise ValueError(
                    f"Symbol '{symbol}' from input string is not in the input alphabet.")
            self.tape[i] = symbol
        self.head_position = 0
        self.current_state = self.start_state

    def simulate(self, input_string, step_limit=1000):
        self._initialize_tape(input_string)
        step = 0

        while step < step_limit:
            if self.current_state == self.accept_state:
                return "Accepted"
            if self.current_state == self.reject_state:
                return "Rejected"

            current_symbol = self.tape.get(
                self.head_position, self.blank_symbol)
            transition_key = (self.current_state, current_symbol)

            if transition_key not in self.transitions:
                return "Rejected"

            next_state, write_symbol, move = self.transitions[transition_key]

            self.tape[self.head_position] = write_symbol

            if move.upper() == 'R':
                self.head_position += 1
            elif move.upper() == 'L':
                self.head_position -= 1
            else:
                raise ValueError(f"Invalid move direction: {move}")

            self.current_state = next_state
            step += 1

        return "Undecided (Step limit reached)"


def parse_tm_json(json_path):
    load_rules(json_path)

    required_sections = {'states', 'input_alphabet', 'tape_alphabet',
                         'transitions', 'start_state', 'accept_state', 'reject_state', 'blank_symbol'}
    sections = set(get_sections(json_path))
    missing = required_sections - sections
    if missing:
        raise ValueError(f"Missing required sections in JSON: {missing}")

    states = get_section_data(json_path, 'states')
    input_alphabet = get_section_data(json_path, 'input_alphabet')
    tape_alphabet = get_section_data(json_path, 'tape_alphabet')
    transitions_data = get_section_data(json_path, 'transitions')
    start_state = get_section_data(json_path, 'start_state')
    accept_state = get_section_data(json_path, 'accept_state')
    reject_state = get_section_data(json_path, 'reject_state')
    blank_symbol = get_section_data(json_path, 'blank_symbol')

    transitions = {}
    for t in transitions_data:
        required = ['current_state', 'read', 'next_state', 'write', 'move']
        if any(k not in t for k in required):
            raise ValueError("Transition missing required keys")

        key = (t['current_state'], t['read'])
        if key in transitions:
            raise ValueError(
                f"Non-deterministic transition found for state {t['current_state']} and symbol {t['read']}")

        transitions[key] = (t['next_state'], t['write'], t['move'])

    return TuringMachine(states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state, blank_symbol)


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 3:
            rules_file = sys.argv[1]
            input_string = sys.argv[2]
        else:
            rules_file = input("Input your rule filename: ")
            input_string = input("Input your input string: ")

        tm = parse_tm_json(rules_file)
        result = tm.simulate(input_string)

        print(
            f"The string \"{input_string}\" parsed through the Turing Machine emulator returns: {result}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
