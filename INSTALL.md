# Installation Guide for Ubuntu/Linux

## Quick Install (Recommended)

```bash
# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Install Python dependencies
pip3 install -r requirements.txt

# Run the scraper
python3 main.py
```

## Alternative: Use Chromium

```bash
# Install Chromium
sudo apt update
sudo apt install chromium-browser

# Install Python dependencies
pip3 install -r requirements.txt

# Run the scraper
python3 main.py
```

## Alternative: Use Firefox

```bash
# Install Firefox
sudo apt update
sudo apt install firefox

# Install Python dependencies
pip3 install -r requirements.txt

# Run the scraper
python3 main.py
```

## Verify Installation

```bash
# Check if Chrome is installed
google-chrome --version

# Or check Chromium
chromium-browser --version

# Or check Firefox
firefox --version

# Test the scraper setup
python3 test_setup.py
```

## Troubleshooting

### "No browser found" error
Install one of the browsers above.

### Permission denied
Run: `sudo apt-get install -f`

### Flatpak/Snap issues
If using VSCodium via Flatpak, install Chrome system-wide (not as Flatpak).
