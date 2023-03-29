import re
from enum import Enum, auto


class State(Enum):
    START = auto()
    LETTER = auto()
    DIGIT = auto()
    OPERATION = auto()
    SEPARATOR = auto()
    DOT = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    END = auto()
    ERROR = auto()


class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, code):
        pos = 0
        state = State.START
        buffer = ""
        code = re.sub(r"//.*", "", code)  # Remove single-line comments

        def reset_state(char):
            nonlocal state, buffer
            state = State.START
            buffer = char

        def is_letter(char):
            return char.isalpha() or char == '_'

        def is_digit(char):
            return char.isdigit()

        def is_operation(char):
            return char in {'+', '-', '*', '/', '%', '&', '|', '^', '!', '=', '<', '>', '?', ':'}

        def is_separator(char):
            return char in {' ', ',', ';', '(', ')', '[', ']', '{', '}', '@'}

        def is_dot(char):
            return char == '.'

        while pos < len(code):
            char = code[pos]
            if char in ['\n', ' ', '\t']:
                pos += 1
                continue

            if state == State.START:
                if is_letter(char):
                    state = State.LETTER
                elif is_digit(char):
                    state = State.DIGIT
                elif is_operation(char):
                    state = State.OPERATION
                elif is_separator(char):
                    state = State.SEPARATOR
                elif is_dot(char):
                    state = State.DOT
                elif char == '\"':
                    state = State.STRING_LITERAL
                elif char == '\'':
                    state = State.CHAR_LITERAL
                else:
                    state = State.ERROR

            buffer += char

            if state == State.LETTER:
                if not (is_letter(char) or is_digit(char)):
                    self.tokens.append(buffer[:-1])
                    reset_state(char)

            elif state == State.DIGIT:
                if not (is_digit(char) or is_dot(char)):
                    self.tokens.append(buffer[:-1])
                    reset_state(char)

            elif state == State.OPERATION:
                if not is_operation(char):
                    self.tokens.append(buffer[:-1])
                    reset_state(char)

            elif state == State.SEPARATOR:
                if not is_separator(char):
                    self.tokens.append(buffer[:-1])
                    reset_state(char)

            elif state == State.DOT:
                if not is_digit(char):
                    self.tokens.append(buffer[:-1])
                    reset_state(char)

            elif state == State.STRING_LITERAL:
                if char == '\"':
                    self.tokens.append(buffer)
                    reset_state("")

            elif state == State.CHAR_LITERAL:
                if char == '\'':
                    self.tokens.append(buffer)
                    reset_state("")

            elif state == State.ERROR:
                print(f"Error: Unexpected character '{char}' at position {pos}")
                break

            pos += 1

        return self.tokens


analyzer = LexicalAnalyzer()
code = """
// Calculate the sum and product
class Program
{
    static void Main(string[] args)
    {
        int a = 378;
        double b = 0.73;
        Console.WriteLine("Sum: " + (a + b));
        Console.WriteLine("Product: " + (a * b));
    }
}
"""

tokens = analyzer.tokenize(code)
for token in tokens:
    print(token)
