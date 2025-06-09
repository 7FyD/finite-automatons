# Finite Automata Emulators - Vlad Lungu

This project provides a set of command-line tools for simulating various types of finite automata.

### `dfa.py`

- **Rules:** `dfa_rules.fa`
- **Accepts:** Strings with an even number of '0's.

### `nfa.py`

- **Rules:** `nfa_rules.fa`
- **Accepts:** Strings ending in "01".

### `pda.py`

- **Rules:** `pda_rules.fa`
- **Accepts:** Strings of the form `0^n1^n` (where n >= 0).

### `tm.py`

- **Rules:** `tm_rules.fa`
- **Accepts:** Strings of the form `0^n1^n2^n` (where n >= 1).

## How to Run

Use the following command structure:
`python <emulator_script.py> <rules_file.fa> <input_string>`

**Example:**

```bash
python dfa.py dfa_rules.fa "1001"
```

## Testing

To run the included test suite, which verifies the emulators against their respective rule files:

```bash
python test.py
```
