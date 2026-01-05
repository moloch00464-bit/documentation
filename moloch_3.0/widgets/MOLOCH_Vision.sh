#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Vision Mode Widget
# ======================================
# Homescreen Button: Photo + Vision
#

# Load API Keys from ~/.bashrc
source ~/.bashrc

cd ~/documentation/moloch_3.0

# Run with error capture and keep terminal open
python3 moloch3_unified.py -v 2>&1

# Keep terminal open to see result
echo ""
echo "=================================="
echo "Drücke ENTER zum Schließen..."
echo "=================================="
read
