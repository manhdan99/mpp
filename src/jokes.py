# -*- coding: utf-8 -*-
"""
jokes.py - Bộ sưu tập truyện cười, câu đùa và từ điển chửi yêu của M++
"""
import random

# Danh sách câu đùa cho cờ --cuoi
DANH_SACH_TRUYEN_CUOI = [
    "Có 10 loại người trên thế giới: Người hiểu hệ nhị phân và người không hiểu gì hết.",
    "Lập trình viên không bao giờ chết, họ chỉ biến thành null pointer và trôi dạt vào cõi hư vô...",
    "Một tester bước vào quán bar: gọi 1 ly bia, 0 ly bia, 999999 ly bia, 1 con thằn lằn, -1 ly bia, 'asdfghj' ly bia... Quán vẫn ổn. Khách hàng thật bước vào hỏi toilet ở đâu, quán bar phát nổ!",
    "Bug không tự nhiên sinh ra, cũng không tự nhiên mất đi, nó chỉ chuyển từ tính năng này sang tính năng khác dưới dạng 'tính năng ngoài ý muốn'!",
    "Tại sao lập trình viên thích bóng tối? Vì ánh sáng thu hút con bọ (bug)!",
    "Hai biến x và y gặp nhau. x than thở: 'Tao cô đơn quá!', y bảo: 'Thì mày kiếm con trỏ mà trỏ vào tao nè!'",
    "Đi làm lập trình viên sợ nhất điều gì? Sợ code chạy mượt mà mà không hiểu tại sao nó chạy!",
    "Đời lập trình viên có 3 giai đoạn: 1. Code hổng chạy; 2. Code chạy nhưng không biết vì sao; 3. Code hổng chạy và cũng không biết vì sao!",
    "C++ nói với C: 'Mày không có đẳng cấp (class) gì cả!'. C cười khẩy: 'Nhưng tao chạy nhanh gấp đôi mày!'",
    "M++ là đỉnh cao trí tuệ loài người: C++ chạy nhanh, còn M++ vừa chạy nhanh vừa tấu hài đỉnh chóp!",
    "Bác sĩ bảo: 'Anh bị thiếu ngủ trầm trọng'. Dev đáp: 'Tại production nó thức thì sao em dám ngủ bác sĩ?'",
    "Thuật toán tìm kiếm người yêu: Độ phức tạp O(vô tận) - Chưa tìm thấy trường hợp cơ sở!",
    "Người ta yêu nhau từ cái nhìn đầu tiên. Còn lập trình viên yêu nhau sau khi giải quyết xong merge conflict!",
    "Code xong nhớ cúng nải chuối, không là tổ nghề C++ nửa đêm hiện về gõ đầu đó nha!",
    "Đừng bao giờ tin câu: 'Code này em test kỹ lắm rồi, cam kết không có bug!'"
]

def lay_truyen_cuoi_ngau_nhien():
    """Trả về một câu đùa ngẫu nhiên"""
    return random.choice(DANH_SACH_TRUYEN_CUOI)


# Bản dịch lỗi compiler g++ sang tiếng Việt phong cách hài hước
GXX_ERROR_PATTERNS = [
    (r"expected ';' before", "Ê dòng {line}: Thiếu dấu chấm phẩy kìa má! Quên cúng 'nhe;' hay 'ha;' zậy?"),
    (r"expected '\)' before", "Dòng {line}: Thiếu ngoặc tròn ')' đóng lại kìa má!"),
    (r"expected '\}' at end of input", "Hết file rồi mà thiếu dấu đóng ngoặc nhọn '}' kìa má! Đóng cửa tắt đèn giùm cái!"),
    (r"expected '\}' before", "Dòng {line}: Thiếu dấu ngoặc nhọn '}' kìa má ơi!"),
    (r"'(\w+)' was not declared in this scope", "Dòng {line}: Ủa biến/hàm '{param1}' ở đâu chui ra vậy má? Chưa khai sinh đã đòi xài, tính lừa thầy phản bạn hả?"),
    (r"cannot convert '([^']+)' to '([^']+)'", "Dòng {line}: Râu ông '{param1}' cắm cằm bà '{param2}' kìa! Ép kiểu tào lao vậy ba, máy tính nó trầm cảm luôn rồi!"),
    (r"redefinition of '([^']+)'", "Dòng {line}: Biến '{param1}' đã có rồi mà khai báo lần nữa? Tham lam vừa vừa thôi má ơi!"),
    (r"no matching function for call to '([^']+)'", "Dòng {line}: Gọi hàm '{param1}' kiểu gì kỳ cục kẹo vậy? Coi lại tham số giùm tui cái!"),
    (r"undefined reference to `tran_dau'", "Ủa alo? File code không có hàm 'tran_dau()' (main) kìa má! Không có trận đấu thì ai đá ai coi trời?"),
    (r"undefined reference to `main'", "Ủa alo? File code không có hàm 'tran_dau()' (main) kìa má! Không có trận đấu thì ai đá ai coi trời?"),
    (r"division by zero", "Dòng {line}: Chia cho 0 kìa ba! Định xé toang vũ trụ hay gì?"),
    (r"invalid operands of types", "Dòng {line}: Phép toán này tào lao quá má, hai kiểu dữ liệu này đánh nhau vỡ đầu bây giờ!"),
]
