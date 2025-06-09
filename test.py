import sys
from dfa import parse_dfa_json
from nfa import parse_nfa_json
from pda import parse_pda_json
from tm import parse_tm_json


def run_tests():
    # --- DFA Tests ---
    print("--- Testing DFA ---")
    try:
        dfa = parse_dfa_json('dfa_rules.fa')
        dfa_test_cases = {
            "00": True,
            "1010": True,
            "01010": False,
            "111": True,
            "0": False,
            "": True,
            "1001": True
        }
        for string, expected in dfa_test_cases.items():
            result = dfa.simulate(string)
            status = "PASS" if result == expected else "FAIL"
            print(
                f"DFA Test '{string}': {'Accepted' if result else 'Rejected'} (Expected: {'Accepted' if expected else 'Rejected'}) - {status}")
    except Exception as e:
        print(f"DFA test failed with error: {e}", file=sys.stderr)
    print("-" * 20)

    # --- NFA Tests ---
    print("--- Testing NFA ---")
    try:
        nfa = parse_nfa_json('nfa_rules.fa')
        nfa_test_cases = {
            "01": True,
            "001": True,
            "11101": True,
            "0101": True,
            "10": False,
            "": False
        }
        for string, expected in nfa_test_cases.items():
            result = nfa.simulate(string)
            status = "PASS" if result == expected else "FAIL"
            print(
                f"NFA Test '{string}': {'Accepted' if result else 'Rejected'} (Expected: {'Accepted' if expected else 'Rejected'}) - {status}")
    except Exception as e:
        print(f"NFA test failed with error: {e}", file=sys.stderr)
    print("-" * 20)

    # --- PDA Tests ---
    print("--- Testing PDA ---")
    try:
        pda = parse_pda_json('pda_rules.fa')
        pda_test_cases = {
            "0011": True,
            "01": True,
            "000111": True,
            "001": False,
            "10": False,
            "": True
        }
        for string, expected in pda_test_cases.items():
            result = pda.simulate(string)
            status = "PASS" if result == expected else "FAIL"
            print(
                f"PDA Test '{string}': {'Accepted' if result else 'Rejected'} (Expected: {'Accepted' if expected else 'Rejected'}) - {status}")
    except Exception as e:
        print(f"PDA test failed with error: {e}", file=sys.stderr)
    print("-" * 20)

    # --- Turing Machine Tests ---
    print("--- Testing Turing Machine ---")
    try:
        tm = parse_tm_json('tm_rules.fa')
        tm_test_cases = {
            "012": "Accepted",
            "001122": "Accepted",
            "01": "Rejected",
            "00122": "Rejected",
            "": "Rejected"
        }
        for string, expected in tm_test_cases.items():
            result = tm.simulate(string)
            status = "PASS" if result == expected else "FAIL"
            print(
                f"TM Test '{string}': {result} (Expected: {expected}) - {status}")
    except Exception as e:
        print(f"TM test failed with error: {e}", file=sys.stderr)
    print("-" * 20)


if __name__ == '__main__':
    run_tests()
