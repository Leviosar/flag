from pathlib import Path
from flagg import __version__
from flagg.__main__ import cli
from click.testing import CliRunner
from flagg.handlers import cli_handler as handler
from flagg.utils.dataclasses import Token

def test_sample_code():
    
    tokens, table = handler(
        Path("./samples/lcc/lcc.lexer.json"), 
        Path("./samples/lcc/prof.code"), 
        None, 
        True, 
        False
    )

    expected_tokens = [
        [Token('l_curly', '{')],
        [Token('l_curly', '{')],
        [Token('type', 'float'), Token('id', 'x'), Token('semicolon', ';')],
        [Token('type', 'float'), Token('id', 'z'), Token('semicolon', ';')],
        [Token('type', 'bool'), Token('id', 'a'), Token('semicolon', ';')],
        [Token('type', 'int'), Token('id', 'i'), Token('semicolon', ';')],
        [Token('type', 'int'), Token('id', 'max'), Token('semicolon', ';')],
        [Token('id', 'x'), Token('attr', '='), Token('integer_literal', '0'), Token('semicolon', ';')],
        [Token('id', 'a'), Token('attr', '='), Token('boolean_literal', 'true'), Token('a1_op', '+'), Token('boolean_literal', 'false'),  Token('semicolon', ';')],
        [Token('id', 'max'), Token('attr', '='), Token('integer_literal', '10000'), Token('semicolon', ';')],
        [Token('keyword', 'for'), Token('l_par', '('), Token('id', 'i'), Token('attr', '='), Token('integer_literal', '1'), Token('semicolon', ';'), Token('id', 'i'), Token('c_op', '<='), Token('id', 'max'), Token('semicolon', ';'), Token('id', 'i'), Token('attr', '='), Token('id', 'i'), Token('a1_op', '+'), Token('integer_literal', '1'), Token('r_par', ')'), Token('l_curly', '{')]
    ]

    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            assert tokens[i][j] == expected_tokens[i][j]