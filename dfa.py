import sys
from read_file import *


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states)

    def simulate(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            key = (current_state, symbol)
            current_state = self.transitions.get(key, None)
            if current_state is None:
                return False
        return current_state in self.final_states


def parse_dfa_json(json_path):
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
        next_state = t['next_state']

        transition_key = (curr, inp)
        if transition_key in transitions:
            raise ValueError(f"Non-deterministic transition: {curr}, {inp}")
        transitions[transition_key] = next_state

    if not isinstance(final_states, list):
        final_states = [final_states]

    return DFA(states, alphabet, transitions, start_state, final_states)


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 3:
            rules = sys.argv[1]
            input_string = sys.argv[2]
        else:
            rules = input("Input your rule filename: ")
            input_string = input("Input your input string: ")
        dfa = parse_dfa_json(rules)
        print(
            f"The string \"{input_string}\" parsed through the DFA emulator returns: {'Accepted' if dfa.simulate(input_string) else 'Rejected'}")

    except Exception as e:
        print(f"Error: {str(e)}")
