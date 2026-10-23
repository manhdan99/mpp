# -*- coding: utf-8 -*-
"""
tokenizer.py - Bộ phân tích từ vựng (Lexer/Tokenizer) cho ngôn ngữ M++
Bảo đảm không bao giờ thay thế từ khóa nằm trong String hoặc Comment!
"""
import re
from dataclasses import dataclass
from typing import List, Optional

class TokenType:
    STRING = "STRING"
    CHAR = "CHAR"
    COMMENT_SINGLE = "COMMENT_SINGLE"
    COMMENT_MULTI = "COMMENT_MULTI"
    COMMENT_KE_CHUYEN = "COMMENT_KE_CHUYEN"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

    def __repr__(self):
        val_repr = repr(self.value)
        if len(val_repr) > 25:
            val_repr = val_repr[:22] + "...'"
        return f"Token({self.type}, {val_repr}, L{self.line}:C{self.col})"

# Danh sách token định nghĩa (type, internal_group_name, regex)
TOKEN_SPECS = [
    # 1. String literals (kèm escape sequence \")
    (TokenType.STRING, "STRING", r'"(?:\\.|[^"\\])*"'),
    # 2. Char literals (kèm escape sequence \')
    (TokenType.CHAR, "CHAR", r"'(?:\\.|[^'\\])*'"),
    # 3. Comment kiểu M++ "ke_chuyen: ..."
    (TokenType.COMMENT_KE_CHUYEN, "COMMENT_KE_CHUYEN", r'\bke_chuyen:[^\r\n]*'),
    # 4. Comment kiểu C++ một dòng // ...
    (TokenType.COMMENT_SINGLE, "COMMENT_SINGLE", r'//[^\r\n]*'),
    # 5. Comment kiểu C++ nhiều dòng /* ... */
    (TokenType.COMMENT_MULTI, "COMMENT_MULTI", r'/\*[\s\S]*?\*/'),
    # 6. Newlines (đếm dòng)
    (TokenType.NEWLINE, "NEWLINE", r'\r?\n'),
    # 7. Whitespace (dấu cách, tab)
    (TokenType.WHITESPACE, "WHITESPACE", r'[ \t\f\v]+'),
    # 8. Numbers (hex, float, int)
    (TokenType.NUMBER, "NUMBER", r'(?:0[xX][0-9a-fA-F]+|\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fFlLuU]*)'),
    # 9. Operators đa ký tự
    (TokenType.OPERATOR, "OP_MULTI", r'(?:<<=|>>=|<<|>>|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|%=|->\*|->|::)'),
    # 10. Identifiers (tên biến, từ khóa M++)
    (TokenType.IDENTIFIER, "IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    # 11. Punctuation và operators đơn ký tự
    (TokenType.PUNCTUATION, "PUNCTUATION", r'[;,\(\)\{\}\[\]\.\?:#]'),
    (TokenType.OPERATOR, "OP_SINGLE", r'[\+\-\*/%=\<\>!&\|\^~]'),
]

GROUP_TO_TYPE = {grp: t_type for t_type, grp, _ in TOKEN_SPECS}
MASTER_REGEX = re.compile('|'.join(f'(?P<{grp}>{pattern})' for _, grp, pattern in TOKEN_SPECS))

class Tokenizer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.line = 1
        self.col = 1
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        pos = 0
        line = 1
        col = 1
        length = len(self.source)

        while pos < length:
            match = MASTER_REGEX.match(self.source, pos)
            if not match:
                # Ký tự lạ không nhận diện được
                bad_char = self.source[pos]
                tokens.append(Token(TokenType.PUNCTUATION, bad_char, line, col))
                pos += 1
                col += 1
                continue

            matched_group = match.lastgroup
            token_type = GROUP_TO_TYPE[matched_group]
            token_value = match.group(matched_group)

            tok = Token(token_type, token_value, line, col)
            tokens.append(tok)

            # Cập nhật line và col
            if token_type == TokenType.NEWLINE:
                line += 1
                col = 1
            elif token_type in (TokenType.COMMENT_MULTI, TokenType.STRING):
                num_newlines = token_value.count('\n')
                if num_newlines > 0:
                    line += num_newlines
                    last_nl = token_value.rfind('\n')
                    col = len(token_value) - last_nl
                else:
                    col += len(token_value)
            else:
                col += len(token_value)

            pos = match.end()

        tokens.append(Token(TokenType.EOF, "", line, col))
        return tokens
