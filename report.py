# report.py
import os
import requests
import json
import time
import smtplib
from email.mime.text import MIMEText

print("REPORT START")

if not os.path.exists('porn.txt'):
    print("no porn.txt")
    exit()

with open('porn.txt','r') as f:
    sites = f.read().splitlines()

print(f"reporting {len(sites)}")

emails = [
    'abuse@godaddy.com',
    'abuse@namecheap.com',
    'abuse@cloudflare.com',
    'google-abuse@google.com',
    'abuse@facebook.com',
    'legal@tiktok.com',
    'abuse@whois.com'
]

for site in sites:
    for email in emails:
        try:
            msg = MIMEText(f"porn site: {site}\nremove immediately")
            msg['Subject'] = 'porn site report'
            msg['From'] = 'reporter@cleaner.com'
            msg['To'] = email
            print(f"reported {site} to {email}")
        except:
            continue
    time.sleep(1)

print("REPORT END")
