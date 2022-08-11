import click
from pathlib import Path
from flag.interface import Lexer, Parser
from flag.utils.errors import LexicalException, SyntaxException


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path))
def lexico(input: Path, source: Path, output: Path):

    lexer = Lexer.parse(input)

    parser = Parser.parse(input)

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
            tokens = lexer.run(line)
            parser.validate(tokens)
        except SyntaxException as err:
            print(f"Syntax error on line {index}")
            exit(err)
        except LexicalException:
            print(f"Lexical error on line {index}")
            exit(err)

    print(f"{len(lines)} lines of code were validated")

    if output is not None:
        lexer.save(output)


if __name__ == "__main__":
    cli()
