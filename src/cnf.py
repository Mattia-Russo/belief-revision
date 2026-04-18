"""
Converts formulas into conjunctive normal form (CNF) and extracts clauses
"""
from __future__ import annotations
from typing import List, Set, FrozenSet
from logic_ast import Expr, Var, Not, And, Or, Imp, Iff

Literal = str
Clause = FrozenSet[Literal]
ClauseSet = Set[Clause]


class CNFConverter:
    @staticmethod
    def eliminate_implications(expr: Expr) -> Expr:
        if isinstance(expr, Var):
            return expr
        if isinstance(expr, Not):
            return Not(CNFConverter.eliminate_implications(expr.expr))
        if isinstance(expr, And):
            return And(
                CNFConverter.eliminate_implications(expr.left),
                CNFConverter.eliminate_implications(expr.right),
            )
        if isinstance(expr, Or):
            return Or(
                CNFConverter.eliminate_implications(expr.left),
                CNFConverter.eliminate_implications(expr.right),
            )
        if isinstance(expr, Imp):
            return Or(
                Not(CNFConverter.eliminate_implications(expr.left)),
                CNFConverter.eliminate_implications(expr.right),
            )
        if isinstance(expr, Iff):
            left = CNFConverter.eliminate_implications(expr.left)
            right = CNFConverter.eliminate_implications(expr.right)
            return And(Or(Not(left), right), Or(Not(right), left))
        raise TypeError(f"Unknown expression type: {type(expr)}")

    @staticmethod
    def to_nnf(expr: Expr) -> Expr:
        if isinstance(expr, Var):
            return expr
        if isinstance(expr, Not):
            inner = expr.expr
            if isinstance(inner, Var):
                return expr
            if isinstance(inner, Not):
                return CNFConverter.to_nnf(inner.expr)
            if isinstance(inner, And):
                return Or(
                    CNFConverter.to_nnf(Not(inner.left)),
                    CNFConverter.to_nnf(Not(inner.right)),
                )
            if isinstance(inner, Or):
                return And(
                    CNFConverter.to_nnf(Not(inner.left)),
                    CNFConverter.to_nnf(Not(inner.right)),
                )
            raise ValueError("Implications should be removed before NNF.")
        if isinstance(expr, And):
            return And(CNFConverter.to_nnf(expr.left), CNFConverter.to_nnf(expr.right))
        if isinstance(expr, Or):
            return Or(CNFConverter.to_nnf(expr.left), CNFConverter.to_nnf(expr.right))
        raise TypeError(f"Unexpected type in NNF conversion: {type(expr)}")

    @staticmethod
    def distribute(a: Expr, b: Expr) -> Expr:
        if isinstance(a, And):
            return And(
                CNFConverter.distribute(a.left, b),
                CNFConverter.distribute(a.right, b),
            )
        if isinstance(b, And):
            return And(
                CNFConverter.distribute(a, b.left),
                CNFConverter.distribute(a, b.right),
            )
        return Or(a, b)

    @staticmethod
    def to_cnf_expr(expr: Expr) -> Expr:
        expr = CNFConverter.eliminate_implications(expr)
        expr = CNFConverter.to_nnf(expr)

        def convert(e: Expr) -> Expr:
            if isinstance(e, (Var, Not)):
                return e
            if isinstance(e, And):
                return And(convert(e.left), convert(e.right))
            if isinstance(e, Or):
                return CNFConverter.distribute(convert(e.left), convert(e.right))
            raise TypeError(f"Unexpected type during CNF conversion: {type(e)}")

        return convert(expr)

    @staticmethod
    def flatten_and(expr: Expr) -> List[Expr]:
        if isinstance(expr, And):
            return CNFConverter.flatten_and(expr.left) + CNFConverter.flatten_and(expr.right)
        return [expr]

    @staticmethod
    def flatten_or(expr: Expr) -> List[Expr]:
        if isinstance(expr, Or):
            return CNFConverter.flatten_or(expr.left) + CNFConverter.flatten_or(expr.right)
        return [expr]

    @staticmethod
    def literal_of(expr: Expr) -> Literal:
        if isinstance(expr, Var):
            return expr.name
        if isinstance(expr, Not) and isinstance(expr.expr, Var):
            return "~" + expr.expr.name
        raise ValueError(f"Expression is not a literal: {expr}")

    @staticmethod
    def negate_literal(literal: Literal) -> Literal:
        return literal[1:] if literal.startswith("~") else "~" + literal

    @staticmethod
    def is_tautology(clause: Clause) -> bool:
        return any(CNFConverter.negate_literal(lit) in clause for lit in clause)

    @staticmethod
    def expr_to_clauses(expr: Expr) -> ClauseSet:
        cnf_expr = CNFConverter.to_cnf_expr(expr)
        clauses: ClauseSet = set()

        for conjunct in CNFConverter.flatten_and(cnf_expr):
            lits = frozenset(CNFConverter.literal_of(x) for x in CNFConverter.flatten_or(conjunct))
            if not CNFConverter.is_tautology(lits):
                clauses.add(lits)

        return clauses