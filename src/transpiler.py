# -*- coding: utf-8 -*-
"""
transpiler.py - Trình chuyển mã (Transpiler) từ M++ sang C++
Chịu trách nhiệm:
1. Nạp từ điển ánh xạ tu_dien.json
2. Phân tích token và dịch sang C++ chuẩn
3. Kiểm tra các Easter Eggs troll hài hước
4. Báo lỗi cú pháp bằng giọng hài
"""
import json
import os
from typing import List, Tuple, Dict, Any, Optional
from src.tokenizer import Tokenizer, Token, TokenType

class TranspileResult:
    def __init__(self, cpp_code: str, warnings: List[str], errors: List[str], stats: Dict[str, Any]):
        self.cpp_code = cpp_code
        self.warnings = warnings
        self.errors = errors
        self.stats = stats

    @property
    def is_success(self) -> bool:
        return len(self.errors) == 0

class Transpiler:
    def __init__(self, dictionary_path: Optional[str] = None):
        if dictionary_path is None:
            # Mặc định lấy tu_dien.json cùng thư mục gốc dự án
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dictionary_path = os.path.join(base_dir, "tu_dien.json")

        self.dictionary_path = dictionary_path
        self.keywords: Dict[str, str] = {}
        self.type_keywords: set = set()
        self.statement_suffixes: set = set()
        self._load_dictionary()

    def _load_dictionary(self):
        if not os.path.exists(self.dictionary_path):
            raise FileNotFoundError(f"Ủa kiếm hổng ra file từ điển: {self.dictionary_path}")

        with open(self.dictionary_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.keywords = data.get("tu_khoa", {})
        self.type_keywords = set(data.get("tu_khoa_kieu_du_lieu", []))
        self.statement_suffixes = set(data.get("duoi_cau_lenh", ["nhe", "ha"]))

    def check_syntax_and_easter_eggs(self, tokens: List[Token]) -> Tuple[List[str], List[str]]:
        """
        Kiểm tra cú pháp cơ bản và kích hoạt các tính năng troll (Easter Eggs):
        1. Easter egg: không có dòng hihi nào -> 'Code gì mà câm như hến vậy trời'
        2. Easter egg: biến dut_bo không phải kiểu ký tự (char) -> cảnh báo
        3. Cú pháp: ngoặc đóng mở không khớp, thiếu tran_dau (main)
        """
        warnings = []
        errors = []

        # 1. Kiểm tra số lần xuất hiện của 'hihi' (cout)
        hihi_count = sum(1 for tok in tokens if tok.type == TokenType.IDENTIFIER and tok.value == "hihi")
        if hihi_count == 0:
            warnings.append("[M++ LỜI NHẮC YÊU THƯƠNG]: Code gì mà câm như hến vậy trời! (Không thấy một câu lệnh 'hihi' nào hết á!)")

        # 2. Kiểm tra có hàm 'tran_dau' (main) hay không
        has_main = any(tok.type == TokenType.IDENTIFIER and tok.value in ("tran_dau", "main") for tok in tokens)
        if not has_main:
            errors.append("Ủa alo? File code không có hàm 'tran_dau()' (main) kìa má! Không có trận đấu thì ai đá ai coi trời?")

        # 3. Kiểm tra cặp dấu ngoặc: (), {}, []
        bracket_stack = []
        bracket_pairs = {')': '(', '}': '{', ']': '['}
        bracket_names = {'(': "tròn '()'", '{': "nhọn '{}'", '[': "vuông '[]'"}

        for tok in tokens:
            if tok.type == TokenType.PUNCTUATION:
                if tok.value in ('(', '{', '['):
                    bracket_stack.append(tok)
                elif tok.value in (')', '}', ']'):
                    expected_open = bracket_pairs[tok.value]
                    if not bracket_stack:
                        errors.append(f"Dòng {tok.line}: Dấu đóng ngoặc '{tok.value}' thừa thãi ở đâu nhảy ra vậy má?")
                    else:
                        top = bracket_stack.pop()
                        if top.value != expected_open:
                            errors.append(
                                f"Dòng {tok.line}: Đóng ngoặc '{tok.value}' nhưng trước đó mở ngoặc '{top.value}' ở dòng {top.line}! Râu ông nọ cắm cằm bà kia kìa!"
                            )

        while bracket_stack:
            unclosed = bracket_stack.pop()
            bname = bracket_names.get(unclosed.value, unclosed.value)
            if unclosed.value == '{':
                errors.append(f"Dòng {unclosed.line}: Mở ngoặc {bname} mà hổng đóng nè má! Tính để gió lùa vô nhà lạnh chết hả?")
            else:
                errors.append(f"Dòng {unclosed.line}: Mở ngoặc {bname} cô đơn quá chưa thấy ai đóng lại nè má!")

        # 4. Kiểm tra Easter Egg: biến tên 'dut_bo'
        # Quét các token: nếu gặp kiểu dữ liệu (thuộc type_keywords),
        # theo sau là biến tên 'dut_bo'
        dut_bo_declared = False
        non_whitespace_tokens = [tok for tok in tokens if tok.type not in (TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.COMMENT_SINGLE, TokenType.COMMENT_MULTI, TokenType.COMMENT_KE_CHUYEN)]
        for i in range(len(non_whitespace_tokens) - 1):
            tok = non_whitespace_tokens[i]
            if tok.type == TokenType.IDENTIFIER and tok.value in self.type_keywords:
                # Xem token tiếp theo có phải con trỏ hoặc tên biến 'dut_bo' không
                j = i + 1
                while j < len(non_whitespace_tokens) and non_whitespace_tokens[j].value in ('*', '&', 'const', 'khongdoi'):
                    j += 1
                if j < len(non_whitespace_tokens):
                    next_tok = non_whitespace_tokens[j]
                    if next_tok.type == TokenType.IDENTIFIER and next_tok.value == "dut_bo":
                        dut_bo_declared = True
                        if tok.value != "dut_bo":
                            warnings.append(
                                f"[M++ CẢNH BÁO] (Dòng {next_tok.line}): Ủa kỳ vậy, dut_bo mà không phải char hả? Đặt tên biến kiểu này coi chừng đút bò thật nha!"
                            )

        return warnings, errors, dut_bo_declared

    def transpile(self, source_code: str) -> TranspileResult:
        """
        Dịch toàn bộ mã nguồn M++ sang C++
        """
        if not source_code.strip():
            return TranspileResult("", [], ["File trống trơn như túi tiền cuối tháng vậy trời! Viết thêm vài dòng đi má!"], {})

        tokenizer = Tokenizer(source_code)
        tokens = tokenizer.tokenize()

        warnings, errors, dut_bo_declared = self.check_syntax_and_easter_eggs(tokens)
        if errors:
            return TranspileResult("", warnings, errors, {"total_tokens": len(tokens)})

        output_parts: List[str] = []
        n = len(tokens)
        i = 0
        transformed_keywords_count = 0

        while i < n:
            tok = tokens[i]

            # 1. Xử lý comment đặc biệt 'ke_chuyen: ...' -> dịch thành '// ke_chuyen: ...'
            if tok.type == TokenType.COMMENT_KE_CHUYEN:
                output_parts.append("// " + tok.value)
                i += 1
                continue

            # 2. Xử lý String & Char -> GIỮ NGUYÊN 100%, không bao giờ thay thế từ khóa bên trong!
            if tok.type in (TokenType.STRING, TokenType.CHAR, TokenType.COMMENT_SINGLE, TokenType.COMMENT_MULTI):
                output_parts.append(tok.value)
                i += 1
                continue

            # 3. Xử lý '#' theo sau là 'keu_ban' (ví dụ: #keu_ban <iostream>)
            if tok.type == TokenType.PUNCTUATION and tok.value == "#":
                # Nhìn trước xem token tiếp theo có phải keu_ban không
                j = i + 1
                while j < n and tokens[j].type == TokenType.WHITESPACE:
                    j += 1
                if j < n and tokens[j].type == TokenType.IDENTIFIER and tokens[j].value == "keu_ban":
                    output_parts.append("#include")
                    transformed_keywords_count += 1
                    i = j + 1
                    continue
                else:
                    output_parts.append(tok.value)
                    i += 1
                    continue

            # 4. Xử lý đuôi câu lệnh hài hước 'nhe;' hoặc 'ha;' (hoặc 'nhe ;', 'ha ;')
            if tok.type == TokenType.IDENTIFIER and tok.value in self.statement_suffixes:
                # Kiểm tra token kế tiếp (bỏ qua khoảng trắng) xem có phải là ';' không
                j = i + 1
                while j < n and tokens[j].type == TokenType.WHITESPACE:
                    j += 1
                if j < n and tokens[j].type == TokenType.PUNCTUATION and tokens[j].value == ";":
                    # Xóa khoảng trắng thừa ngay trước từ 'nhe'/'ha' nếu có
                    if output_parts and output_parts[-1].isspace():
                        output_parts.pop()
                    i = j  # nhảy tới dấu ';'
                    continue

            # 5. Xử lý từ khóa M++ -> C++
            if tok.type == TokenType.IDENTIFIER:
                val = tok.value

                # Trường hợp đặc biệt: 'dut_bo' có thể là kiểu dữ liệu (char) hoặc tên biến!
                # Nếu người dùng đặt tên biến là 'dut_bo' (ví dụ: manh dut_bo = 10; hoặc dut_bo dut_bo = 'A';)
                if val == "dut_bo":
                    # Kiểm tra xem token này là TYPE hay là TÊN BIẾN
                    # 1. Nếu đứng sau một kiểu dữ liệu -> Đây là TÊN BIẾN!
                    prev_non_ws = None
                    for k in range(len(output_parts) - 1, -1, -1):
                        p = output_parts[k].strip()
                        if p:
                            prev_non_ws = p
                            break
                    
                    # 2. Kiểm tra token kế tiếp
                    next_non_ws_tok = None
                    for k in range(i + 1, n):
                        if tokens[k].type not in (TokenType.WHITESPACE, TokenType.NEWLINE):
                            next_non_ws_tok = tokens[k]
                            break

                    is_var = False
                    if prev_non_ws in ("int", "float", "double", "char", "string", "bool", "void", "vector", "*", "&"):
                        is_var = True
                    elif dut_bo_declared and next_non_ws_tok and next_non_ws_tok.value in ("=", ";", ",", ")", "]", "++", "--", "<<", ">>", "+", "-", "*", "/", "%", "==", "!="):
                        is_var = True

                    if is_var:
                        output_parts.append("dut_bo")
                        i += 1
                        continue

                if val in self.keywords:
                    replacement = self.keywords[val]
                    output_parts.append(replacement)
                    transformed_keywords_count += 1
                else:
                    output_parts.append(val)
                i += 1
                continue

            # Các token khác (toán tử, số, dấu câu, xuống dòng, khoảng trắng) giữ nguyên
            output_parts.append(tok.value)
            i += 1

        cpp_code = "".join(output_parts)

        stats = {
            "total_tokens": len(tokens),
            "transformed_keywords": transformed_keywords_count,
            "lines": source_code.count('\n') + 1
        }

        return TranspileResult(cpp_code, warnings, errors, stats)
