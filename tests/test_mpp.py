# -*- coding: utf-8 -*-
"""
test_mpp.py - Bộ kiểm thử tự động toàn diện cho ngôn ngữ M++
Kiểm tra:
1. Tokenizer bảo toàn nguyên vẹn từ khóa trong chuỗi và comment.
2. Dịch chuẩn các từ khóa M++ sang C++.
3. Cú pháp kết thúc câu nhe; và ha;
4. Easter egg: không có hihi -> Câm như hến.
5. Easter egg: cha không phải char -> Cảnh báo vui.
6. Xử lý comment ke_chuyen:
7. Dịch, biên dịch và chạy thật toàn bộ các chương trình mẫu.
"""
import unittest
import os
import subprocess
import sys
import json

# Thêm thư mục gốc vào sys.path để import
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.tokenizer import Tokenizer, TokenType
from src.transpiler import Transpiler
from src.compiler import Compiler
from src.jokes import lay_truyen_cuoi_ngau_nhien, DANH_SACH_TRUYEN_CUOI

class TestMPlusPlus(unittest.TestCase):
    def setUp(self):
        self.transpiler = Transpiler()
        self.compiler = Compiler()

    def test_tu_dien_json(self):
        """Kiểm tra file từ điển: đầy đủ từ khóa bắt buộc và hơn 20 từ khóa mở rộng"""
        dict_path = os.path.join(BASE_DIR, "tu_dien.json")
        self.assertTrue(os.path.exists(dict_path), "File tu_dien.json không tồn tại!")
        
        with open(dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        tu_khoa = data.get("tu_khoa", {})
        
        # Các từ khóa tối thiểu theo yêu cầu đề bài
        bat_buoc = [
            "nguyen_con", "troi_noi", "gap_doi", "cha", "chuoi_hihi", "dungsai",
            "trongtron", "neuma", "khongthi", "khongthi_neuma", "lapdi",
            "lapmai", "lamdi", "chonbua", "truonghop", "thoi", "bolua",
            "tra_ve_haha", "chuan", "sai_roi", "bang_nhom", "cuc_cuc",
            "congkhai", "bimat", "khongdoi", "de_moi", "xoa_sach", "tran_dau",
            "hihi", "haha", "xuongdong", "keu_ban", "xai_chung"
        ]
        for kw in bat_buoc:
            self.assertIn(kw, tu_khoa, f"Từ khóa bắt buộc '{kw}' bị thiếu trong từ điển!")

        # Kiểm tra tối thiểu 20 từ khóa sáng tạo thêm (tổng cộng ít nhất 33 + 20 = 53)
        self.assertGreaterEqual(len(tu_khoa), 53, "Cần tối thiểu 20 từ khóa mở rộng sáng tạo!")

    def test_tokenizer_preserves_strings(self):
        """Kiểm tra tokenizer TUYỆT ĐỐI KHÔNG thay thế từ khóa nằm trong String"""
        code = 'chuoi_hihi s = "nguyen_con troi_noi gap_doi tran_dau hihi haha nhe; xai_chung";'
        res = self.transpiler.transpile(f"nguyen_con tran_dau() {{ {code} tra_ve_haha 0; }}")
        
        expected_str = '"nguyen_con troi_noi gap_doi tran_dau hihi haha nhe; xai_chung"'
        self.assertIn(expected_str, res.cpp_code, "Từ khóa trong chuỗi đã bị thay thế sai trái!")

    def test_tokenizer_preserves_escaped_strings(self):
        """Kiểm tra chuỗi chứa dấu nháy kép escape: \\\" """
        code = r'chuoi_hihi s = "Day la \"nguyen_con\" va \"tran_dau\" nhe;";'
        res = self.transpiler.transpile(f"nguyen_con tran_dau() {{ {code} hihi << s; tra_ve_haha 0; }}")
        self.assertIn(r'"Day la \"nguyen_con\" va \"tran_dau\" nhe;"', res.cpp_code)

    def test_tokenizer_preserves_comments(self):
        """Kiểm tra từ khóa trong comment không bị dịch"""
        code = """
        // nguyen_con tran_dau hihi nhe;
        /* troi_noi chuoi_hihi xai_chung */
        nguyen_con tran_dau() {
            hihi << "ok";
            tra_ve_haha 0;
        }
        """
        res = self.transpiler.transpile(code)
        self.assertIn("// nguyen_con tran_dau hihi nhe;", res.cpp_code)
        self.assertIn("/* troi_noi chuoi_hihi xai_chung */", res.cpp_code)

    def test_ke_chuyen_comment(self):
        """Kiểm tra comment kiểu ke_chuyen: ... được chuyển thành // ke_chuyen: ..."""
        code = """
        ke_chuyen: Ngay xua co nguoi code M++ rat vui tran_dau
        nguyen_con tran_dau() {
            hihi << 1;
            tra_ve_haha 0;
        }
        """
        res = self.transpiler.transpile(code)
        self.assertIn("// ke_chuyen: Ngay xua co nguoi code M++ rat vui tran_dau", res.cpp_code)

    def test_syntax_endings_nhe_and_ha(self):
        """Kiểm tra cú pháp kết thúc câu lệnh bằng nhe; và ha;"""
        code = """
        nguyen_con tran_dau() {
            nguyen_con a = 10 nhe;
            nguyen_con b = 20 ha;
            hihi << (a + b) nhe;
            tra_ve_haha 0 ha;
        }
        """
        res = self.transpiler.transpile(code)
        self.assertTrue(res.is_success)
        self.assertIn("int a = 10;", res.cpp_code)
        self.assertIn("int b = 20;", res.cpp_code)
        self.assertIn("cout << (a + b);", res.cpp_code)
        self.assertIn("return 0;", res.cpp_code)

    def test_easter_egg_cam_nhu_hen(self):
        """Easter Egg 1: Nếu không có dòng hihi nào, cảnh báo 'Code gì mà câm như hến vậy trời'"""
        code = """
        nguyen_con tran_dau() {
            nguyen_con a = 10 nhe;
            tra_ve_haha a;
        }
        """
        res = self.transpiler.transpile(code)
        found_warning = any("Code gì mà câm như hến vậy trời" in w for w in res.warnings)
        self.assertTrue(found_warning, "Chưa kích hoạt Easter egg câm như hến!")

    def test_easter_egg_cha_not_char(self):
        """Easter Egg 2: Nếu biến cha kiểu không phải ký tự -> Cảnh báo vui"""
        code = """
        nguyen_con tran_dau() {
            nguyen_con cha = 100 nhe;
            hihi << cha;
            tra_ve_haha 0;
        }
        """
        res = self.transpiler.transpile(code)
        found_warning = any("Tính làm cha thiên hạ hay gì?" in w for w in res.warnings)
        self.assertTrue(found_warning, "Chưa kích hoạt Easter egg cha không phải char!")

    def test_cha_as_char_no_warning(self):
        """Nếu biến cha có kiểu là cha (char) -> KHÔNG cảnh báo"""
        code = """
        nguyen_con tran_dau() {
            cha cha = 'A' nhe;
            hihi << cha;
            tra_ve_haha 0;
        }
        """
        res = self.transpiler.transpile(code)
        found_warning = any("Tính làm cha thiên hạ hay gì?" in w for w in res.warnings)
        self.assertFalse(found_warning, "Lẽ ra không được cảnh báo khi cha là char!")

    def test_syntax_error_missing_main(self):
        """Báo lỗi hài khi thiếu hàm tran_dau (main)"""
        code = """
        nguyen_con cong(nguyen_con a, nguyen_con b) {
            tra_ve_haha a + b;
        }
        """
        res = self.transpiler.transpile(code)
        self.assertFalse(res.is_success)
        found_err = any("tran_dau" in e for e in res.errors)
        self.assertTrue(found_err, "Chưa báo lỗi thiếu hàm tran_dau!")

    def test_syntax_error_unclosed_brace(self):
        """Báo lỗi hài khi mở ngoặc nhọn mà không đóng"""
        code = """
        nguyen_con tran_dau() {
            hihi << 1;
        """
        res = self.transpiler.transpile(code)
        self.assertFalse(res.is_success)
        found_err = any("Mở ngoặc nhọn" in e or "lạnh chết" in e for e in res.errors)
        self.assertTrue(found_err, "Chưa báo lỗi quên đóng ngoặc nhọn!")

    def test_jokes_generation(self):
        """Kiểm tra hàm lấy truyện cười cho cờ --cuoi"""
        joke = lay_truyen_cuoi_ngau_nhien()
        self.assertIn(joke, DANH_SACH_TRUYEN_CUOI)

    def test_run_all_samples(self):
        """Biên dịch và chạy thật tất cả các file ví dụ trong thư mục vi_du"""
        vi_du_dir = os.path.join(BASE_DIR, "vi_du")
        files = [f for f in os.listdir(vi_du_dir) if f.endswith(".m++")]
        self.assertGreaterEqual(len(files), 5, "Cần có ít nhất 5 file ví dụ!")

        for fname in sorted(files):
            fpath = os.path.join(vi_du_dir, fname)
            with self.subTest(sample_file=fname):
                with open(fpath, "r", encoding="utf-8") as f:
                    code = f.read()
                
                res = self.transpiler.transpile(code)
                self.assertTrue(res.is_success, f"Dịch thất bại file {fname}: {res.errors}")

                base, _ = os.path.splitext(fpath)
                cpp_file = base + ".cpp"
                exe_file = base + (".exe" if sys.platform == "win32" else "")

                with open(cpp_file, "w", encoding="utf-8") as f:
                    f.write(res.cpp_code)

                ok, funny_errs, raw_err = self.compiler.compile(cpp_file, exe_file)
                self.assertTrue(ok, f"Compile thất bại file {fname}: {funny_errs} / {raw_err}")

                exit_code = self.compiler.run(exe_file)
                self.assertEqual(exit_code, 0, f"Chạy file {fname} thất bại với mã lỗi {exit_code}")

                # Dọn dẹp file tạm sau khi test xong
                try:
                    if os.path.exists(cpp_file):
                        os.remove(cpp_file)
                    if os.path.exists(exe_file):
                        os.remove(exe_file)
                except Exception:
                    pass

if __name__ == "__main__":
    unittest.main()
