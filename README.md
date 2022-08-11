# Flag 

Flag is an acronym Formal Language Analyzer Generator and that pretty much describes the functionality of this project.

## Formal Languages

Formal languages are a set of rules described upon an alphabet that resolves to a set of words, this type of construction is very powerful when solving a problem that requires a strict shape for possible solutions and it's the base for all programming languages.

## The compilation process

Programming languages are usually run in a computer, and the computer's processor has a closed set of instructions that are built directly on the chip, so if you want to "speak" with the processor, you have to use it's language (usually binary code, with each word representing one instruction that should be executed). The process of transforming your code into machine code is called compilation and is a whole area of study inside computer science.

If you don't know anything about compilation, probably this project is useless for you, but you can always learn and return here to use Flag. I would recommend starting with the book **"Compilers: Principles, Techniques, and Tools"** which served as a guide for my introductory course on formal languages on college. It starts from the basics on compilation, but it's necessary to have previous knowledge on some basic discrete mathematics concepts.

## What Flag can do

Currently we cover two out of three steps on the analysis phase of the compilation process, Flag can generate and run the lexical and syntatic analyzers based on JSON configuration files passed as input. It also can raise lexical and syntatic errors while validating your code.

You can install Flag and use it as a CLI application or you can add it to your python application as a library and use our interface to build some awesome things.

# Docs

## Installation

Install it via PIP

```
pip install --user flag
```

## Describing your language

Languages are described on a `JSON` file format with predefined keys. On CLI mode, you should pass the file as an argument, and in library mode you can use the `parse` method in the interfaces.

The JSON format for languages is shown below (JSON doesn't support comentaries, but i'm using here just for didatic purposes):

```json
{
    "version": "1.0.0",
    "reserved-keywords": ["const"],
    "definitions": [
        {"name": "digit", "expression": "0|1"}
    ],
    "tokens": [
        {"name": "binary", "expression": "(0|1)*"},
        {"name": "operator", "expression": "a n d|o r"},
        {"name": "left_parenthesis", "expression": "("},
        {"name": "right_parenthesis", "expression": ")"}
    ],
    "grammar": {
        "nonterminals": ["S"],
        "terminals": ["binary", "operator", "&"],
        "initial": "S",
        "productions": [
            {"head": "S", "body": "binary operator binary"}
        ]
    }
}
```

A more detailed view of all properties inside this JSON format is listed on the below table. `object` types must match keys and value types of the above example.

| Key                  | Type     | Description                                                               |
| :------------------- | :------- | :------------------------------------------------------------------------ |
| version              | string   | Version constraint for your language (currently unused)                   |
| reserved-keywords    | string[] | List of keywords in your language (will generate a special type of token) |
| definitions          | object[] | List of regular definitions that will be processed before tokens          |
| tokens               | object[] | List of token definitions, expression must be a REGEX                     |
| grammar              | object   | Parent object for grammar variables                                       |
| grammar.nonterminals | string[] | List of nonterminal symbols                                               |
| grammar.terminals    | string[] | List of terminal symbols (must match token names)                         |
| grammar.initial      | string   | Initial symbol of grammar                                                 |
| grammar.productions  | object[] | List of productions with head and body                                    |

You can add other convenient data inside this files, but newer versions of flag may use new key names for properties, if you wanna be sure we don't have any conflict, use a `metadata` key inside the file, this key will never be used inside Flag.

## Using Flag via CLI

After installing Flag with `pip`, be sure you have pip's binary folder on your system's $PATH, then you can call it with the instructions below:

```
Usage: flag [OPTIONS] INPUT SOURCE

Options:
  --output PATH
  --help         Show this message and exit.
```

## Using Flag as a Library

Flag has two separate interfaces for `lexer` and `parser`, they're located on the `flag.interface` module and have methods for parsing the analyzers using a JSON file.

A simple example of importing and using these interfaces:

```python
from flag.interface import Lexer, Parser

lines = ["A source code separated in lines", "Second line"]
# Creates a lexer
lexer = Lexer.parse(file_path)
# Creates a parser
parser = Parser.parse(file_path)

for line in lines:
    # Generates the list of tokens
    tokens = lexer.run(line)
    # Validate those tokens under the grammar
    if not parser.validate(tokens):
        raise "Error"
```

# Contributing

I could really use help on building meaningful and cool examples of languages, check out the `samples` folder to see the format for examples.