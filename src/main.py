from belief_base import BeliefBase, Belief


def demo() -> None:
    kb = BeliefBase([
        Belief("p", 5),
        Belief("q", 3),
        Belief("p -> q", 4),
    ])

    print("Initial belief base:")
    print(kb)
    print()

    print("Does KB entail q?")
    print(kb.entails("q"))
    print()

    print("Does KB entail ~q?")
    print(kb.entails("~q"))
    print()

    revised = kb.revise("~q", priority=100)

    print("After revision by ~q:")
    print(revised)
    print()

    print("Does revised KB entail ~q?")
    print(revised.entails("~q"))
    print()

    print("Is revised KB consistent?")
    print(revised.is_consistent())


if __name__ == "__main__":
    demo()