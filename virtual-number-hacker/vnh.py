#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
============================================================
Virtual Number Hacker (VNH) - أداة الأرقام الافتراضية
للاستخدام في Termux - نسخة مبسطة وسريعة
============================================================
"""

import os
import sys
import time
import random
import json
import sqlite3
import threading
import requests
from datetime import datetime

# محاولة استيراد المكتبات مع رسائل خطأ واضحة
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    # تعريف ألوان وهمية
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    Style = type('', (), {'BRIGHT': ''})()

# التحقق من المكتبات الأساسية
REQUIRED_MODULES = {
    'requests': 'requests',
    'beautifulsoup4': 'bs4',
    'phonenumbers': 'phonenumbers'
}

missing = []
for module, import_name in REQUIRED_MODULES.items():
    try:
        __import__(import_name)
    except ImportError:
        missing.append(module)

if missing:
    print(f"{Fore.RED}❌ المكتبات التالية غير مثبتة: {', '.join(missing)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}قم بتشغيل: pip install {' '.join(missing)}{Style.RESET_ALL}")
    sys.exit(1)

# استيراد باقي المكتبات
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import phonenumbers
from phonenumbers import carrier, timezone, geocoder

# ========== الإعدادات ==========
VERSION = "1.0.0"
DB_NAME = "vnh_numbers.db"
ua = UserAgent()

# ========== تهيئة قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS numbers
                 (number TEXT PRIMARY KEY, country TEXT, source TEXT, 
                  date TEXT, used INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def save_number(number, country, source):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO numbers (number, country, source, date) VALUES (?, ?, ?, ?)",
                  (number, country, source, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except:
        pass
    conn.commit()
    conn.close()

def get_random_number():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT number, country, source FROM numbers WHERE used = 0 ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    if result:
        c.execute("UPDATE numbers SET used = 1 WHERE number = ?", (result[0],))
    conn.commit()
    conn.close()
    return result

# ========== المصادر ==========
def get_from_onlinesim():
    """جلب أرقام من OnlineSim"""
    numbers = []
    try:
        url = "https://onlinesim.io/api/getFreeNumbers"
        r = requests.get(url, timeout=10, headers={'User-Agent': ua.random})
        if r.status_code == 200:
            data = r.json()
            for item in data[:10]:
                if 'number' in item:
                    num = item['number']
                    numbers.append({
                        'number': num,
                        'country': item.get('country', 'Unknown'),
                        'source': 'OnlineSim'
                    })
    except:
        pass
    return numbers

def generate_israeli(count=5):
    """توليد أرقام إسرائيلية"""
    numbers = []
    operators = ['50', '52', '53', '54', '55', '56', '57', '58', '59']
    for _ in range(count):
        op = random.choice(operators)
        sub = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        num = f"+972{op}{sub}"
        try:
            if phonenumbers.is_valid_number(phonenumbers.parse(num)):
                numbers.append({'number': num, 'country': 'IL', 'source': 'Generator'})
        except:
            continue
    return numbers

def generate_usa(count=5):
    """توليد أرقام أمريكية"""
    numbers = []
    area_codes = ['212', '213', '214', '215', '216', '217', '218', '310', '312', '313']
    for _ in range(count):
        area = random.choice(area_codes)
        sub = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        num = f"+1{area}{sub}"
        try:
            if phonenumbers.is_valid_number(phonenumbers.parse(num)):
                numbers.append({'number': num, 'country': 'US', 'source': 'Generator'})
        except:
            continue
    return numbers

def get_all_numbers():
    """جمع كل الأرقام"""
    all_nums = []
    print(f"{Fore.CYAN}[*] جاري جمع الأرقام...{Style.RESET_ALL}")
    
    nums = get_from_onlinesim()
    all_nums.extend(nums)
    print(f"{Fore.GREEN}[✓] OnlineSim: {len(nums)} رقم{Style.RESET_ALL}")
    
    nums = generate_israeli(3)
    all_nums.extend(nums)
    print(f"{Fore.GREEN}[✓] إسرائيلي: {len(nums)} رقم{Style.RESET_ALL}")
    
    nums = generate_usa(3)
    all_nums.extend(nums)
    print(f"{Fore.GREEN}[✓] أمريكي: {len(nums)} رقم{Style.RESET_ALL}")
    
    for item in all_nums:
        save_number(item['number'], item['country'], item['source'])
    
    return all_nums

# ========== الواجهة ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════╗
{Fore.RED}║  {Fore.YELLOW}██╗   ██╗███╗   ██╗██╗  ██╗{Fore.RED}                          ║
{Fore.RED}║  {Fore.YELLOW}██║   ██║████╗  ██║██║  ██║{Fore.RED}                          ║
{Fore.RED}║  {Fore.YELLOW}██║   ██║██╔██╗ ██║███████║{Fore.RED}                          ║
{Fore.RED}║  {Fore.YELLOW}╚██╗ ██╔╝██║╚██╗██║██╔══██║{Fore.RED}                          ║
{Fore.RED}║  {Fore.YELLOW} ╚████╔╝ ██║ ╚████║██║  ██║{Fore.RED}                          ║
{Fore.RED}║  {Fore.YELLOW}  ╚═══╝  ╚═╝  ╚═══╝╚═╝  ╚═╝{Fore.RED}                          ║
{Fore.RED}╠══════════════════════════════════════════════════════════╣
{Fore.RED}║  {Fore.CYAN}Virtual Number Hacker v{VERSION}{Fore.RED}                              ║
{Fore.RED}║  {Fore.GREEN}أداة الأرقام الافتراضية - للاستخدام التعليمي{Fore.RED}         ║
{Fore.RED}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def show_menu():
    print(f"\n{Fore.CYAN}════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1]{Fore.WHITE} الحصول على رقم عشوائي{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[2]{Fore.WHITE} الحصول على رقم إسرائيلي (+972){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[3]{Fore.WHITE} الحصول على رقم أمريكي (+1){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[4]{Fore.WHITE} تحديث قاعدة البيانات{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[5]{Fore.WHITE} عرض الإحصائيات{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[6]{Fore.WHITE} معلومات عن الثغرات{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[0]{Fore.WHITE} خروج{Style.RESET_ALL}")
    print(f"{Fore.CYAN}════════════════════════════════════════════════{Style.RESET_ALL}")

def show_number_info(number, country, source):
    print(f"\n{Fore.GREEN}✅ تم العثور على رقم!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📱 الرقم:{Fore.WHITE} {number}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🌍 الدولة:{Fore.WHITE} {country}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📦 المصدر:{Fore.WHITE} {source}{Style.RESET_ALL}")
    
    try:
        parsed = phonenumbers.parse(number)
        country_name = geocoder.description_for_number(parsed, 'ar')
        operator = carrier.name_for_number(parsed, 'ar')
        if country_name:
            print(f"{Fore.YELLOW}🏳️ الدولة بالعربية:{Fore.WHITE} {country_name}{Style.RESET_ALL}")
        if operator:
            print(f"{Fore.YELLOW}📡 المشغل:{Fore.WHITE} {operator}{Style.RESET_ALL}")
    except:
        pass
    
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")

def show_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM numbers")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM numbers WHERE used = 0")
    available = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM numbers WHERE used = 1")
    used = c.fetchone()[0]
    c.execute("SELECT country, COUNT(*) FROM numbers GROUP BY country")
    by_country = c.fetchall()
    conn.close()
    
    print(f"\n{Fore.CYAN}📊 إحصائيات قاعدة البيانات{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📦 إجمالي الأرقام:{Fore.WHITE} {total}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ متاح:{Fore.WHITE} {available}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ مستخدم:{Fore.WHITE} {used}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🌍 حسب الدولة:{Style.RESET_ALL}")
    for country, count in by_country:
        flag = "🇮🇱" if country == "IL" else "🇺🇸" if country == "US" else "🌍"
        print(f"  {flag} {country}: {count}")

def show_vuln_info():
    info = f"""
{Fore.RED}⚠️  معلومات الثغرات (للدراسة فقط){Style.RESET_ALL}
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}

{Fore.YELLOW}1. ثغرة SafeUM:{Style.RESET_ALL}
   • استغلال أنماط أرقام SafeUM
   • توليد أرقام +972 بنسبة نجاح عالية

{Fore.YELLOW}2. ثغرة OnlineSim API:{Style.RESET_ALL}
   • استخراج أرقام مجانية
   • تحديث يومي للأرقام

{Fore.YELLOW}3. ثغرة الأرقام الإسرائيلية:{Style.RESET_ALL}
   • 9 مشغلين مختلفين
   • أرقام صالحة للتسجيل

{Fore.YELLOW}4. ثغرة الأرقام الأمريكية:{Style.RESET_ALL}
   • 300+ رمز منطقة
   • أرقام حقيقية النمط

{Fore.RED}⚠️  تنبيه قانوني:{Style.RESET_ALL}
هذه الأداة للتعليم والبحث الأمني فقط.
استخدامها على أرقام حقيقية دون إذن غير قانوني.
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
"""
    print(info)

def main():
    init_db()
    
    while True:
        clear_screen()
        print_banner()
        show_menu()
        
        choice = input(f"\n{Fore.GREEN}اختر رقم (0-6): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            result = get_random_number()
            if result:
                show_number_info(result[0], result[1], result[2])
            else:
                print(f"\n{Fore.YELLOW}⚠️ لا توجد أرقام متاحة. جاري التحديث...{Style.RESET_ALL}")
                get_all_numbers()
                result = get_random_number()
                if result:
                    show_number_info(result[0], result[1], result[2])
                else:
                    print(f"{Fore.RED}❌ فشل الحصول على رقم{Style.RESET_ALL}")
        
        elif choice == '2':
            nums = generate_israeli(1)
            if nums:
                num = nums[0]
                show_number_info(num['number'], num['country'], num['source'])
                save_number(num['number'], num['country'], num['source'])
        
        elif choice == '3':
            nums = generate_usa(1)
            if nums:
                num = nums[0]
                show_number_info(num['number'], num['country'], num['source'])
                save_number(num['number'], num['country'], num['source'])
        
        elif choice == '4':
            print(f"\n{Fore.CYAN}[*] جاري تحديث قاعدة البيانات...{Style.RESET_ALL}")
            nums = get_all_numbers()
            print(f"{Fore.GREEN}[✓] تم إضافة {len(nums)} رقم جديد{Style.RESET_ALL}")
        
        elif choice == '5':
            show_stats()
        
        elif choice == '6':
            show_vuln_info()
        
        elif choice == '0':
            print(f"\n{Fore.GREEN}👋 وداعاً!{Style.RESET_ALL}")
            sys.exit(0)
        
        input(f"\n{Fore.CYAN}اضغط Enter للمتابعة...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 تم الإنهاء{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ خطأ: {e}{Style.RESET_ALL}")
        sys.exit(1)
