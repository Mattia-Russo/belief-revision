from belief_base import BeliefBase

HELP_TEXT = """
Commands:
    add <formula> [priority]   Add a formula (default priority=1)
    revise <formula>           Revise belief base with formula (Levi Identity)
    contract <formula>         Contract belief base by formula
    expand <formula>           Expand belief base with formula
    entails <formula>          Check if KB entails formula
    consistent                 Check if KB is consistent
    show                       Print current belief base
    clear                      Remove all beliefs
    help                       Show this message
    quit                       Exit

Formula syntax:
    ~p   p & q   p | q   p -> q   p <-> q   (p | q) & r
"""


def print_kb(kb: BeliefBase) -> None:
    beliefs = sorted(kb.beliefs, key=lambda b: -b.priority)
    if not beliefs:
        print("  (empty)")
    else:
        for b in beliefs:
            print(f"  [{b.priority}] {b.formula}")


def run_cli() -> None:
    kb = BeliefBase()
    print("Belief Revision Engine — 02180 Intro to AI")
    print("Type 'help' for commands, 'quit' to exit.\n")

    while True:
        try:
            raw = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=2)
        cmd = parts[0].lower()

        if cmd == "quit":
            print("Goodbye.")
            break

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd == "show":
            print("Current belief base:")
            print_kb(kb)

        elif cmd == "consistent":
            result = kb.is_consistent()
            print(f"  Consistent: {result}")

        elif cmd == "clear":
            kb = BeliefBase()
            print("  Belief base cleared.")

        elif cmd == "add":
            if len(parts) < 2:
                print("  Usage: add <formula> [priority]")
                continue
            formula = parts[1]
            priority = 1
            if len(parts) == 3:
                try:
                    priority = int(parts[2])
                except ValueError:
                    print("  Priority must be an integer.")
                    continue
            try:
                kb.add_belief(formula, priority)
                print(f"  Added: {formula} [priority={priority}]")
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "entails":
            if len(parts) < 2:
                print("  Usage: entails <formula>")
                continue
            formula = parts[1]
            try:
                result = kb.entails(formula)
                print(f"  KB entails '{formula}': {result}")
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "expand":
            if len(parts) < 2:
                print("  Usage: expand <formula>")
                continue
            formula = parts[1]
            try:
                kb = kb.expand(formula, priority=1)
                print(f"  Expanded with: {formula}")
                print("  New belief base:")
                print_kb(kb)
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "contract":
            if len(parts) < 2:
                print("  Usage: contract <formula>")
                continue
            formula = parts[1]
            try:
                kb = kb.contract(formula)
                print(f"  Contracted by: {formula}")
                print("  New belief base:")
                print_kb(kb)
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "revise":
            if len(parts) < 2:
                print("  Usage: revise <formula>")
                continue
            formula = parts[1]
            try:
                kb = kb.revise(formula, priority=100)
                print(f"  Revised with: {formula}")
                print("  New belief base:")
                print_kb(kb)
            except Exception as e:
                print(f"  Error: {e}")

        else:
            print(f"  Unknown command: '{cmd}'. Type 'help' for commands.")


if __name__ == "__main__":
    run_cli()