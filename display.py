#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 JP Flouret <jpflouret@gmail.com>
# SPDX-License-Identifier: MIT

import time
import signal
import sys
import board
import busio
import psutil
import adafruit_ssd1306
import socket

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


def create_bar(opening, closing, value, width, char='\xfe'):
    bar_len = width - len(opening) - len(closing)
    bar_filled = round(bar_len * clamp(value, 0.0, 100.0) / 100.0)
    bar = char * clamp(bar_filled, 0, bar_len)
    return f"{opening}{bar.ljust(bar_len)}{closing}"


def get_hostname_and_ip():
    try:
        hostname = socket.gethostname()
        if not hostname or hostname == 'localhost':
            try:
                with open('/etc/hostname', 'r') as f:
                    hostname = f.read().strip()
            except:
                hostname = "unknown"
    except Exception:
        hostname = "unknown"

    try:
        ip_addr = "unknown"
        for interface in psutil.net_if_addrs():
            for addr in psutil.net_if_addrs()[interface]:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    ip_addr = addr.address
                    break
            if ip_addr != "unknown":
                break
    except Exception:
        ip_addr = "unknown"

    return hostname, ip_addr


def main():

    INTERVAL = 0.5
    i2c = busio.I2C(board.SCL, board.SDA)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

    def clear_display():
        display.fill(0)
        display.show()


    def cleanup_display():
        clear_display()
        sys.exit(0)


    def signal_handler(signum, frame):
        cleanup_display()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    clear_display()
    onoff = 0
    bar_graph_width = display.width // 6

    try:
        while True:
            onoff = (onoff+1) % 2
            cpu_percent = psutil.cpu_percent(interval=INTERVAL)
            ram_percent = psutil.virtual_memory().percent
            hostname, ip_addr = get_hostname_and_ip()

            display.fill(0)
            display.pixel(display.width-1, 0, onoff)
            display.text(hostname, 0, 0, 1)
            display.text(ip_addr, 0, 8, 1)
            display.text(create_bar("CPU: [", "]", cpu_percent, bar_graph_width), 0, 16, 1)
            display.text(create_bar("Mem: [", "]", ram_percent, bar_graph_width), 0, 24, 1)
            display.show()

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        cleanup_display()

if __name__ == "__main__":
    main()
