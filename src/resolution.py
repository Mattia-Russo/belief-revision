"""
Implements the logical inference engine using propositional resolution.
"""
from __future__ import annotations
from typing import List, Set, FrozenSet
from logic_ast import Not
from parser import parse_formula
from cnf import CNFConverter, Clause, ClauseSet


class ResolutionProver:
    @staticmethod
    def resolve(c1: Clause, c2: Clause) -> Set[Clause]:
        resolvents = set()

        for lit in c1:
            comp = CNFConverter.negate_literal(lit)
            if comp in c2:
                new_clause = frozenset((c1 - {lit}) | (c2 - {comp}))
                if not CNFConverter.is_tautology(new_clause):
                    resolvents.add(new_clause)

        return resolvents

    @staticmethod
    def is_unsatisfiable(clauses: ClauseSet) -> bool:
        clauses = set(clauses)

        while True:
            new_clauses = set()
            clause_list = list(clauses)

            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    resolvents = ResolutionProver.resolve(clause_list[i], clause_list[j])
                    if frozenset() in resolvents:
                        return True
                    new_clauses |= resolvents

            if new_clauses.issubset(clauses):
                return False

            clauses |= new_clauses

    @staticmethod
    def entails(kb_formulas: List[str], query: str) -> bool:
        clauses: ClauseSet = set()

        for formula in kb_formulas:
            clauses |= CNFConverter.expr_to_clauses(parse_formula(formula))

        clauses |= CNFConverter.expr_to_clauses(Not(parse_formula(query)))
        return ResolutionProver.is_unsatisfiable(clauses)

    @staticmethod
    def is_consistent(kb_formulas: List[str]) -> bool:
        clauses: ClauseSet = set()
        for formula in kb_formulas:
            clauses |= CNFConverter.expr_to_clauses(parse_formula(formula))
        return not ResolutionProver.is_unsatisfiable(clauses)