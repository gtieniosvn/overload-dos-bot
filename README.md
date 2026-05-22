# ⚡ Overload DoS Bot - Telegram Edition

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/your_bot)

> **⚠️ CẢNH BÁO: Chỉ sử dụng cho mục đích giáo dục và kiểm thử trên hệ thống được phép!**

## 📋 Tính năng

- 🤖 **Điều khiển qua Telegram Bot** - Quản lý từ xa dễ dàng
- ⚡ **Async aiohttp** - Hiệu suất cao, hỗ trợ 500+ requests/giây
- 🌐 **Hỗ trợ SOCKS5 Proxy** - Ẩn danh khi tấn công HTTP
- 📊 **Real-time Statistics** - Cập nhật trạng thái mỗi 3 giây
- 🎛️ **Inline Keyboard** - Giao diện nút bấm tiện lợi
- 🔒 **Admin Only** - Bảo mật, chỉ admin được sử dụng

## 🚀 Cài đặt

### Yêu cầu

- Python 3.7+
- pip
- Git

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Tạo Telegram Bot

1. Nhắn tin cho @BotFather trên Telegram
2. Gửi lệnh /newbot
3. Đặt tên cho bot
4. Lưu Bot Token

Cấu hình

```bash
# Linux/Mac/Termux
export BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
export ADMIN_ID="YOUR_TELEGRAM_ID"

# Windows (Command Prompt)
set BOT_TOKEN=YOUR_BOT_TOKEN_HERE
set ADMIN_ID=YOUR_TELEGRAM_ID

# Windows (PowerShell)
$env:BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
$env:ADMIN_ID="YOUR_TELEGRAM_ID"
```

Chạy bot

```bash
python overload_bot.py
```

📖 Cách sử dụng

Commands Telegram

Command Chức năng
/start Menu chính
/attack Bắt đầu tấn công mới
/stop Dừng tấn công
/status Xem trạng thái
/info Thông tin hệ thống
/help Trợ giúp

Phương thức tấn công

Method Mô tả Yêu cầu
http HTTP GET Flood -
http-proxy HTTP qua SOCKS5 Proxy -
slowloris Slowloris Keep-Alive -
slowloris-proxy Slowloris qua Proxy -
syn-flood TCP SYN Flood Root
arp-spoof ARP Spoofing Root
disconnect Ngắt kết nối mạng Root

🏗️ Cấu trúc dự án

```
overload-dos-bot/
├── overload_bot.py          # Main bot file
├── requirements.txt         # Dependencies
├── README.md               # Tài liệu
├── .gitignore              # Git ignore
└── LICENSE                 # License
```

⚙️ Requirements

```
python-telegram-bot>=20.0
aiohttp>=3.8
colorama>=0.4.5
PySocks>=1.7.1
scapy>=2.4.5
requests>=2.28.1
```

🔒 Bảo mật

· Không commit Bot Token lên GitHub!
· Sử dụng biến môi trường
· Admin Only - Chỉ ID được phép mới dùng được bot

⚠️ Disclaimer

Công cụ này chỉ được tạo ra cho mục đích giáo dục và kiểm thử bảo mật trên các hệ thống được phép.

Tác giả không chịu trách nhiệm về bất kỳ hành vi sử dụng sai mục đích nào.
