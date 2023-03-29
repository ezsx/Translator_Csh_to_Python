class Lexeme:
    def __init__(self, id, value, type):
        self._id = id
        self._value = value
        self._type = type

    def __str__(self):
        return f"Lexeme(id={self.id}, value='{self.value}', type={self.type})"

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def raw_value(self):
        if self.type == LexemeType.separator:
            return "" if self.value == " " else self.value
        elif self.type in [LexemeType.arrayAddressCounter, LexemeType.functionCall, LexemeType.mark]:
            return self.value + " "
        elif self.type in [LexemeType.conditional, LexemeType.goto]:
            return self.type.value
        else:
            return self.type.value + "_" + str(self.id) + " "

    @property
    def precedence(self):
        return SystemTable.getPrecedence(self.value, self.type)

    def __lt__(self, other):
        return self.precedence < other.precedence

    @property
    def is_opening_square_bracket(self):
        return self.type == LexemeType.divider and self.value == "["

    @property
    def is_closing_square_bracket(self):
        return self.type == LexemeType.divider and self.value == "]"

    @property
    def is_opening_round_bracket(self):
        return self.type == LexemeType.divider and self.value == "("

    @property
    def is_closing_round_bracket(self):
        return self.type == LexemeType.divider and self.value == ")"

    @property
    def is_opening_bracket(self):
        return self.type == LexemeType.divider and self.value == "{"

    @property
    def is_closing_bracket(self):
        return self.type == LexemeType.divider and self.value == "}"


class UniqueLexemeTable:
    def __init__(self):
        self.hashmap = {}
        self.data = []

    def update(self, value, type):
        if value not in self.hashmap:
            lexeme = Lexeme(len(self.hashmap), value, type)
            self.hashmap[value] = lexeme
            self.data.append(lexeme)

    def get_lexeme(self, value):
        return self.hashmap.get(value)

    def remove_all(self):
        self.hashmap.clear()
        self.data.clear()


from enum import Enum


class LexemeType(str, Enum):
    identifier = "I"
    keyword = "K"
    constant = "C"
    literal = "L"
    operator = "O"
    divider = "D"
    separator = "S"
    comment = ""

    arrayAddressCounter = "AAC"
    functionCall = "FC"
    conditional = "Condition"
    goto = "Goto"
    mark = "M"
    declaration = "DC"
    loopMark = "LM"
    funcBodyStart = "FBS"
    funcBodyEnd = "FBE"


class SystemTable(Enum):
    divider = 1
    operator = 2
    keyword = 3
    separator = 4

    @staticmethod
    def getPrecedence(value, type):
        precedenceTable = {
            "if": 0,
            "while": 0,
            "(": 0,
            "[": 0,
            "return": 0,
            "]": 1,
            ")": 1,
            "{": 1,
            "else": 1,
            ";": 1,
            "--": 2,
            "++": 2,
            "=": 3,
            "+=": 3,
            "-=": 3,
            "*=": 3,
            "/=": 3,
            "%=": 3,
            "<": 3,
            ">": 3,
            "<=": 3,
            ">=": 3,
            "!=": 3,
            "==": 3,
            "+": 4,
            "-": 4,
            "*": 5,
            "/": 5,
            "%": 5,
        }

        if type in ["functionCall", "arrayAddressCounter", "mark", "loopMark"]:
            return 0
        elif type == "keyword":
            return precedenceTable.get(value, 10)
        else:
            return precedenceTable.get(value, 10)

    def getId(self, value):
        if self == SystemTable.divider:
            return self.dividers.get(value)
        elif self == SystemTable.operator:
            return self.operators.get(value)
        elif self == SystemTable.keyword:
            return self.keywords.get(value)
        elif self == SystemTable.separator:
            return self.separators.get(value)

    def getTable(self):
        if self == SystemTable.divider:
            return [Lexeme(i + 1, v, LexemeType.divider) for i, v in enumerate(sorted(self.dividers.keys()))]
        elif self == SystemTable.operator:
            return [Lexeme(i + 1, v, LexemeType.operator) for i, v in enumerate(sorted(self.operators.keys()))]
        elif self == SystemTable.keyword:
            return [Lexeme(i + 1, v, LexemeType.keyword) for i, v in enumerate(sorted(self.keywords.keys()))]
        elif self == SystemTable.separator:
            return []

    @property
    def dividers(self):
        symbols = ["{", "}", "(", ")", ",", ";", r"\\", "[", "]"]
        return dict(zip(symbols, range(1, len(symbols) + 1)))

    @property
    def operators(self):
        symbols = ["+", "-", "*", "/", "%", "=", ">", "<", "!", "&", "|", "&&", "||", "++", "--", "+=", "-=", "/=",
                   "*=", "%=", "<=", ">=", "==", "!="]
        return dict(zip(symbols, range(1, len(symbols) + 1)))

    @property
    def keywords(self):
        symbols = ["class", "if", "else", "while", "int", "float", "char", "string", "namespace", "void", "static",
                   "using", "System", "break", "return"]
        return dict(zip(symbols, range(1, len(symbols) + 1)))

    @property
    def separators(self):
        symbols = [" ", r"\n", r"\t"]
        return dict(zip(symbols, range(1, len(symbols) + 1)))

import re


class LexicalPattern:
    # This regex should match strings like:
    #  // This is a comment
    #  //This is another comment with symbols like $!@#
    #  /* This is a multi-line comment */
    #  /* This is a multi-line comment with symbols like $!@# */.
    comment = r"^(//.*|/\*(([^\*]|\s)*)\*/)"

    # Should match any operators like: +, ++, -= etc.
    operator = r"^([-*+%=><!&|]{1,2}|[/])"

    # Should match strings for identifier names
    identifier = r"^([a-zA-Z_][a-zA-Z0-9_]*)"

    # Should match string like: "something"
    literal = r"^(\"[^\n\"]*\")"

    # Should match strings like: 123, 0.456, .789, 1.23e4, 1.23E+4, 0.456, 1.23e-4, and so on.
    constant = r"^(((\d)+([\.](\d)*([eE][+-]?(\d)+)?)?|([\.](\d)+([eE][+-]?(\d)+)?)))"

    # Should match strings like: {, }, (, ), `,`, ;, [, ]
    divider = r'^[\{\}\(\),.;\[\]]'

    # Should match strings of whitespaces, newLines and tabs
    separator = r"^([\s])"

    # Convert regex patterns to compiled regex objects
    comment = re.compile(comment)
    operator = re.compile(operator)
    identifier = re.compile(identifier)
    literal = re.compile(literal)
    constant = re.compile(constant)
    divider = re.compile(divider)
    separator = re.compile(separator)
