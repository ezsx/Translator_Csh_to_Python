from Snow_Lukin_refactored_swift_to_python_analyzer.Lexema import Lexeme, LexemeType, LexicalPattern, SystemTable, UniqueLexemeTable
import re


class LexicalAnalyzer:
    def __init__(self, include_separators=False):
        self.lexemes = []
        self.identifier_table = UniqueLexemeTable()
        self.literal_table = UniqueLexemeTable()
        self.constant_table = UniqueLexemeTable()
        self.include_separators = include_separators

    def convert(self, code: str) -> None:
        self.reset()
        while code:
            status = False
            for lexeme_type, pattern in self.states:
                match = re.search(pattern, code)
                # print(match)
                if match:
                    value = match.group()
                    print(value)
                    self.update_tables(value, lexeme_type)
                    code = code[match.end():]
                    status = True
                    break
            if not status:
                raise ValueError("Unexpected symbol.")

    def reset(self) -> None:
        self.lexemes.clear()
        self.identifier_table.remove_all()
        self.literal_table.remove_all()
        self.constant_table.remove_all()

    def get_user_table(self, table_type, UserTable) -> list[Lexeme]:
        if table_type == UserTable.identifier:
            return self.identifier_table.data
        elif table_type == UserTable.constant:
            return self.constant_table.data
        elif table_type == UserTable.literal:
            return self.literal_table.data

    def update_tables(self, value: str, lexeme_type: int) -> None:
        lexeme = None
        if lexeme_type == LexemeType.identifier and SystemTable.keyword.getId(value) is not None:
            lexeme = Lexeme(SystemTable.keyword.getId(value), value, LexemeType.keyword)
        elif lexeme_type == LexemeType.identifier:
            self.identifier_table.update(value, lexeme_type)
            lexeme = self.identifier_table.get_lexeme(value)
        elif lexeme_type == LexemeType.constant:
            self.constant_table.update(value, lexeme_type)
            lexeme = self.constant_table.get_lexeme(value)
        elif lexeme_type == LexemeType.literal:
            self.literal_table.update(value, lexeme_type)
            lexeme = self.literal_table.get_lexeme(value)
        elif lexeme_type == LexemeType.operator:
            lexeme = Lexeme(SystemTable.operator.getId(value), value, lexeme_type)
        elif lexeme_type == LexemeType.divider:
            lexeme = Lexeme(SystemTable.divider.getId(value), value, lexeme_type)
        elif lexeme_type == LexemeType.separator and self.include_separators:
            lexeme = Lexeme(SystemTable.separator.getId(value), value, lexeme_type)
        if lexeme is not None:
            self.lexemes.append(lexeme)

    @property
    def states(self) -> tuple[tuple[int, str], ...]:
        return (
            (LexemeType.separator, LexicalPattern.separator),
            (LexemeType.comment, LexicalPattern.comment),
            (LexemeType.identifier, LexicalPattern.identifier),
            (LexemeType.constant, LexicalPattern.constant),
            (LexemeType.literal, LexicalPattern.literal),
            (LexemeType.operator, LexicalPattern.operator),
            (LexemeType.divider, LexicalPattern.divider)
        )


s = r"""
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
a = LexicalAnalyzer(include_separators=True)
a.convert(s)
# print(a.lexemes)
[print(i) for i in a.lexemes]
