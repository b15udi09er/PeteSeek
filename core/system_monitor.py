import psutil
import subprocess
import re
from datetime import datetime

class SystemMonitor:
    def get_status(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        ping = self._ping("8.8.8.8")
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        
        return (
            f"CPU: {cpu}% {'🚀' if cpu < 50 else '💀'}\n"
            f"RAM: {ram}% {'🍃' if ram < 70 else '🔥'}\n"
            f"Ping: {ping}ms {'⚡' if ping < 100 else '🐢'}\n"
            f"Uptime: {str(uptime).split('.')[0]} ⏳"
        )

    def check_cpu_emergency(self):
        cpu = psutil.cpu_percent()
        if cpu > 90:
            return f"🚨 **CPU CRISIS** ({cpu}%) - I'M MELTING!"
        elif cpu > 75:
            return f"⚠️ **CPU WARNING** ({cpu}%) - This hurts..."
        return None

    def _ping(self, ip):
        try:
            result = subprocess.run(["ping", "-c", "3", ip], capture_output=True, text=True)
            match = re.search(r"min/avg/max/.+? = (\d+\.\d+)", result.stdout)
            return float(match.group(1)) if match else 999.99
        except:
            return 999.99