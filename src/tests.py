from belief_base import BeliefBase, Belief


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
    assert revised.entails("~q")


def test_vacuity() -> None:
    kb = BeliefBase([Belief("p", 5)])
    revised = kb.revise("q")
    expanded = kb.expand("q", priority=100)
    assert same_answers(revised, expanded, ["p", "q", "~q", "p&q"])


def test_consistency() -> None:
    kb = BeliefBase([
        Belief("p", 5),
        Belief("p -> q", 4),
    ])
    revised = kb.revise("~q")
    assert revised.is_consistent()


def test_extensionality_like() -> None:
    kb = BeliefBase([Belief("p", 5)])
    r1 = kb.revise("q")
    r2 = kb.revise("~~q")
    assert same_answers(r1, r2, ["p", "q", "~q"])


if __name__ == "__main__":
    test_success()
    test_vacuity()
    test_consistency()
    test_extensionality_like()
    print("All tests passed.")