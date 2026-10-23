#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mpp.py - Giao diện dòng lệnh (CLI) chính của ngôn ngữ M++
Cú pháp:
    mpp chay file.m++ [--cuoi] [tham so truyen vao chuong trinh...]
    mpp dich file.m++ [-o file_xuat.cpp]
    mpp tro_giup / mpp --help
"""
import sys
import os
import argparse

# Thiết lập UTF-8 cho terminal để hiển thị tiếng Việt mượt mà
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.transpiler import Transpiler
from src.compiler import Compiler
from src.jokes import lay_truyen_cuoi_ngau_nhien

# Màu sắc ANSI cho terminal thêm phần sinh động
MAU_DO = "\033[91m"
MAU_XANH_LA = "\033[92m"
MAU_VANG = "\033[93m"
MAU_XANH_DUONG = "\033[96m"
MAU_DAM = "\033[1m"
MAU_RESET = "\033[0m"

BANNER = f"""{MAU_XANH_DUONG}{MAU_DAM}
======================================================================
  __  __     _     _ 
 |  \\/  |   | |   | |
 | \\  / |___| |___| |     NGÔN NGỮ LẬP TRÌNH M++ (Troll++ Edition)
 | |\\/| |___| |___| |     "Cú pháp tấu hài - Tốc độ bàn thờ của C++"
 |_|  |_|   |_|   |_|     Phiên bản 1.0.0
======================================================================{MAU_RESET}"""

def in_canh_bao(msg: str):
    print(f"{MAU_VANG}{MAU_DAM}{msg}{MAU_RESET}")

def in_loi(msg: str):
    print(f"{MAU_DO}{MAU_DAM}{msg}{MAU_RESET}")

def in_thanh_cong(msg: str):
    print(f"{MAU_XANH_LA}{MAU_DAM}{msg}{MAU_RESET}")

def in_banner_cuoi():
    joke = lay_truyen_cuoi_ngau_nhien()
    print(f"\n{MAU_CYAN if 'MAU_CYAN' in globals() else MAU_XANH_DUONG}{'='*60}")
    print(f"🤣 [ GÓC HÀI HƯỚC M++ ]:")
    print(f"   {joke}")
    print(f"{'='*60}{MAU_RESET}\n")

def huong_dan_su_dung():
    print(BANNER)
    print(f"""
{MAU_DAM}CÁCH DÙNG:{MAU_RESET}
    {MAU_XANH_LA}mpp chay <file.m++> [--cuoi] [tham_so...]{MAU_RESET}
        -> Dịch sang C++, biên dịch bằng g++ và chạy ngay lập tức.
        -> Thêm cờ {MAU_VANG}--cuoi{MAU_RESET} để đọc một mẩu truyện cười sau khi chạy xong.

    {MAU_XANH_LA}mpp dich <file.m++> [-o <file.cpp>]{MAU_RESET}
        -> Chỉ dịch file .m++ sang mã nguồn C++ hợp lệ (.cpp).

    {MAU_XANH_LA}mpp tro_giup{MAU_RESET} hoặc {MAU_XANH_LA}mpp --help{MAU_RESET}
        -> Xem lại bảng hướng dẫn xịn sò này.

{MAU_DAM}VÍ DỤ NHANH:{MAU_RESET}
    mpp chay vi_du/01_hello.m++
    mpp chay vi_du/02_tinh_tong.m++ --cuoi
    mpp dich vi_du/01_hello.m++ -o hello.cpp
""")

def xu_ly_dich(filepath: str, output_path: str = None) -> bool:
    if not os.path.exists(filepath):
        in_loi(f"❌ [LỖI]: Ủa kiếm mòn con mắt không thấy file '{filepath}' đâu hết trơn! Có gõ nhầm tên không đó đại ca?")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    transpiler = Transpiler()
    result = transpiler.transpile(source_code)

    # In các cảnh báo / Easter egg
    for warning in result.warnings:
        in_canh_bao(f"⚠️  {warning}")

    # Nếu có lỗi cú pháp
    if not result.is_success:
        in_loi(f"\n🚫 [ỐI GIỜI ƠI! LỖI CÚ PHÁP RỒI]:")
        for err in result.errors:
            in_loi(f"   👉 {err}")
        return False

    # Xác định đường dẫn file C++ xuất ra
    if not output_path:
        base, _ = os.path.splitext(filepath)
        output_path = base + ".cpp"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.cpp_code)

    in_thanh_cong(f"✨ [THÀNH CÔNG]: Dịch xong xuôi mượt mà rồi nha đại ca!")
    print(f"   📁 File nguồn: {filepath}")
    print(f"   📄 File đích  : {output_path}")
    print(f"   📊 Thống kê   : {result.stats.get('transformed_keywords', 0)} từ khóa troll đã hóa thân thành C++ chuẩn chỉ!")
    return True

def xu_ly_chay(filepath: str, co_cuoi: bool = False, extra_args: list = None) -> int:
    if not os.path.exists(filepath):
        in_loi(f"❌ [LỖI]: Ủa kiếm mòn con mắt không thấy file '{filepath}' đâu hết trơn! Có gõ nhầm tên không đó đại ca?")
        return 1

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    transpiler = Transpiler()
    result = transpiler.transpile(source_code)

    # In cảnh báo / Easter eggs
    for warning in result.warnings:
        in_canh_bao(f"⚠️  {warning}")

    if not result.is_success:
        in_loi(f"\n🚫 [ỐI GIỜI ƠI! LỖI CÚ PHÁP RỒI]:")
        for err in result.errors:
            in_loi(f"   👉 {err}")
        return 1

    # Tạo file cpp và exe cùng thư mục hoặc trong thư mục build
    base, _ = os.path.splitext(filepath)
    cpp_path = base + ".cpp"
    exe_name = base + (".exe" if sys.platform == "win32" else "")

    with open(cpp_path, "w", encoding="utf-8") as f:
        f.write(result.cpp_code)

    compiler = Compiler()
    success, funny_errors, raw_stderr = compiler.compile(cpp_path, exe_name)

    if not success:
        in_loi(f"\n💥 [G++ TỨC GIẬN CHỬI BỚI]:")
        for fe in funny_errors:
            in_loi(f"   👉 {fe}")
        return 1

    # Chạy chương trình
    exit_code = compiler.run(exe_name, extra_args)

    # Nếu có cờ --cuoi thì in truyện cười
    if co_cuoi:
        in_banner_cuoi()

    return exit_code

def main():
    if len(sys.argv) < 2:
        huong_dan_su_dung()
        sys.exit(0)

    lenh = sys.argv[1].lower()

    if lenh in ("tro_giup", "--help", "-h", "help"):
        huong_dan_su_dung()
        sys.exit(0)

    if lenh == "dich":
        if len(sys.argv) < 3:
            in_loi("❌ Thiếu tên file .m++ cần dịch rồi má ơi! Ví dụ: mpp dich code.m++")
            sys.exit(1)
        
        filepath = sys.argv[2]
        output_path = None
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv):
                output_path = sys.argv[idx + 1]

        success = xu_ly_dich(filepath, output_path)
        sys.exit(0 if success else 1)

    elif lenh == "chay":
        if len(sys.argv) < 3:
            in_loi("❌ Thiếu tên file .m++ cần chạy rồi má ơi! Ví dụ: mpp chay code.m++")
            sys.exit(1)

        filepath = sys.argv[2]
        co_cuoi = False
        extra_args = []

        # Tách cờ --cuoi và các đối số truyền vào chương trình
        for arg in sys.argv[3:]:
            if arg == "--cuoi":
                co_cuoi = True
            else:
                extra_args.append(arg)

        code = xu_ly_chay(filepath, co_cuoi, extra_args)
        sys.exit(code)

    else:
        in_loi(f"❌ Lệnh lạ lẫm vậy ba: '{lenh}'. Gõ 'mpp tro_giup' để xem hướng dẫn nha!")
        sys.exit(1)

if __name__ == "__main__":
    main()
