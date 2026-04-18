"""
Defines the belief base and belief objects, including priorities.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from resolution import ResolutionProver


@dataclass
class Belief:
    formula: str
    priority: int

    def __str__(self) -> str:
        return f"{self.formula} [priority={self.priority}]"


class BeliefBase:
    def __init__(self, beliefs: Optional[List[Belief]] = None):
        self._beliefs: List[Belief] = beliefs[:] if beliefs else []

    @property
    def beliefs(self) -> List[Belief]:
        return self._beliefs[:]

    def formulas(self) -> List[str]:
        return [belief.formula for belief in self._beliefs]

    def add_belief(self, formula: str, priority: int = 1) -> None:
        if formula not in self.formulas():
            self._beliefs.append(Belief(formula, priority))

    def remove_belief(self, formula: str) -> None:
        self._beliefs = [b for b in self._beliefs if b.formula != formula]

    def copy(self) -> "BeliefBase":
        return BeliefBase(self._beliefs)

    def entails(self, formula: str) -> bool:
        return ResolutionProver.entails(self.formulas(), formula)

    def is_consistent(self) -> bool:
        return ResolutionProver.is_consistent(self.formulas())

    def expand(self, formula: str, priority: int = 1) -> "BeliefBase":
        new_base = self.copy()
        new_base.add_belief(formula, priority)
        return new_base

    def contract(self, formula: str) -> "BeliefBase":
        """
        Priority-based contraction.
        Removes lower-priority beliefs first until the base no longer entails formula.
        """
        new_base = self.copy()

        if not new_base.entails(formula):
            return new_base

        ordered_beliefs = sorted(new_base._beliefs, key=lambda b: (b.priority, b.formula))

        for belief in ordered_beliefs:
            if not new_base.entails(formula):
                break
            new_base.remove_belief(belief.formula)

        return new_base

    def revise(self, formula: str, priority: int = 100) -> "BeliefBase":
        """
        Levi identity:
            B * phi = (B ÷ ~phi) + phi
        """
        negated_formula = f"~({formula})"
        contracted = self.contract(negated_formula)
        return contracted.expand(formula, priority)

    def __str__(self) -> str:
        if not self._beliefs:
            return "{}"
        return "{ " + ", ".join(str(b) for b in self._beliefs) + " }"