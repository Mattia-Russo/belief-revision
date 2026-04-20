from belief_base import BeliefBase, Belief
from resolution import ResolutionProver


def same_answers(kb1: BeliefBase, kb2: BeliefBase, queries: list[str]) -> bool:
    for q in queries:
        if kb1.entails(q) != kb2.entails(q):
            return False
    return True


def test_success() -> None:
    kb = BeliefBase([
        Belief("p", 5),
        Belief("q", 3),
        Belief("p -> q", 4),
    ])
    revised = kb.revise("~q")
    assert revised.entails("~q"), "Success postulate failed"
    print("  [PASS] Success")


def test_inclusion() -> None:
    kb = BeliefBase([
        Belief("p", 5),
        Belief("p -> q", 4),
    ])
    phi = "~q"
    revised = kb.revise(phi)

    combined = kb.formulas() + [phi]

    for belief in revised.beliefs:
        f = belief.formula
        assert ResolutionProver.entails(combined, f), (f"Inclusion postulate failed: '{f}' is in B*phi but not in Cn(B+phi)")
    print("  [PASS] Inclusion")


def test_vacuity() -> None:
    kb = BeliefBase([Belief("p", 5)])
    revised = kb.revise("q")
    expanded = kb.expand("q", priority=100)
    assert same_answers(revised, expanded, ["p", "q", "~q", "p&q"]), "Vacuity postulate failed"
    print("  [PASS] Vacuity")


def test_consistency() -> None:
    kb = BeliefBase([
        Belief("p", 5),
        Belief("p -> q", 4),
    ])
    revised = kb.revise("~q")
    assert revised.is_consistent(), "Consistency postulate failed"
    print("  [PASS] Consistency")


def test_extensionality_like() -> None:
    kb = BeliefBase([Belief("p", 5)])
    r1 = kb.revise("q")
    r2 = kb.revise("~~q")
    assert same_answers(r1, r2, ["p", "q", "~q"]), "Extensionality postulate failed"
    print("  [PASS] Extensionality")


if __name__ == "__main__":
    print("Running AGM postulate tests...\n")
    test_success()
    test_inclusion()
    test_vacuity()
    test_consistency()
    test_extensionality_like()
    print("\nAll tests passed.")