import re
from enum import Enum


class TokenType(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    LITERAL = 3
    CONSTANT = 4
    OPERATOR = 5
    DIVIDER = 6
    SEPARATOR = 7
    COMMENT = 8


TOKEN_PATTERNS = {
    TokenType.KEYWORD: r"\b(class|if|else|while|int|float|char|string|namespace|void|static|using|System|break|return)\b",
    TokenType.IDENTIFIER: r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    TokenType.LITERAL: r"\"[^\n\"]*\"",
    TokenType.CONSTANT: r"(((\d)+([\.](\d)*([eE][+-]?(\d)+)?)?|([\.](\d)+([eE][+-]?(\d)+)?)))",
    TokenType.OPERATOR: r"([-*+%=><!&|]{1,2}|[/])",
    TokenType.DIVIDER: r"[\{\}\(\),.;\[\]]",
    TokenType.SEPARATOR: r"[\s]",
    TokenType.COMMENT: r"(//.*|/\*(([^\*]|\s)*)\*/)",
}


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type.name}: {self.value}"


class LexicalAnalyzer:
    def __init__(self, include_separators=False):
        self.include_separators = include_separators

    def tokenize(self, code: str):
        tokens = []
        while code:
            matched = False
            for token_type, pattern in TOKEN_PATTERNS.items():
                match = re.match(pattern, code)
                if match:
                    value = match.group()
                    if self.include_separators or token_type != TokenType.SEPARATOR:
                        tokens.append(Token(token_type, value))
                    code = code[len(value):]
                    matched = True
                    break
            if not matched:
                raise ValueError("Unexpected symbol.")
        return tokens

    def tokens_to_code(self, tokens):
        code = ""
        for token in tokens:
            code += token.value
        return code

    def tokens_to_code_2(self, tokens):
        code = ""
        for token in tokens:
            code += (" " + token.token_type.name + " ") if token.token_type.name != "SEPARATOR" else " "
        return code


source_code = r"""
using System;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            int x = 10;
            int y = 20;
            int sum = x + y;
            Console.WriteLine("The sum of {x} and {y} is {sum}.");
        }
    }
}
"""

analyzer = LexicalAnalyzer(include_separators=True)

tokens = analyzer.tokenize(source_code)

reconstructed_code = analyzer.tokens_to_code(tokens)

print("Reconstructed code:\n")
print(reconstructed_code)

