#!/bin/bash
set -e

# Clone repo
git clone https://github.com/b15udi09er/PeteSeek.git /opt/peteseek
cd /opt/peteseek

# Secure token
mkdir -p config
chmod 700 config
echo "PASTE_YOUR_TOKEN_HERE" > config/token.txt
chmod 600 config/token.txt

# Python setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd service
sudo tee /etc/systemd/system/peteseek.service > /dev/null <<EOF
[Unit]
Description=PeteSeek Bot
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=/opt/peteseek
ExecStart=/opt/peteseek/venv/bin/python /opt/peteseek/core/discord_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now peteseek
echo "✅ Installed! Check status with: systemctl status peteseek"