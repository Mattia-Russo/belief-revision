"""
Defines the abstract syntax tree (AST) classes for propositional logic formulas
"""
from __future__ import annotations
from dataclasses import dataclass


class Expr:
    pass


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Not(Expr):
    expr: Expr

    def __str__(self) -> str:
        return f"~{self.expr}"


@dataclass(frozen=True)
class And(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} & {self.right})"


@dataclass(frozen=True)
class Or(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} | {self.right})"


@dataclass(frozen=True)
class Imp(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} -> {self.right})"


@dataclass(frozen=True)
class Iff(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} <-> {self.right})"