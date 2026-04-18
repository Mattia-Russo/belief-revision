"""
Parses propositional formulas written as strings into AST objects
"""
from __future__ import annotations
from typing import List, Optional
from logic_ast import Expr, Var, Not, And, Or, Imp, Iff


class Tokenizer:
    @staticmethod
    def tokenize(text: str) -> List[str]:
        text = text.replace(" ", "")
        tokens = []
        i = 0

        while i < len(text):
            if text.startswith("<->", i):
                tokens.append("<->")
                i += 3
            elif text.startswith("->", i):
                tokens.append("->")
                i += 2
            elif text[i] in "()~&|":
                tokens.append(text[i])
                i += 1
            else:
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                    j += 1
                if j == i:
                    raise ValueError(f"Unexpected character at position {i}: {text[i]}")
                tokens.append(text[i:j])
                i = j

        return tokens


class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[str]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected: Optional[str] = None) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input.")
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected}, got {token}.")
        self.pos += 1
        return token

    def parse(self) -> Expr:
        expr = self.parse_iff()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()}")
        return expr

    def parse_iff(self) -> Expr:
        left = self.parse_imp()
        while self.peek() == "<->":
            self.consume("<->")
            right = self.parse_imp()
            left = Iff(left, right)
        return left

    def parse_imp(self) -> Expr:
        left = self.parse_or()
        while self.peek() == "->":
            self.consume("->")
            right = self.parse_or()
            left = Imp(left, right)
        return left

    def parse_or(self) -> Expr:
        left = self.parse_and()
        while self.peek() == "|":
            self.consume("|")
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self) -> Expr:
        left = self.parse_not()
        while self.peek() == "&":
            self.consume("&")
            right = self.parse_not()
            left = And(left, right)
        return left

    def parse_not(self) -> Expr:
        if self.peek() == "~":
            self.consume("~")
            return Not(self.parse_not())
        return self.parse_atom()

    def parse_atom(self) -> Expr:
        token = self.peek()
        if token == "(":
            self.consume("(")
            expr = self.parse_iff()
            self.consume(")")
            return expr
        if token is None:
            raise ValueError("Unexpected end of input.")
        if token in {"&", "|", "->", "<->", ")"}:
            raise ValueError(f"Unexpected token: {token}")
        self.consume()
        return Var(token)


def parse_formula(text: str) -> Expr:
    tokens = Tokenizer.tokenize(text)
    return Parser(tokens).parse()