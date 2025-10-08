#!/bin/bash
echo "Searching for Chrome installation..."
echo ""

# Check common locations
for path in /usr/bin/google-chrome /usr/bin/google-chrome-stable /opt/google/chrome/google-chrome /usr/bin/chromium-browser /usr/bin/chromium; do
    if [ -f "$path" ]; then
        echo "✓ Found: $path"
        $path --version
        echo ""
        echo "Add this to config.py:"
        echo "CHROME_BINARY_PATH = '$path'"
        exit 0
    fi
done

echo "✗ Chrome not found in standard locations"
echo ""
echo "Please run outside Flatpak/Snap environment:"
echo "  which google-chrome"
