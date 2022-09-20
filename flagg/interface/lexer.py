import json
import pathlib
import re
import click
from typing import Dict, List, Union
from tabulate import tabulate
from autome.utils.dataclasses import Definition, Token

from flagg.utils.errors import LexicalException


class Lexer:
    """
    Interface for generating lexical analyzers using Thompson's building algorithm
    """

    keywords: List[str]
    """
    List of keywords for the language, keywords will be used as a special type of token,
    evaluated before the other types and with higher precedence
    """
    definitions: List[Definition]
    """
    List of regular definitions used to compose more complex tokens
    A regular definition itself WILL NOT be evaluated as a token type
    """
    tokens: List[Definition]
    """
    List of token definitions that will be used by the lexer as rules for findind tokens 
    in a source code. Tokens are created in order, so you can use already defined tokens
    as part of the definition of the later tokens, e.g:
        
    digit => 0|1|2|3|4|5|6|7|8|9

    float => digit* . digit* 
    """
    verbose: bool
    """Flag for enabling verbose mode
    """

    def __init__(
        self, input: Union[click.Path, pathlib.Path, None], verbose: bool = False
    ) -> None:
        self.verbose = verbose

        if input is None:
            pass
        elif isinstance(input, click.Path) or isinstance(input, pathlib.Path):
            self.input = self.parse_input(input)
            self.build_lexer()
        else:
            raise Exception("Invalid arguments")

    @classmethod
    def parse(cls, input: Union[click.Path, pathlib.Path], verbose: bool = False):
        """Parses the input file with the definitions of a lexical analyzer into useful data for the program"""
        with open(input) as file:
            content = json.load(file)

        if not content.get("automata"):
            return Lexer(input, verbose)

        instance = Lexer(None, verbose)
        instance.keywords = content["reserved-keywords"]
        instance.definitions = [
            Definition(definition["name"], definition["expression"])
            for definition in content["definitions"]
        ]
        instance.tokens = [
            Definition(definition["name"], definition["expression"])
            for definition in content["tokens"]
        ]

        return instance

    def parse_input(self, input: click.Path):
        """Parses the input file with the definitions of a lexical analyzer into useful data for the program"""
        with open(input) as file:
            content = json.load(file)

        self.keywords = content["reserved-keywords"]
        self.definitions = [
            Definition(definition["name"], definition["expression"])
            for definition in content["definitions"]
        ]
        self.tokens = [
            Definition(definition["name"], definition["expression"])
            for definition in content["tokens"]
        ]

    def save(self, output: click.Path) -> None:
        data = {
            "reserved-keywords": self.keywords,
            "definitions": [definition.dict() for definition in self.definitions],
            "tokens": [token.dict() for token in self.tokens],
        }

        with open(output, "w+") as fp:
            fp.write(json.dumps(data))

    def build_lexer(self) -> None:
        """
        Uses the regular definitions and token definitions to build a DFA that can identify tokens of
        the defined language. It's a huge DFA which accepts any word of any of the definitions passed
        as arguments, identifiying the type of token by a label 'type' marked on the final states of
        the 'building' automatas
        """

        if self.verbose:
            data = self.definitions + self.tokens
            data = [[entry.name, entry.expression] for entry in data]
            headers = ["Type", "Expression"]
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

        defined_tokens: List[Definition] = []
        for token in self.tokens:
            for definition in self.definitions:
                if definition.name in token.expression:
                    token.expression = token.expression.replace(
                        definition.name, f"({definition.expression})"
                    )

            for defined_token in defined_tokens:
                if defined_token.name in token.expression:
                    token.expression = token.expression.replace(
                        defined_token.name, f"({defined_token.expression})"
                    )

            token.regex = re.compile(f"^{token.expression}$")
            defined_tokens.append(token)

    def run(self, code: str) -> List[Dict[str, str]]:
        """
        Evaluates a given source code with a previously built lexer.

        If at any time there's a symbol the DFA can't recognize, or a invalid token pattern, raises an
        exception. Otherwise, returns a list of the recognized tokens.
        """
        source = code.strip()

        if self.verbose:
            data = []
            lines = source.split("\n")
            for index, line in enumerate(lines):
                data.append([index, line])
            print(tabulate(data, headers=["Source code"], tablefmt="fancy_grid"))

        found: List[Token] = []

        i = 0
        error = False

        """
            Estratégias de leitura: o código é lido a primeira vez (L1) da direita para esquerda,
            checando a cada caractere se a palavra atual é parte de um token.

            Caso em L1 a palavra não seja parte de um token, fazemos uma leitura (L2) removendo
            o último caractere lido, para checar se no passo anterior tinhamos um token.

            Caso em L2 não seja encontrado um token, ainda assim será feita uma terceira leitura (L3)
            até o final da linha de código, para checar por possíveis tokens que não podem ser identificados
            apenas lendo o seu início (como por exemplo strings, a string 'abc' não pode ser identificada apenas
            pela leitura de ' ou 'a)

            Caso L3 não consiga encontrar um token, é levantado um erro léxico.
        """
        while i < len(source):
            word = ""

            while i < len(source) and source[i] != "\n":
                word += source[i]
                word = word.strip()
                i += 1

                if word in self.keywords:
                    continue

                for type in self.tokens:
                    if type.regex.match(word):
                        # L3
                        if error:
                            found.append(Token(type.name, word))
                            word = ""
                            error = False
                        break
                else:
                    # L2
                    if word[:-1] in self.keywords:
                        found.append(Token("keyword", word))
                        word = ""
                        error = False
                        i -= 1
                        continue

                    for type in self.tokens:
                        if type.regex.match(word[:-1]):
                            found.append(Token(type.name, word))
                            word = ""
                            error = False
                            i -= 1
                            break
                    else:
                        if word != "" and word != " ":
                            error = True
                            continue

            if error:
                raise LexicalException(
                    f"Lexical Error, unexpected symbol sequence: {word}", i
                )

            i += 1

        if self.verbose:
            data = []
            for entry in found:
                data.append([entry.type, entry.value])
            print(tabulate(data, headers=["TokenType", "Value"], tablefmt="fancy_grid"))

        return found
