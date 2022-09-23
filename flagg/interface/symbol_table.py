from dataclasses import dataclass
from typing import Dict, List
from tabulate import tabulate
from flagg.utils.dataclasses import Token

class SymbolTable:
    def __init__(self, valid_types = ['id']) -> None:
        self.entries: Dict[str, SymbolTableEntry] = {}
        self.valid_types = valid_types

    def append(self, line, tokens: List[Token]):
        for token in filter(lambda t: t.type in self.valid_types, tokens):
            try:
                self.entries.get(token.value).lines.append(line)
            except AttributeError:
                self.entries[token.value] = SymbolTableEntry(token, [line])

    def __repr__(self) -> str:
        headers = ['word', 'type', 'lines']
        data = [[e.word, e.type, e.lines] for e in self.entries.values()]
        return tabulate(data, headers=headers, tablefmt="fancy_grid")

@dataclass
class SymbolTableEntry:

    lines: List[int]
    type: str
    word: str

    def __init__(self, token: Token, lines: List[int] = []):
        self.type = token.type
        self.word = token.value
        self.lines = lines