"""Configured Wi-Fi and socket-based NTP, with no teaching-helper side effects."""
import network
import time
import socket
import struct
import uasyncio
import config


async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    profiles = config.WIFI_PROFILES
    if not profiles:
        raise ValueError('WIFI_PROFILES is empty')
    if wlan.isconnected():
        current = wlan.config('essid')
        if current in profiles:
            print('[WiFi] IP:', wlan.ifconfig()[0])
            return current, profiles[current]
    try:
        ranked = sorted(wlan.scan(), key=lambda entry: entry[3], reverse=True)
        candidates = []
        for entry in ranked:
            ssid = entry[0].decode('utf-8')
            if ssid in profiles and ssid not in candidates:
                candidates.append(ssid)
    except (OSError, UnicodeError):
        candidates = []
    for ssid in profiles:
        if ssid not in candidates:
            candidates.append(ssid)
    for attempt in range(3):
        for ssid in candidates:
            print('[WiFi] Connecting to configured network, attempt', attempt + 1)
            try:
                wlan.disconnect()
                wlan.connect(ssid, profiles[ssid])
                for _ in range(50):
                    if wlan.isconnected():
                        print('[WiFi] IP:', wlan.ifconfig()[0])
                        return ssid, profiles[ssid]
                    await uasyncio.sleep_ms(200)
            except OSError as error:
                print('[WiFi] Connection error:', type(error).__name__)
        await uasyncio.sleep(1)
    raise OSError('WiFi connection failed; check config.py and 2.4 GHz WiFi')


async def sync_time():
    from machine import RTC
    # MicroPython ESP32 may use the 2000 epoch; Unix uses the 1970 epoch.
    delta = 3155673600 if time.gmtime(0)[0] == 2000 else 2208988800
    packet = b'\x23' + b'\x00' * 47
    for server in ('pool.ntp.org', 'time.google.com', 'time.cloudflare.com'):
        client = None
        try:
            address = socket.getaddrinfo(server, 123, 0, socket.SOCK_DGRAM)[0][-1]
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.setblocking(False)
            client.sendto(packet, address)
            started = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), started) < 2000:
                try:
                    reply, sender = client.recvfrom(48)
                except OSError as error:
                    if error.args and error.args[0] in (11, 35, 10035, 115):
                        await uasyncio.sleep_ms(50)
                        continue
                    raise
                if sender[0] != address[0] or sender[1] != 123:
                    continue
                if (len(reply) < 48 or reply[0] & 7 != 4
                        or reply[0] >> 6 == 3 or not 1 <= reply[1] <= 15):
                    raise ValueError('Invalid NTP reply')
                seconds = struct.unpack('!I', reply[40:44])[0] - delta
                local = time.gmtime(seconds + config.TIMEZONE_OFFSET_SEC)
                if local[0] < 2020:
                    raise ValueError('Invalid NTP date')
                RTC().datetime((local[0], local[1], local[2], local[6],
                                local[3], local[4], local[5], 0))
                print('[Time] Clock synchronized (UTC+8)')
                return True
        except (OSError, ValueError):
            pass
        finally:
            if client is not None:
                client.close()
        await uasyncio.sleep_ms(100)
    print('[Time] NTP failed; retaining RTC time')
    return False


def get_current_time():
    now = time.localtime()
    return ('{:04d}/{:02d}/{:02d}'.format(now[0], now[1], now[2]),
            ('一', '二', '三', '四', '五', '六', '日')[now[6]],
            '{:02d}:{:02d}:{:02d}'.format(now[3], now[4], now[5]))
