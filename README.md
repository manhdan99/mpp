<p align="center">
  <img src="assets/banner.svg" alt="M++ Programming Language" width="100%" />
</p>

<p align="center">
  <a href="#-giới-thiệu"><img src="https://img.shields.io/badge/Language-M++-8b5cf6?style=for-the-badge&logo=codepen&logoColor=white" alt="M++" /></a>
  <a href="#-yêu-cầu-hệ-thống"><img src="https://img.shields.io/badge/Python-3.8%2B-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" /></a>
  <a href="#-yêu-cầu-hệ-thống"><img src="https://img.shields.io/badge/Compiler-C%2B%2B17%20%2F%20g%2B%2B-00599c?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++17" /></a>
  <a href="#-kiểm-thử-tự-động"><img src="https://img.shields.io/badge/Tests-13%2F13%20Passing-10b981?style=for-the-badge&logo=githubactions&logoColor=white" alt="Tests" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge" alt="License MIT" /></a>
  <a href="#-tính-năng-troll-độc-quyền"><img src="https://img.shields.io/badge/Troll%20Level-Over%209000-ec4899?style=for-the-badge&logo=target&logoColor=white" alt="Troll Level" /></a>
</p>

<h3 align="center">
  ⚡ Cú pháp tấu hài dân gian • Sức mạnh C++17 nguyên bản • Tốc độ bàn thờ ⚡
</h3>

<p align="center">
  <b>M++ (M-Plus-Plus)</b> là một ngôn ngữ lập trình độc đáo, kết hợp giữa tốc độ thực thi tối đa của C++ và văn hóa mạng hài hước của Việt Nam. Toàn bộ từ khóa, kiểu dữ liệu, hàm thư viện và cú pháp đều được "troll hóa" nhưng chạy thật 100% nhờ Transpiler chuẩn Lexer!
</p>

---

## 📑 Mục Lục
- [Kiến Trúc Hoạt Động](#-kiến-trúc-hoạt-động)
- [Tính Năng Nổi Bật](#-tính-năng-nổi-bật)
- [So Sánh C++ và M++](#-so-sánh-c-và-m)
- [Từ Điển Ánh Xạ M++](#-từ-điển-ánh-xạ-m)
- [Cài Đặt & Yêu Cầu](#-cài-đặt--yêu-cầu)
- [Cách Sử Dụng CLI](#-cách-sử-dụng-cli)
- [Kho Ví Dụ Mẫu](#-kho-ví-dụ-mẫu)
- [Kiểm Thử Tự Động](#-kiểm-thử-tự-động)
- [Đóng Góp](#-đóng-góp)
- [Giấy Phép](#-giấy-phép)

---

## 🏗 Kiến Trúc Hoạt Động

<p align="center">
  <img src="assets/architecture.svg" alt="M++ Architecture Flow" width="100%" />
</p>

1. **Phân tích từ vựng (Lexer Tokenizer)**: Quét luồng mã nguồn `.m++`, phân tách String literals, Char literals, Comment (`//`, `/* */`, `ke_chuyen:`), Number, Operator và Identifier.
2. **Bảo vệ tuyệt đối nội dung chuỗi**: Tokenizer cam kết **không bao giờ thay thế từ khóa** nằm trong chuỗi `""` hoặc comment.
3. **Bộ chuyển đổi ngữ nghĩa (Transpiler Core)**: Ánh xạ từ khóa theo `tu_dien.json`, chuẩn hóa đuôi câu lệnh `nhe;`/`ha;`, bắt các Easter eggs và kiểm tra cấu trúc ngoặc.
4. **Biên dịch & Tối ưu (g++ Compiler)**: Gọi `g++ -std=c++17 -O2` để sinh file nhị phân native thực thi trực tiếp với tốc độ tối đa.
5. **Chửi yêu khi có lỗi**: Tự động chuyển đổi các lỗi khô khan từ compiler thành thông báo tiếng Việt hài hước, chỉ rõ dòng lỗi.

---

## 🎭 Tính Năng Nổi Bật

| Tính Năng | Mô Tả Chi Tiết |
|---|---|
| **🛡️ Tokenizer Thực Thụ** | Không dùng regex replace thô. Thoải mái viết `chuoi_hihi s = "manh dan hihi nhe;";` mà không lo vỡ chuỗi. |
| **💬 Comment `ke_chuyen:`** | Thêm cú pháp comment dòng mới: `ke_chuyen: Hôm nay trời đẹp viết code...` trước khi vào hàm chính. |
| **🤙 Đuôi Câu Linh Hoạt** | Dấu chấm phẩy `;` vẫn chạy tốt, nhưng hỗ trợ thêm `nhe;` và `ha;` tạo cảm giác thân thiện khi code. |
| **🐔 Easter Egg "Câm Như Hến"** | Nếu chương trình không hề gọi lệnh xuất `hihi` (cout), trình biên dịch sẽ nhắc nhở yêu thương. |
| **🥊 Easter Egg "Mạnh Trùm"** | Khai báo biến `manhtrum` với kiểu khác `char` sẽ nhận cảnh báo vui nhộn từ hệ thống. |
| **🤣 Chế Độ `--cuoi`** | Sau khi chương trình kết thúc, tự động kể một câu chuyện cười giới lập trình viên. |
| **🤬 Báo Lỗi "Chửi Yêu"** | Lỗi thiếu chấm phẩy, quên đóng ngoặc hay biến lạ được dịch thành ngôn ngữ đời thường dí dỏm. |

---

## 🔄 So Sánh C++ và M++

```cpp
// ==================== C++ ====================
#include <iostream>
using namespace std;

int main() {
    cout << "Xin chao the gioi!" << endl;
    return 0;
}
```

```m++
// ==================== M++ ====================
keu_ban <iostream>
xai_chung;

manh tran_dau() {
    hihi << "Xin chao the gioi!" << xuongdong nhe;
    tra_ve_haha 0 ha;
}
```

---

## 📖 Từ Điển Ánh Xạ M++

Toàn bộ từ khóa được định nghĩa trong file cấu hình độc lập [`tu_dien.json`](tu_dien.json):

### 1. Kiểu dữ liệu & Từ khóa cơ bản
| C++ | M++ | Ý nghĩa / Cách đọc |
|---|---|---|
| `int` | `manh` | Số nguyên mạnh mẽ |
| `float` | `dan` | Số thực đàn em |
| `double` | `manhnguyen` | Số thực gấp đôi anh Mạnh |
| `char` | `manhtrum` | Ký tự của anh Mạnh trùm |
| `string` | `chuoi_hihi` | Chuỗi ký tự vui vẻ |
| `bool` | `dungsai` | Kiểu đúng sai |
| `void` | `trongtron` | Hàm trống trơn không trả về |
| `const` | `khongdoi` | Hằng số không bao giờ đổi |
| `true` | `chuan` | Chuẩn cơm mẹ nấu |
| `false` | `sai_roi` | Sai bét tè lè nhè |
| `nullptr` | `hu_vo` | Hư vô, vô ảnh |

### 2. Cấu trúc điều khiển & Vòng lặp
| C++ | M++ | Ý nghĩa / Cách đọc |
|---|---|---|
| `if` | `neuma` | Nếu mà như vầy |
| `else` | `khongthi` | Không thì như kia |
| `else if` | `khongthi_neuma` | Không thì nếu mà |
| `for` | `lapdi` | Lặp đi lặp lại |
| `while` | `lapmai` | Lặp mãi không ngừng |
| `do` | `lamdi` | Làm đi rồi tính tiếp |
| `switch` | `chonbua` | Chọn bừa một cái |
| `case` | `truonghop` | Trong trường hợp này |
| `break` | `thoi` | Thôi nghỉ, thoát ra |
| `continue` | `bolua` | Bỏ lụa qua vòng kế tiếp |
| `return` | `tra_ve_haha` | Trả về kết quả haha |

### 3. Hàm, Lớp & Đối tượng
| C++ | M++ | Ý nghĩa / Cách đọc |
|---|---|---|
| `main` | `tran_dau` | Trận đấu chính của chương trình |
| `class` | `bang_nhom` | Băng nhóm (Class) |
| `struct` | `cuc_cuc` | Cục dữ liệu gom lại (Struct) |
| `public` | `congkhai` | Ai cũng thấy |
| `private` | `bimat` | Giấu kín như bưng |
| `protected` | `giu_kin` | Giữ kín nội bộ |
| `new` | `de_moi` | Đẻ mới một đối tượng |
| `delete` | `xoa_sach` | Xóa sạch sẽ giải phóng RAM |

### 4. Vào / Ra & Thư viện chuẩn (Mở rộng)
| C++ | M++ | Ý nghĩa / Cách đọc |
|---|---|---|
| `cout` | `hihi` | Cười hì hì in ra màn hình |
| `cin` | `haha` | Cười ha ha hút dữ liệu vào |
| `endl` | `xuongdong` | Xuống dòng |
| `#include` | `keu_ban` | Kêu gọi thư viện bạn bè vào |
| `using namespace std` | `xai_chung` | Xài chung cả lò `std` |
| `vector` | `hang_dai` | Mảng động co giãn |
| `size()` | `bao_nhieu` | Đếm số phần tử |
| `push_back()` | `nhet_vao` | Nhét vào cuối mảng |
| `pop_back()` | `moc_ra` | Móc phần tử cuối ra |
| `sqrt()` | `can_bac_hai_ne` | Căn bậc hai |
| `swap()` | `doi_cho` | Đổi chỗ 2 phần tử |
| `sort()` | `xep_hang` | Bắt xếp hàng ngay ngắn |
| `min()` / `max()` | `nho_nhat` / `bu_nhat` | Nhỏ nhất / Bự nhất |
| `abs()` / `pow()` | `tuyet_doi_nha` / `mu_len` | Tuyệt đối / Lũy thừa |
| `begin()` / `end()` | `bat_dau` / `ket_thuc` | Con trỏ đầu / cuối mảng |

---

## 💻 Cài Đặt & Yêu Cầu

1. **Python 3.8+** (Khuyên dùng Python 3.10, 3.11 hoặc 3.12).
2. **Trình biên dịch C++** hỗ trợ C++17 trở lên (`g++` từ MinGW-w64, MSYS2, GCC trên Linux, hoặc Clang trên macOS).

Kiểm tra môi trường trong terminal:
```bash
python --version
g++ --version
```

Clone mã nguồn về máy:
```bash
git clone https://github.com/your-username/mpp.git
cd mpp
```

---

## ⚡ Cách Sử Dụng CLI

### 1. Dịch và Chạy Trực Tiếp
```bash
# Windows
.\mpp.bat chay vi_du/01_hello.m++

# Linux / macOS
./mpp chay vi_du/01_hello.m++

# Hoặc dùng python trực tiếp
python mpp.py chay vi_du/01_hello.m++
```

### 2. Kích Hoạt Chế Độ Thư Giãn (`--cuoi`)
```bash
.\mpp.bat chay vi_du/02_tinh_tong.m++ --cuoi
```

### 3. Chỉ Dịch Sang File C++ Hợp Lệ
```bash
# Tự động xuất vi_du/01_hello.cpp
.\mpp.bat dich vi_du/01_hello.m++

# Hoặc chỉ định tên file mong muốn
.\mpp.bat dich vi_du/01_hello.m++ -o hello.cpp
```

### 4. Xem Trợ Giúp
```bash
.\mpp.bat tro_giup
```

---

## 📂 Kho Ví Dụ Mẫu

Thư mục [`vi_du/`](vi_du/) chứa 7 chương trình mẫu từ cơ bản đến nâng cao:

| File | Mô Tả | Điểm Nhấn Cú Pháp |
|---|---|---|
| [`01_hello.m++`](vi_du/01_hello.m++) | Hello World | `keu_ban`, `xai_chung`, `hihi`, `nhe;`, `ha;` |
| [`02_tinh_tong.m++`](vi_du/02_tinh_tong.m++) | Tính tổng 1..N | `lapdi`, `neuma`, `khongthi`, `tra_ve_haha` |
| [`03_giai_thua.m++`](vi_du/03_giai_thua.m++) | Tính giai thừa | Đệ quy, vòng lặp `lapmai`, `dai_thoong` |
| [`04_so_nguyen_to.m++`](vi_du/04_so_nguyen_to.m++) | Sàng lọc số nguyên tố | `can_bac_hai_ne`, `dungsai`, `chuan`, `bolua`, `thoi` |
| [`05_sap_xep_mang.m++`](vi_du/05_sap_xep_mang.m++) | Sắp xếp mảng / vector | `hang_dai`, `nhet_vao`, `doi_cho`, `xep_hang`, `bat_dau` |
| [`06_oop_bang_nhom.m++`](vi_du/06_oop_bang_nhom.m++) | Hướng đối tượng OOP | `bang_nhom`, `cuc_cuc`, `congkhai`, `bimat`, `de_moi`, `xoa_sach` |
| [`07_test_troll.m++`](vi_du/07_test_troll.m++) | Kiểm tra bảo vệ chuỗi | Biến `manhtrum` kích hoạt cảnh báo, chuỗi giữ nguyên từ khóa |

---

## 🧪 Kiểm Thử Tự Động

M++ đi kèm bộ test tự động kiểm thử toàn diện 13 kịch bản:

```bash
python -m unittest tests/test_mpp.py -v
```

```
test_easter_egg_cam_nhu_hen ... ok
test_easter_egg_manhtrum_not_char ... ok
test_jokes_generation ... ok
test_ke_chuyen_comment ... ok
test_manhtrum_as_char_no_warning ... ok
test_run_all_samples ... ok
test_syntax_endings_nhe_and_ha ... ok
test_syntax_error_missing_main ... ok
test_syntax_error_unclosed_brace ... ok
test_tokenizer_preserves_comments ... ok
test_tokenizer_preserves_escaped_strings ... ok
test_tokenizer_preserves_strings ... ok
test_tu_dien_json ... ok

----------------------------------------------------------------------
Ran 13 tests in 4.6s

OK (100% Passed)
```

---

## 🤝 Đóng Góp

Mọi đóng góp từ cộng đồng đều được chào đón nồng nhiệt!
1. Fork dự án
2. Tạo nhánh tính năng (`git checkout -b feature/tu-khoa-moi`)
3. Thêm từ khóa vào [`tu_dien.json`](tu_dien.json)
4. Viết test trong [`tests/test_mpp.py`](tests/test_mpp.py)
5. Mở Pull Request để cùng tấu hài!

---

## 📜 Giấy Phép

Phát hành dưới giấy phép [MIT License](LICENSE). Tự do học tập, sửa đổi, chia sẻ và lan tỏa tiếng cười!
