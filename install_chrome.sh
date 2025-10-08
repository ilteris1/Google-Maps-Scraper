#!/bin/bash
# Quick Chrome installation script for Ubuntu/Linux

echo "Installing Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y
rm google-chrome-stable_current_amd64.deb

echo "Verifying installation..."
google-chrome --version

echo "Done! Now run: python3 main.py"
