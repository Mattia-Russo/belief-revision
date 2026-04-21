# Belief Revision
Belief Revision assignment for the Introduction to AI (02180) course at DTU.
The assignment implements a modular belief revision engine for propositional logic, designed around the course topics of propositional inference, CNF conversion, resolution, and AGM-style belief change.

---
## Project Structure
```text
src/
├── main.py
├── logic_ast.py
├── parser.py
├── cnf.py
├── resolution.py
├── belief_base.py
├── cli.py
└── tests.py
```

### File Overview
- **`main.py`**: Entry point of the project. Runs a small demonstration of the belief revision engine by creating a belief base, performing revision, and printing the results.

- **`logic_ast.py`**: Defines the abstract syntax tree (AST) classes for propositional logic formulas, such as variables, negation, conjunction, disjunction, implication, and biconditional.

- **`parser.py`**: Parses propositional formulas written as strings into AST objects. It includes tokenization and recursive-descent parsing with operator precedence.

- **`cnf.py`**: Converts formulas into conjunctive normal form (CNF) and extracts clauses. This module prepares formulas for resolution-based inference.

- **`resolution.py`** Implements the logical inference engine using propositional resolution. It is used to test entailment and consistency of the belief base.

- **`belief_base.py`**: Defines the belief base and belief objects, including priorities. It implements the main belief change operations: expansion, contraction, and revision.

- **`cli.py`**: Implements the Command Line Interface. Running this file the user is able to use the belief engine from the terminal.

- **`tests.py`**: Contains test cases for the system, including checks inspired by AGM postulates such as Success, Vacuity, Consistency, and Extensionality.

---
### Design Overview
The project is split into separate layers so that each module has one clear responsibility:
1. **Formula representation**  
   Propositional formulas are represented internally as AST objects rather than raw strings.

2. **Parsing**  
   Input formulas written in symbolic form are converted into ASTs.

3. **CNF transformation**  
   Formulas are transformed into conjunctive normal form so they can be used by the resolution engine.

4. **Logical inference**  
   Entailment is checked using resolution by testing whether `KB ∧ ¬φ` is unsatisfiable.

5. **Belief revision**  
   The belief base supports:
   - **Expansion**: add a new belief
   - **Contraction**: remove beliefs until a target formula is no longer entailed
   - **Revision**: contract by the negation of the new information, then expand by the new information

---
## Input Syntax
The parser supports symbolic propositional logic with:
- Negation: `~`
- Conjunction: `&`
- Disjunction: `|`
- Implication: `->`
- Biconditional: `<->`

Examples:
```text
p
~q
(p & q)
(p -> q)
((p -> q) & p)
(p <-> (q | r))
```

A simple example belief base:
```python
kb = BeliefBase([
    Belief("p", 5),
    Belief("q", 3),
    Belief("p -> q", 4),
])
```
Then revise by `~q`:
```python
revised = kb.revise("~q", priority=100)
```
This gives a new belief base that accepts the new information and removes lower-priority conflicting beliefs when needed.

---
## How to run
Run the demo program:
```bash
python main.py
```

Run the tests:
```bash
python tests.py
```
The demo in `main.py` creates a small belief base, performs belief revision with new information, and prints the updated result.

---
## Requirements
- Python 3.10 or newer
- No external dependencies are required
- The project uses only the Python standard library