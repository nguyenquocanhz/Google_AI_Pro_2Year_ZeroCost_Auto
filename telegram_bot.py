import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter

if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

STATUS_LABELS = {
    "pending": "⏳ Đang chờ",
    "running": "🔄 Đang chạy",
    "waiting_human": "🟡 Cần can thiệp",
    "completed": "✅ Hoàn tất",
    "error": "❌ Lỗi",
}

HELP_TEXT = """🤖 Bot điều khiển Google AI Pro

/status — Tổng quan trạng thái
/accounts — Danh sách tài khoản và tiến độ
/logs [1-30] — Xem các dòng log mới nhất
/run <account_id> — Chạy một tài khoản
/runall — Chạy toàn bộ tài khoản chưa hoàn tất
/stop [account_id] — Dừng một hoặc toàn bộ tác vụ
/id — Xem Telegram user ID của bạn
/help — Hiện hướng dẫn

Ví dụ: /run Account_1
Bot không trả về mật khẩu, khóa 2FA hoặc thông tin thẻ."""


def split_text(text, limit=3500):
    chunks = []
    remaining = text or "(Không có nội dung)"
    while len(remaining) > limit:
        cut = remaining.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = limit
        chunks.append(remaining[:cut])
        remaining = remaining[cut:].lstrip("\n")
    chunks.append(remaining)
    return chunks


def json_request(url, payload=None, timeout=20, source="Dịch vụ"):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="GET" if data is None else "POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
            detail = body.get("detail") or body.get("description") or raw
        except json.JSONDecodeError:
            detail = raw or str(exc)
        raise RuntimeError(f"{source}: {detail}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{source} không phản hồi: {exc.reason}") from None
    except TimeoutError:
        raise RuntimeError(f"{source}: không nhận được phản hồi đúng hạn") from None


class TelegramDashboardBot:
    def __init__(self, token, allowed_user_ids, dashboard_url="http://127.0.0.1:8765"):
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.allowed_user_ids = set(allowed_user_ids)
        self.dashboard_url = dashboard_url.rstrip("/")

    def telegram(self, method, payload=None, timeout=20):
        result = json_request(
            f"{self.api_url}/{method}",
            payload=payload or {},
            timeout=timeout,
            source="Telegram",
        )
        if not result.get("ok"):
            raise RuntimeError(f"Telegram: {result.get('description', 'phản hồi không hợp lệ')}")
        return result.get("result")

    def dashboard(self, path, payload=None):
        return json_request(
            f"{self.dashboard_url}{path}",
            payload=payload,
            timeout=25,
            source="Dashboard",
        )

    def send_text(self, chat_id, text):
        for chunk in split_text(text):
            self.telegram(
                "sendMessage",
                {"chat_id": chat_id, "text": chunk, "disable_web_page_preview": True},
            )

    def handle_message(self, message):
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        user_id = message.get("from", {}).get("id")
        text = message.get("text", "").strip()
        if chat_id is None or user_id is None or not text.startswith("/"):
            return

        command = text.split(maxsplit=1)[0].split("@", 1)[0].lower()
        args = text.split()[1:]

        if command == "/id":
            self.send_text(chat_id, f"Telegram user ID của bạn: {user_id}")
            return
        if chat.get("type") != "private":
            self.send_text(chat_id, "🔒 Bot chỉ nhận lệnh trong chat riêng để bảo vệ dữ liệu.")
            return
        if user_id not in self.allowed_user_ids:
            self.send_text(
                chat_id,
                f"🔒 Tài khoản Telegram chưa được cấp quyền.\nUser ID: {user_id}\n"
                "Thêm ID này vào TELEGRAM_ALLOWED_USER_IDS rồi khởi động lại bot.",
            )
            return

        try:
            response = self.execute(command, args)
        except Exception as exc:
            response = f"❌ {exc}"
        self.send_text(chat_id, response)

    def execute(self, command, args):
        if command in ("/start", "/help"):
            return HELP_TEXT
        if command == "/status":
            return self.status_text()
        if command == "/accounts":
            return self.accounts_text()
        if command == "/logs":
            return self.logs_text(args)
        if command == "/run":
            return self.run_single(args)
        if command == "/runall":
            result = self.dashboard("/api/run/batch", {})
            queued = result.get("queued", [])
            return f"🚀 Đã đưa {len(queued)} tài khoản vào hàng đợi chạy hàng loạt."
        if command == "/stop":
            return self.stop(args)
        return "Lệnh không được hỗ trợ. Dùng /help để xem danh sách lệnh."

    def status_text(self):
        state = self.dashboard("/api/state")
        accounts = state.get("accounts", [])
        counts = Counter(account.get("status", "pending") for account in accounts)
        lines = [
            "📊 TRẠNG THÁI HỆ THỐNG",
            f"Khu vực: {state.get('target_region', 'US')}",
            f"Tổng số tài khoản: {len(accounts)}",
            f"Tiến trình đang hoạt động: {state.get('active_count', 0)}",
            f"Chạy hàng loạt: {'Có' if state.get('batch_running') else 'Không'}",
            f"Tự động hủy gia hạn: {'Bật' if state.get('auto_cancel') else 'Tắt'}",
            "",
        ]
        for status, label in STATUS_LABELS.items():
            lines.append(f"{label}: {counts.get(status, 0)}")
        for status, count in sorted(counts.items()):
            if status not in STATUS_LABELS:
                lines.append(f"{status}: {count}")
        return "\n".join(lines)

    def accounts_text(self):
        accounts = self.dashboard("/api/state").get("accounts", [])
        if not accounts:
            return "📋 Chưa có tài khoản nào. Hãy nhập tài khoản từ dashboard."
        lines = [f"📋 DANH SÁCH TÀI KHOẢN ({len(accounts)})"]
        for index, account in enumerate(accounts[:20], start=1):
            status = STATUS_LABELS.get(account.get("status"), account.get("status", "Không rõ"))
            message = account.get("step_message", "")
            if len(message) > 180:
                message = message[:177] + "..."
            lines.extend(
                [
                    "",
                    f"{index}. {account.get('id', 'Không rõ')} — {status}",
                    account.get("email", "Không có email"),
                    f"Bước: {account.get('current_step', 0)}/5 | Hết hạn: {account.get('expiry_date', '-')}",
                    message,
                ]
            )
        if len(accounts) > 20:
            lines.extend(["", f"… Còn {len(accounts) - 20} tài khoản nữa."])
        return "\n".join(lines)

    def logs_text(self, args):
        try:
            count = int(args[0]) if args else 12
        except ValueError:
            raise RuntimeError("Số dòng log phải là một số từ 1 đến 30.") from None
        if not 1 <= count <= 30:
            raise RuntimeError("Số dòng log phải từ 1 đến 30.")
        logs = self.dashboard("/api/state").get("logs", [])
        if not logs:
            return "📜 Chưa có log nào."
        return f"📜 {min(count, len(logs))} DÒNG LOG MỚI NHẤT\n\n" + "\n".join(logs[-count:])

    def find_account(self, account_id):
        accounts = self.dashboard("/api/state").get("accounts", [])
        return next((account for account in accounts if account.get("id") == account_id), None)

    def run_single(self, args):
        if not args:
            raise RuntimeError("Cú pháp: /run <account_id>. Ví dụ: /run Account_1")
        account_id = args[0]
        account = self.find_account(account_id)
        if not account:
            raise RuntimeError(f"Không tìm thấy tài khoản {account_id}.")
        if account.get("is_running"):
            raise RuntimeError(f"Tài khoản {account_id} đang chạy.")
        self.dashboard("/api/run/single", {"account_id": account_id})
        return f"🚀 Đã bắt đầu chạy {account_id}. Dùng /status để theo dõi."

    def stop(self, args):
        if not args:
            self.dashboard("/api/stop", {})
            return "⏹ Đã gửi lệnh dừng toàn bộ tác vụ."
        account_id = args[0]
        account = self.find_account(account_id)
        if not account:
            raise RuntimeError(f"Không tìm thấy tài khoản {account_id}.")
        if not account.get("is_running"):
            raise RuntimeError(f"Tài khoản {account_id} không đang chạy; chưa gửi lệnh dừng.")
        self.dashboard("/api/stop", {"account_id": account_id})
        return f"⏹ Đã gửi lệnh dừng {account_id}."


def parse_allowed_user_ids(raw):
    user_ids = set()
    for value in re.split(r"[\s,;]+", raw.strip()):
        if not value:
            continue
        try:
            user_ids.add(int(value))
        except ValueError:
            print(f"[BOT] Bỏ qua Telegram user ID không hợp lệ: {value}", flush=True)
    return user_ids


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("Thiếu TELEGRAM_BOT_TOKEN. Xem hướng dẫn trong README.md.")
    allowed_user_ids = parse_allowed_user_ids(os.environ.get("TELEGRAM_ALLOWED_USER_IDS", ""))
    dashboard_url = os.environ.get("DASHBOARD_URL", "http://127.0.0.1:8765")
    bot = TelegramDashboardBot(token, allowed_user_ids, dashboard_url)

    print("[BOT] Bot Telegram đã sẵn sàng.", flush=True)
    print(f"[BOT] Dashboard: {dashboard_url}", flush=True)
    print(f"[BOT] Số Telegram user được cấp quyền: {len(allowed_user_ids)}", flush=True)
    if not allowed_user_ids:
        print("[BOT] Chưa có user nào được cấp quyền. Gửi /id cho bot để lấy ID.", flush=True)

    offset = 0
    while True:
        try:
            updates = bot.telegram(
                "getUpdates",
                {"offset": offset, "timeout": 40, "allowed_updates": ["message"]},
                timeout=55,
            )
            for update in updates or []:
                offset = update["update_id"] + 1
                message = update.get("message")
                if message:
                    bot.handle_message(message)
        except KeyboardInterrupt:
            print("\n[BOT] Đã dừng bot.", flush=True)
            break
        except Exception as exc:
            print(f"[BOT] Lỗi vòng lặp: {exc}", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()
