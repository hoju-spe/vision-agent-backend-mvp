#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/vision-agent-backend-mvp}"

echo "[1/5] Updating apt packages"
sudo apt-get update -y

echo "[2/5] Installing Docker, Compose plugin, and Git"
sudo apt-get install -y ca-certificates curl gnupg git
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[3/5] Enabling Docker service"
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker "$USER"

echo "[4/5] Preparing app data directories"
mkdir -p "$APP_DIR/data/uploads" "$APP_DIR/data/results"

echo "[5/5] Setup complete"
echo "Log out and reconnect once so the docker group permission is applied."
echo "Then run: cd $APP_DIR && docker compose up -d --build"
