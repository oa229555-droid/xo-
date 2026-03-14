#!/usr/bin/env python3
"""
توليد بايلودات عشوائية
"""

import os
import random
import string

class PayloadGenerator:
    def __init__(self):
        self.payloads = []
        
    def generate(self, size):
        """توليد بايلود عشوائي بالحجم المطلوب"""
        return os.urandom(size)
    
    def generate_text(self, size):
        """توليد نص عشوائي"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()
    
    def generate_http(self):
        """توليد طلب HTTP عشوائي"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
        paths = ['/', '/index.html', '/api', '/data', '/image.jpg', '/script.js']
        
        method = random.choice(methods)
        path = random.choice(paths)
        
        return f"{method} {path} HTTP/1.1\r\nHost: example.com\r\n\r\n".encode()
    
    def generate_payloads(self, count, min_size=64, max_size=65535):
        """توليد مجموعة بايلودات"""
        for _ in range(count):
            size = random.randint(min_size, max_size)
            self.payloads.append(self.generate(size))
        return self.payloads
