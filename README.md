========================================================================
  Bảng điều khiển tự động Google AI Pro (5 TB) miễn phí hai năm
  (US$0.00 -> 24 tháng)
========================================================================

【I. YÊU CẦU VỀ MÔI TRƯỜNG】
1. Hệ điều hành Windows 10 / 11.
2. Đã cài đặt trình duyệt Google Chrome (dùng đường dẫn mặc định).
3. Đã cài đặt Python 3.10 trở lên (chọn Add Python to PATH khi cài đặt).
4. Mạng: bật proxy khu vực Hoa Kỳ (US) trên máy hoặc nhập mẫu proxy ở cột bên trái của bảng điều khiển.
5. KHUYẾN NGHỊ ĐỔI VPN VÀ MÚI GIỜ: sử dụng NordVPN, Proton VPN hoặc Hola tại khu vực Hoa Kỳ (US). Đổi múi giờ Windows khớp với vị trí VPN để tránh rò rỉ thông tin vị trí. Kiểm tra IP đầu ra trước khi chạy.

【II. CÁC BƯỚC KHỞI ĐỘNG NHANH】
1. Khi sử dụng lần đầu, nhấp đúp để chạy: 【1_Cai_dat_va_khoi_chay.bat】
2. Từ những lần sau, chỉ cần nhấp đúp: 【2_Khoi_chay_bang_dieu_khien.bat】
3. Trình duyệt sẽ tự động mở trang bảng điều khiển: http://127.0.0.1:8765

【III. TÙY CHỈNH THẺ THANH TOÁN VÀ HƯỚNG DẪN CHẠY TÀI KHOẢN】
1. Nhập thông tin thẻ thanh toán (bắt buộc):
   - Trong khu vực 【Cấu hình chung và liên kết thẻ miễn thuế trực tiếp】 ở bên trái trang web, nhập thông tin thẻ Visa hoặc Mastercard quốc tế của bạn:
     * Số thẻ (16 chữ số)
     * Ngày hết hạn (tháng / năm, ví dụ: 08 / 29)
     * Mã bảo mật (CVC gồm 3 chữ số)
     * Tên chủ thẻ bằng tiếng Anh
     * Mã bưu chính miễn thuế đã được điền sẵn là 97201 (Oregon, bang miễn thuế của Hoa Kỳ), không cần thay đổi
   - Sau khi nhập, nhấp vào 【💾 Lưu cấu hình】.
   - Lưu ý: tập lệnh có cơ chế bảo vệ nghiêm ngặt để không phát sinh chi phí. Chỉ khi cửa sổ thanh toán xác nhận số tiền là US$0.00, tập lệnh mới nhấp vào đăng ký; toàn bộ quá trình không bị trừ tiền.

2. Nhập hàng loạt tài khoản Google:
   - Dán danh sách tài khoản vào khu vực 【Nhập hàng loạt tài khoản】 ở bên phải trang web (mỗi dòng một tài khoản). Hỗ trợ bất kỳ định dạng nào sau đây:
     * email----mật_khẩu----email_khôi_phục
     * email----mật_khẩu----email_khôi_phục----khóa_2FA
     * email----mật_khẩu----khóa_2FA
   - Nhấp vào 【➕ Nhập toàn bộ danh sách tài khoản】.

3. Bắt đầu chạy tự động:
   - Nhấp vào 【▶ Thực thi】 bên cạnh từng tài khoản hoặc 【▶ Chạy tự động hàng loạt】 ở đầu trang.
   - Tập lệnh sẽ tự động hoàn thành các bước sau:
     Bước 1: Tự động đăng nhập Google và xác minh bằng email khôi phục / 2FA
     Bước 2: Liên kết thẻ miễn thuế trực tiếp + gói miễn phí 12 tháng đầu tiên (US$0.00)
     Bước 3: Cộng thêm gói miễn phí 6 tháng thứ hai (US$0.00 -> tổng cộng 18 tháng)
     Bước 4: Cộng thêm gói miễn phí 6 tháng thứ ba (US$0.00 -> đạt mức tối đa 24 tháng)
     Bước 5: Tự động chuyển đến Google Play để hủy gia hạn tự động, giữ quyền lợi cho đến khi hết hạn sau 2 năm và chụp ảnh màn hình để xác minh

【IV. BOT TELEGRAM ĐIỀU KHIỂN DASHBOARD】
Bot dùng Telegram Bot API qua long polling, không cần cài thêm thư viện Python và không thay đổi automation hiện có.

1. Tạo bot và lấy token:
   - Mở @BotFather trên Telegram, gửi /newbot và làm theo hướng dẫn.
   - Giữ token ở nơi riêng tư, không chia sẻ cho bất kỳ ai hoặc đưa vào mã nguồn.

2. Khởi chạy:
   - Chạy 【2_Khoi_chay_bang_dieu_khien.bat】 và giữ dashboard ở http://127.0.0.1:8765.
   - Chạy 【3_Khoi_chay_bot_Telegram.bat】, nhập token và Telegram user ID được cấp quyền khi được hỏi.
   - Nếu chưa biết user ID, để trống mục user ID, gửi /id cho bot rồi khởi động lại và nhập ID nhận được.
   - Có thể cấp quyền cho nhiều user bằng dấu phẩy, ví dụ: 123456789,987654321.

3. Cấu hình bằng biến môi trường nếu không dùng launcher:
   set TELEGRAM_BOT_TOKEN=token_cua_ban
   set TELEGRAM_ALLOWED_USER_IDS=123456789
   python telegram_bot.py
   Biến DASHBOARD_URL là tùy chọn, mặc định http://127.0.0.1:8765.

4. Các lệnh:
   - /status: tổng quan trạng thái hệ thống.
   - /accounts: xem email, trạng thái, bước hiện tại và ngày hết hạn.
   - /logs [1-30]: xem các dòng log mới nhất, ví dụ /logs 20.
   - /run <account_id>: chạy một tài khoản, ví dụ /run Account_1.
   - /runall: chạy toàn bộ tài khoản chưa hoàn tất.
   - /stop [account_id]: dừng một tài khoản đang chạy hoặc toàn bộ tác vụ.
   - /id: xem Telegram user ID.
   - /help: xem hướng dẫn trong Telegram.

5. Bảo mật:
   - Chỉ user ID nằm trong TELEGRAM_ALLOWED_USER_IDS mới có thể điều khiển bot.
   - Bot chỉ nhận lệnh trong chat riêng; không trả về mật khẩu, khóa 2FA hoặc thông tin thẻ.
   - Token chỉ đọc từ biến môi trường, không ghi vào config.json.


# Trang thẻ: https://faka.cdkey.si
# Blog: https://blog.caowo.de
# Nhóm TG: @Hello_Florence
