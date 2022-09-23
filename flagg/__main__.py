import click
from pathlib import Path
from flagg.interface import Lexer, Parser, SymbolTable
from flagg.utils.errors import LexicalException, SyntaxException


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path))
@click.option("--verbose/--no-verbose", default=False)
@click.option("--syntatic/--no-syntatic", default=False)
def cli(input, source, output, verbose, syntatic):

    lexer = Lexer.parse(input, verbose=False)
    parser = Parser.parse(input, verbose=False)
    table = SymbolTable()

    with open(source, "r") as file:
        code = file.read()

    lines = code.split("\n")

    for index, line in enumerate(lines):
        # Handling blank lines
        if line.strip() == "":
            continue

        # Handling commments in a stupid way
        if line.strip()[0] == "#":
            continue

        try:
            tokens = lexer.run(line.strip())
            table.append(index + 1, tokens)
            
            if (syntatic):
                parser.validate(tokens)
        except SyntaxException as err:
            print(f"Syntax error on line {index}")
            exit(err)
        except LexicalException as err:
            print(f"Lexical error on line {index}, column {err.args[1]}.")
            print(line)
            print((" " * (err.args[1] - 1)) + "^")
            exit()

    print(f"\n {len(lines)} lines of code were validated")

    if verbose:
        print("\n Symbol table:")
        print(table)
        print("\n")

    if output is not None:
        lexer.save(output)


if __name__ == "__main__":
    cli()
