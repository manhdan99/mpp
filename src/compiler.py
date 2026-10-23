# -*- coding: utf-8 -*-
"""
compiler.py - Trình biên dịch và thông dịch chạy C++
Gọi g++ để biên dịch mã C++, dịch lỗi sang phong cách tấu hài M++, và chạy file exe
"""
import os
import re
import subprocess
import sys
from typing import Tuple, List, Optional
from src.jokes import GXX_ERROR_PATTERNS

class Compiler:
    def __init__(self, gxx_cmd: str = "g++"):
        self.gxx_cmd = gxx_cmd

    def check_gxx(self) -> bool:
        """Kiểm tra xem g++ có sẵn trên hệ thống không"""
        try:
            res = subprocess.run([self.gxx_cmd, "--version"], capture_output=True, text=True, check=False)
            return res.returncode == 0
        except FileNotFoundError:
            return False

    def translate_gxx_errors(self, stderr_output: str, source_filename: str = "") -> List[str]:
        """
        Dịch các lỗi khô khan của g++ sang ngôn ngữ chửi yêu hài hước của M++
        """
        funny_errors = []
        error_regex = re.compile(r'^(?:[^\n:]+):(\d+):(?:\d+)?:?\s*(?:fatal\s+)?error:\s*(.+)$', re.MULTILINE)

        matches = error_regex.findall(stderr_output)
        if not matches:
            # Nếu không bắt được regex cụ thể nhưng có lỗi
            if stderr_output.strip():
                funny_errors.append(f"G++ kêu réo nè đại ca ơi:\n{stderr_output.strip()}")
            return funny_errors

        for line_str, raw_msg in matches:
            line = int(line_str)
            translated = False

            for pattern, template in GXX_ERROR_PATTERNS:
                m = re.search(pattern, raw_msg)
                if m:
                    groups = m.groups()
                    params = {"line": line}
                    for idx, g in enumerate(groups, 1):
                        params[f"param{idx}"] = g
                    
                    try:
                        msg = template.format(**params)
                    except Exception:
                        msg = f"Dòng {line}: {template}"
                    funny_errors.append(msg)
                    translated = True
                    break

            if not translated:
                funny_errors.append(f"Dòng {line}: g++ nó chửi nè đại ca: '{raw_msg.strip()}'. Coi sửa lẹ kẻo nó giận!")

        return funny_errors

    def compile(self, cpp_path: str, exe_path: str) -> Tuple[bool, List[str], str]:
        """
        Biên dịch file C++ thành file exe
        Trả về (thành công, danh sách lỗi hài hước, stderr gốc)
        """
        if not self.check_gxx():
            return False, ["Không tìm thấy trình biên dịch 'g++' trên máy! Cài g++ vô rồi hẵng chơi M++ nhe má!"], ""

        cmd = [self.gxx_cmd, "-std=c++17", "-O2", cpp_path, "-o", exe_path]
        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if process.returncode == 0:
                return True, [], ""
            else:
                funny_errors = self.translate_gxx_errors(process.stderr, cpp_path)
                return False, funny_errors, process.stderr
        except Exception as e:
            return False, [f"Lỗi hệ thống khi gọi g++: {str(e)}"], str(e)

    def run(self, exe_path: str, args: Optional[List[str]] = None) -> int:
        """
        Chạy file exe đã biên dịch
        """
        if args is None:
            args = []
        full_cmd = [exe_path] + args
        try:
            # Chạy trực tiếp và chuyển tiếp stdio để tương tác được cin/cout
            proc = subprocess.run(full_cmd)
            return proc.returncode
        except Exception as e:
            print(f"\n[LỖI CHẠY CHƯƠNG TRÌNH]: {e}", file=sys.stderr)
            return 1
