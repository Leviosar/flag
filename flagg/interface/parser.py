from typing import List
import click

from autome.grammars.cfg import CFG
from autome.utils.dataclasses import Token


class Parser:
    def __init__(self, grammar: CFG, verbose: bool = False) -> None:
        self.grammar = grammar
        self.verbose = verbose

    @classmethod
    def parse(cls, input: click.Path, verbose: bool = False) -> "Parser":
        """Parses a grammar contained inside a JSON file

        Args:
            input (click.Path): path to the file containing the grammar
            verbose (bool, optional): flag for verbose mode. Defaults to False.

        Returns:
            Parser: a new Parser interface instance
        """
        grammar = CFG.parse(input)

        return Parser(grammar, verbose)

    def validate(self, tokens: List[Token]) -> bool:
        """Validates a list of tokens using grammar's rules to check for sentence formation

        Args:
            tokens (List[Token]): List of tokens to be validated

        Returns:
            bool: result of the validation
        """
        return self.grammar.accept(tokens, self.verbose)
