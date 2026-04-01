#!/bin/bash
# Run this on your GCE VM after cloning the repo
# Usage: bash deploy/setup.sh chat.yourdomain.com

set -e

DOMAIN=${1:?"Usage: bash deploy/setup.sh <your-domain>"}
USER=$(whoami)
REPO_DIR=$(pwd)

echo "=== Installing Node.js 24 ==="
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs nginx certbot python3-certbot-nginx

echo "=== Installing dependencies ==="
cd "$REPO_DIR/server" && npm install
cd "$REPO_DIR/client" && npm install

echo "=== Writing production .env ==="
cat > "$REPO_DIR/client/.env.production" <<EOF
VITE_API_URL=https://$DOMAIN/api
VITE_SOCKET_URL=https://$DOMAIN
EOF

echo "=== Building frontend ==="
cd "$REPO_DIR/client" && npm run build

echo "=== Setting up Nginx ==="
sudo sed -e "s|chat.yourdomain.com|$DOMAIN|g" \
         -e "s|YOUR_USER|$USER|g" \
         -e "s|/home/$USER/messaging|$REPO_DIR|g" \
         "$REPO_DIR/deploy/nginx.conf" | sudo tee /etc/nginx/sites-available/messaging > /dev/null

sudo ln -sf /etc/nginx/sites-available/messaging /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo "=== Getting SSL certificate ==="
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email

echo "=== Starting backend with PM2 ==="
sudo npm install -g pm2
cd "$REPO_DIR"
pm2 start deploy/ecosystem.config.js
pm2 save
pm2 startup | tail -1 | bash

echo ""
echo "=== Done! ==="
echo "Your app is live at https://$DOMAIN"
echo ""
echo "Don't forget to add $DOMAIN to Firebase authorized domains:"
echo "  Firebase Console > Authentication > Settings > Authorized domains"
