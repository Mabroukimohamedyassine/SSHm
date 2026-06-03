#!/usr/bin/env bash
set -e

INSTALL_DIR="/opt/sshm"
BIN_PATH="/usr/local/bin/sshm"

GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m"

print_step() {
  printf "${BLUE}==>${NC} %s\n" "$1"
}

print_ok() {
  printf "${GREEN}✔${NC} %s\n" "$1"
}

print_warn() {
  printf "${YELLOW}!${NC} %s\n" "$1"
}

print_err() {
  printf "${RED}✖${NC} %s\n" "$1"
}

printf "${GREEN}\n  SSHm Installer\n${NC}"
printf "${BLUE}  -----------------------------${NC}\n\n"

print_step "Copying files to ${INSTALL_DIR}"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r . "$INSTALL_DIR/"
print_ok "Files copied"

print_step "Creating isolated Python environment"
sudo python3 -m venv "$INSTALL_DIR/venv"
print_ok "Virtual environment created"

print_step "Installing dependencies"
sudo "$INSTALL_DIR/venv/bin/pip" install -q -r "$INSTALL_DIR/requirements.txt"
print_ok "Dependencies installed"

print_step "Installing CLI wrapper to ${BIN_PATH}"
sudo tee "$BIN_PATH" > /dev/null << 'EOF'
#!/usr/bin/env bash
exec /opt/sshm/venv/bin/python /opt/sshm/main.py "$@"
EOF
sudo chmod +x "$BIN_PATH"
print_ok "Wrapper installed"

if [ ! -f "$INSTALL_DIR/.env" ]; then
    print_warn "Don't forget: echo 'GROQ_API_KEY=sk-...' > /opt/sshm/.env"
fi

printf "\n${GREEN}Done.${NC} Run: ${BLUE}sshm${NC}\n"
