# ⚡ OverGTien DoS Bot

<div align="center">

![Version](https://img.shields.io/badge/Version-3.0.0-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20Windows-lightgrey?style=for-the-badge)

**Power meets Simplicity**

<img src="https://img.shields.io/badge/MADE%20WITH-PYTHON%20%7C%20AIOHTTP%20%7C%20TELEGRAM-orange?style=for-the-badge" alt="Made with">

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Phương thức tấn công](#-phương-thức-tấn-công)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Cấu hình](#-cấu-hình)
- [Sử dụng](#-sử-dụng)
- [Commands](#-commands)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Hiệu suất](#-hiệu-suất)
- [Bảo mật](#-bảo-mật)
- [Khắc phục sự cố](#-khắc-phục-sự-cố)
- [Đóng góp](#-đóng-góp)
- [Disclaimer](#-disclaimer)
- [Tác giả](#-tác-giả)
- [License](#-license)

---

## 🚀 Giới thiệu

**OverGTien** là công cụ DoS (Denial of Service) thế hệ mới, được điều khiển hoàn toàn qua **Telegram Bot**. Với kiến trúc **async aiohttp**, OverGTien có khả năng tạo ra hàng ngàn requests mỗi giây, hỗ trợ đa dạng phương thức tấn công từ Layer 2 đến Layer 7.

> **Tên gọi:** OverGTien = Over (vượt trội) + GTien (tốc độ) = "Sức mạnh vượt trội"

---

## ✨ Tính năng

### Core Features
- 🤖 **Telegram Bot Control** - Điều khiển từ xa qua Telegram
- ⚡ **Async aiohttp Engine** - Hiệu suất cực cao, non-blocking I/O
- 🌐 **SOCKS5 Proxy Support** - Tự động fetch và sử dụng proxy
- 📊 **Real-time Statistics** - Cập nhật trạng thái mỗi 3 giây
- 🎛️ **Inline Keyboard** - Giao diện nút bấm trực quan
- 🔒 **Admin Only** - Bảo mật tuyệt đối
- 📈 **Progress Bar** - Hiển thị tiến trình trực quan
- 🔄 **Auto Recovery** - Tự động tạo lại connections khi mất

### Advanced Features
- 🧵 **Multi-threading + Async** - Kết hợp sức mạnh của cả hai
- 🛡️ **CloudFlare Detection** - Phát hiện website dùng CloudFlare
- 📝 **Comprehensive Logging** - Log chi tiết mọi hoạt động
- 🎯 **Multiple Attack Methods** - 7 phương thức tấn công khác nhau
- 🔌 **Plug & Play** - Cài đặt và chạy trong 5 phút

---

## 🎯 Phương thức tấn công

### Layer 7 - Application Layer

| Method | Mô tả | Proxy | Hiệu suất |
|--------|-------|-------|-----------|
| `http` | HTTP GET Flood cơ bản | ❌ | ⭐⭐⭐⭐⭐ |
| `http-proxy` | HTTP GET Flood qua SOCKS5 | ✅ | ⭐⭐⭐⭐ |
| `slowloris` | Giữ kết nối mở (Keep-Alive) | ❌ | ⭐⭐⭐ |
| `slowloris-proxy` | Slowloris qua SOCKS5 Proxy | ✅ | ⭐⭐⭐ |

### Layer 4 - Transport Layer

| Method | Mô tả | Yêu cầu |
|--------|-------|---------|
| `syn-flood` | TCP SYN Flood | **Root** |

### Layer 2 - Data Link Layer

| Method | Mô tả | Yêu cầu |
|--------|-------|---------|
| `arp-spoof` | ARP Spoofing Attack | **Root** |
| `disconnect` | Network Disconnect | **Root** |

---

## 💻 Yêu cầu hệ thống

### Hệ điều hành
- **Linux** (Ubuntu, Debian, Kali, Arch, etc.) ✅
- **Termux** (Android) ✅
- **Windows** (Limited - chỉ HTTP methods) ⚠️
- **macOS** ✅

### Phần mềm
- **Python** 3.7 trở lên
- **pip** (Python package manager)
- **Git** (để clone repository)

### Dependencies
```

python-telegram-bot >= 20.0
aiohttp >= 3.8.0
colorama >= 0.4.5
PySocks >= 1.7.1
scapy >= 2.4.5
requests >= 2.28.1

```

---

## 📥 Cài đặt

### Cách 1: Cài đặt nhanh (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/gtieniosvn/overload-dos-bot.git

# Di chuyển vào thư mục
cd OverGTien

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy bot
python overgtien_bot.py
```

Cách 2: Cài đặt thủ công

```bash
# Tải code
wget https://github.com/gtieniosvn/overload-dos-bot/archive/main.zip
unzip main.zip
cd OverGTien-main

# Cài đặt từng gói
pip install python-telegram-bot
pip install aiohttp
pip install colorama
pip install PySocks
pip install scapy
pip install requests

# Chạy
python overgtien_bot.py
```

Cách 3: Termux (Android)

```bash
# Cập nhật Termux
pkg update && pkg upgrade

# Cài Python và Git
pkg install python git

# Cài dependencies
pip install python-telegram-bot aiohttp colorama PySocks scapy requests

# Clone và chạy
git clone https://github.com/gtieniosvn/overload-dos-bot.git
cd OverGTien
python overgtien_bot.py
```

---

⚙️ Cấu hình

Bước 1: Tạo Telegram Bot

1. Mở Telegram, tìm @BotFather
2. Gửi lệnh /newbot
3. Đặt tên cho bot (VD: OverGTien Bot)
4. Đặt username cho bot (VD: OverGTien_bot)
5. Lưu Token được cung cấp

```
Example Token:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

Bước 2: Lấy Admin ID

1. Mở Telegram, tìm @userinfobot
2. Gửi lệnh /start
3. Lưu ID của bạn

```
Example ID:
987654321
```

Bước 3: Thiết lập biến môi trường

Linux/macOS/Termux

```bash
export BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export ADMIN_ID="987654321"
```

Thêm vào ~/.bashrc hoặc ~/.zshrc để tự động load:

```bash
echo 'export BOT_TOKEN="YOUR_TOKEN"' >> ~/.bashrc
echo 'export ADMIN_ID="YOUR_ID"' >> ~/.bashrc
source ~/.bashrc
```

Windows (Command Prompt)

```cmd
set BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
set ADMIN_ID=987654321
```

Windows (PowerShell)

```powershell
$env:BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
$env:ADMIN_ID="987654321"
```

Bước 4: Xác nhận cấu hình

```bash
# Kiểm tra biến môi trường
echo $BOT_TOKEN
echo $ADMIN_ID

# Chạy bot
python overgtien_bot.py
```

Nếu thấy thông báo:

```
[✓] OverGTien Bot is running...
[*] Press Ctrl+C to stop
```

Là thành công! 🎉

---

📖 Sử dụng

Giao diện Telegram

1. Mở Telegram, tìm bot của bạn
2. Gửi /start để hiện menu chính
3. Chọn chức năng từ bàn phím:

```
╔══════════════════════════╗
║  ⚔️ New Attack          ║
║  📊 System Info         ║
║  🛑 Stop All            ║
║  ❓ Help                ║
╚══════════════════════════╝
```

Quy trình tấn công

```
1. Chọn "⚔️ New Attack"
2. Chọn phương thức (HTTP, HTTP-Proxy, Slowloris, ...)
3. Nhập URL mục tiêu (VD: http://example.com)
4. Nhập số lượng threads (VD: 100)
5. Nhập thời gian tấn công (VD: 60 giây)
6. Xác nhận "✅ LAUNCH"
```

Màn hình trạng thái

```
⚔️ OverGTien ATTACK STATUS

🎯 Target: http://example.com
🔧 Method: HTTP
⏱️ Elapsed: 30s
⏳ Remaining: 30s

[████████░░] 50.0%

📤 Requests: 15,234
✅ Success (200): 12,456
🚫 Blocked (403): 1,234
❌ Errors: 1,544
📦 Data Sent: 45.67 MB
⚡ Requests/s: 507.8
📈 Success Rate: 81.8%

[🛑 STOP ATTACK]
```

---

📟 Commands

Commands Telegram

Command Chức năng Ví dụ
/start Hiển thị menu chính /start
/attack Bắt đầu tấn công mới /attack
/stop Dừng tất cả tấn công /stop
/status Xem trạng thái hiện tại /status
/info Thông tin hệ thống /info
/help Xem trợ giúp /help
/cancel Hủy thao tác hiện tại /cancel

Phím tắt

Nút Chức năng
⚔️ New Attack Bắt đầu tấn công mới
📊 System Info Xem thông tin hệ thống
🛑 Stop All Dừng tất cả cuộc tấn công
🛑 STOP ATTACK Dừng cuộc tấn công hiện tại
✅ LAUNCH Xác nhận và bắt đầu
❌ CANCEL Hủy bỏ

---

📁 Cấu trúc dự án

```
OverGTien/
├── overgtien_bot.py          # Main bot file
├── requirements.txt          # Python dependencies
├── README.md                # Tài liệu hướng dẫn
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
│
├── assets/                  # Tài nguyên
│   ├── logo.png            # Logo
│   └── screenshot.png      # Ảnh chụp màn hình
│
├── docs/                    # Tài liệu bổ sung
│   ├── INSTALL.md          # Hướng dẫn cài đặt chi tiết
│   ├── METHODS.md          # Mô tả các phương thức
│   └── FAQ.md              # Câu hỏi thường gặp
│
└── tests/                   # Unit tests
    └── test_bot.py
```

---

📊 Hiệu suất

Benchmark

Method Threads Requests/s CPU Usage Memory
http 100 ~500-800 60-70% ~150MB
http 500 ~2000-3000 80-90% ~300MB
http-proxy 50 ~200-400 40-50% ~120MB
slowloris 100 N/A 30-40% ~100MB

So sánh với công cụ khác

Tool Async Proxy Telegram Requests/s
OverGTien ✅ ✅ ✅ 800+
LOIC ❌ ❌ ❌ ~200
HOIC ❌ ❌ ❌ ~300
Slowloris ❌ ❌ ❌ N/A

---

🔒 Bảo mật

Các biện pháp bảo mật

1. Admin Only - Chỉ ID được cấu hình mới dùng được bot
2. Environment Variables - Token không hardcode trong code
3. .gitignore - Đảm bảo không push token lên GitHub
4. Input Validation - Kiểm tra tất cả input từ người dùng

Best Practices

```bash
# ✅ ĐÚNG - Sử dụng biến môi trường
export BOT_TOKEN="your_token"
python overgtien_bot.py

# ❌ SAI - Hardcode token trong code
BOT_TOKEN = "123456:ABCdef"  # Không làm vậy!
```

---

🔧 Khắc phục sự cố

Lỗi thường gặp

Lỗi Nguyên nhân Cách khắc phục
ModuleNotFoundError Thiếu dependencies pip install -r requirements.txt
403 Forbidden Bị target chặn Đổi proxy hoặc method khác
Bot not responding Token sai hoặc hết hạn Kiểm tra lại BOT_TOKEN
Connection Refused Server target đã sập Đợi server online lại
Permission denied Thiếu quyền root Chạy với sudo
Timeout Mạng chậm hoặc target chặn Tăng timeout hoặc đổi proxy

Debug Mode

```bash
# Bật debug mode
export DEBUG=true
python overgtien_bot.py
```

---

🤝 Đóng góp

Các bước đóng góp

1. Fork dự án
2. Tạo branch mới (git checkout -b feature/AmazingFeature)
3. Commit thay đổi (git commit -m 'Add some AmazingFeature')
4. Push lên branch (git push origin feature/AmazingFeature)
5. Mở Pull Request

Coding Standards

· Tuân thủ PEP 8
· Viết docstring cho tất cả functions
· Thêm type hints
· Viết unit tests cho features mới

---

⚠️ Disclaimer

```
╔══════════════════════════════════════════════════════╗
║                    ⚠️ CẢNH BÁO ⚠️                    ║
║                                                      ║
║  Công cụ này được tạo ra CHỈ CHO MỤC ĐÍCH:           ║
║  • Giáo dục về an ninh mạng                          ║
║  • Kiểm thử bảo mật trên hệ thống ĐƯỢC PHÉP          ║
║  • Nghiên cứu về tấn công từ chối dịch vụ            ║
║                                                      ║
║  ❌ KHÔNG sử dụng để:                                 ║
║  • Tấn công hệ thống KHÔNG ĐƯỢC PHÉP                 ║
║  • Gây thiệt hại cho bất kỳ tổ chức/cá nhân nào      ║
║  • Vi phạm pháp luật                                  ║
║                                                      ║
║  Tác giả KHÔNG chịu trách nhiệm về:                   ║
║  • Bất kỳ hành vi sử dụng sai mục đích nào           ║
║  • Thiệt hại gây ra bởi công cụ này                  ║
║  • Hậu quả pháp lý từ việc sử dụng                   ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

👥 Tác giả

Tác giả Vai trò Liên hệ
7zx Core Developer GitHub
8fn Core Developer GitHub
João Core Developer GitHub

Contributors

Cảm ơn tất cả những người đã đóng góp cho dự án!

https://contrib.rocks/image?repo=YOUR_USERNAME/OverGTien

---

⭐ Star History

Nếu bạn thấy dự án hữu ích, hãy cho một ⭐!

https://api.star-history.com/svg?repos=YOUR_USERNAME/OverGTien&type=Date

---

📜 License

Dự án được phân phối dưới MIT License. Xem file LICENSE để biết thêm chi tiết.

```
MIT License

Copyright (c) 2024 7zx, 8fn, João

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

---

🗺️ Roadmap

v3.1.0 (Coming Soon)

· Web Dashboard
· Multiple bot support
· Custom User-Agent lists
· Proxy auto-rotation

v3.2.0 (Planned)

· DDoS (Distributed) mode
· Machine Learning evasion
· API for external tools
· Docker support

v3.3.0 (Future)

· GUI Desktop App
· Mobile App (React Native)
· Cloud deployment scripts
· Attack templates

---

💬 Hỗ trợ

· Telegram: @OverGTien_Support
· Issues: GitHub Issues
· Discussions: GitHub Discussions
· Email: support@overgtien.com

---

🙏 Lời cảm ơn

· python-telegram-bot - Telegram Bot API wrapper
· aiohttp - Async HTTP client/server
· scapy - Packet manipulation
· PySocks - SOCKS proxy client
· colorama - Terminal colors

---

<div align="center">

⚡ OverGTien

"Power meets Simplicity"

⬆ Back to top

</div>
``` 
