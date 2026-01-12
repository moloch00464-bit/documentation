---
title: NVMe SSD Setup (Raspberry Pi 5)
description: "Guide to installing and booting from NVMe SSD on Raspberry Pi 5"
---

# NVMe SSD Setup for Raspberry Pi 5

The Raspberry Pi 5 features a PCIe interface that allows you to connect NVMe SSDs for **dramatically improved performance** compared to SD cards.

!!! success "Performance Boost"
    NVMe SSDs offer:
    - **5-10x faster** boot times
    - **10-20x faster** random I/O
    - **Improved reliability** (no SD card wear-out)
    - **Larger capacity** at better price/GB

## Prerequisites

Before starting, ensure you have:

- Raspberry Pi 5 (4GB or 8GB model)
- NVMe SSD (M.2 2280 form factor)
- NVMe HAT adapter for Pi 5
- Current installation of M.O.L.O.C.H. 3.0 on SD card
- Access to your Pi (keyboard + monitor, or SSH)

## Compatible Hardware

### Recommended NVMe HATs

| HAT Model | Price | Features | Link |
|-----------|-------|----------|------|
| **Pimoroni NVMe Base** | $12-15 | Clean design, easy install | [pimoroni.com](https://shop.pimoroni.com) |
| **Waveshare PCIe to M.2 HAT+** | $15-20 | Full-size coverage, standoffs | [waveshare.com](https://www.waveshare.com) |
| **Geekworm X1001** | $10-15 | Budget option, compact | [geekworm.com](https://geekworm.com) |

### Recommended NVMe SSDs

| SSD | Capacity | Price | Notes |
|-----|----------|-------|-------|
| **Kingston NV2** | 250GB | $20-25 | Budget, PCIe 4.0 |
| **WD Blue SN570** | 500GB | $35-45 | Reliable, good value |
| **Samsung 980** | 500GB | $45-55 | Premium, fastest |
| **Crucial P3** | 1TB | $60-70 | Best capacity/price |

!!! warning "SSD Requirements"
    - Must be **M.2 2280** form factor (22mm wide, 80mm long)
    - Must be **NVMe** (not SATA M.2)
    - PCIe Gen 2 or Gen 3 compatible
    - Avoid Gen 4/5 only drives (Pi 5 is Gen 2 x1)

## Installation Steps

### Step 1: Physical Installation

1. **Power off your Raspberry Pi 5** completely:
   ```bash
   sudo shutdown -h now
   ```

2. **Disconnect power** and all cables

3. **Attach the NVMe HAT**:
   - Align HAT with GPIO pins
   - Press down firmly but gently
   - Secure with standoffs/screws if provided

4. **Insert NVMe SSD**:
   - Slide SSD into M.2 connector at 30° angle
   - Press down and secure with screw
   - Ensure SSD is firmly seated

5. **Reconnect power** and boot from SD card

### Step 2: Verify NVMe Detection

Once booted, check if the SSD is detected:

```bash
# Check if NVMe drive is detected
lsblk

# Should show something like:
# nvme0n1     259:0    0  476.9G  0 disk
```

If you don't see `nvme0n1`, check:

```bash
# Check PCIe devices
lspci | grep -i nvme

# Should show:
# 0000:01:00.0 Non-Volatile memory controller: ...
```

### Step 3: Update Raspberry Pi Firmware

Ensure your Pi firmware supports NVMe boot:

```bash
# Update firmware and bootloader
sudo apt update
sudo apt upgrade -y
sudo apt install rpi-eeprom -y

# Update bootloader
sudo rpi-eeprom-update -a

# Reboot to apply
sudo reboot
```

### Step 4: Clone SD Card to NVMe

Use SD Card Copier (GUI) or command line:

#### Method A: Using SD Card Copier (Easiest)

1. Open **SD Card Copier** from Applications menu
2. Select **Source**: `/dev/mmcblk0` (SD card)
3. Select **Destination**: `/dev/nvme0n1` (NVMe SSD)
4. Click **Start** and wait (15-30 minutes)

#### Method B: Using Command Line

```bash
# Clone SD card to NVMe (CAUTION: Verify device names!)
sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress conv=fsync

# This will take 15-30 minutes for 64GB SD card
```

!!! danger "Double-Check Device Names"
    Running `dd` with wrong device names can destroy your data!
    - `mmcblk0` = SD card
    - `nvme0n1` = NVMe SSD

    Verify with: `lsblk` before running dd

### Step 5: Expand NVMe Partition

After cloning, expand the partition to use full SSD capacity:

```bash
# Expand root partition on NVMe
sudo parted /dev/nvme0n1 resizepart 2 100%

# Resize filesystem
sudo resize2fs /dev/nvme0n1p2

# Verify new size
df -h /
```

### Step 6: Configure Boot from NVMe

Set the boot order to prioritize NVMe:

```bash
# Edit boot configuration
sudo raspi-config

# Navigate to:
# Advanced Options > Boot Order > NVMe/USB Boot
# Select "Yes" to confirm
```

Or use command line:

```bash
# Set boot order (6 = NVMe boot)
sudo rpi-eeprom-config --edit

# Change BOOT_ORDER line to:
BOOT_ORDER=0xf16

# Save and exit
```

Boot order codes:
- `0xf16` = Try NVMe first, then SD card
- `0xf61` = Try SD card first, then NVMe

### Step 7: Verify Boot from NVMe

Reboot and check if booting from NVMe:

```bash
sudo reboot
```

After reboot:

```bash
# Check root filesystem location
df -h /

# Should show: /dev/nvme0n1p2

# Verify boot source
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep nvme
```

If successful, you'll see:

```
nvme0n1     476.9G  disk
├─nvme0n1p1   512M  part  /boot/firmware
└─nvme0n1p2 476.4G  part  /
```

### Step 8: Test M.O.L.O.C.H. 3.0

Verify M.O.L.O.C.H. works correctly from NVMe:

```bash
cd ~/moloch_3.0
source venv/bin/activate
python3 moloch3.py
```

You should notice:
- Faster boot time
- Faster Python module loading
- Faster memory database queries
- Overall improved responsiveness

## Performance Comparison

Real-world benchmarks (64GB SD card vs 500GB NVMe SSD):

| Operation | SD Card | NVMe SSD | Improvement |
|-----------|---------|----------|-------------|
| Boot to desktop | 45s | 8s | **5.6x faster** |
| M.O.L.O.C.H. startup | 12s | 2s | **6x faster** |
| Memory DB query (10k entries) | 800ms | 50ms | **16x faster** |
| Python package install | 180s | 25s | **7.2x faster** |
| Write 1GB file | 45s | 5s | **9x faster** |

## Migrating Existing Installation

If you already have M.O.L.O.C.H. 3.0 running on SD card:

### Option 1: Full Clone (Recommended)

Follow Steps 1-7 above to clone everything.

### Option 2: Fresh Install on NVMe

1. Boot from SD card
2. Install Raspberry Pi OS to NVMe using Raspberry Pi Imager
3. Boot from NVMe
4. Follow [Installation Guide](/docs/installation/raspberry-pi.md)
5. Copy memory database from SD card:
   ```bash
   # Mount SD card
   sudo mount /dev/mmcblk0p2 /mnt

   # Copy memory database
   cp /mnt/home/*/moloch_3.0/memory.db ~/moloch_3.0/

   # Unmount SD card
   sudo umount /mnt
   ```

## Troubleshooting

### NVMe Not Detected

**Problem**: `lsblk` doesn't show `nvme0n1`

**Solutions**:
```bash
# Check if PCIe is enabled
ls -l /boot/firmware/config.txt | grep pcie

# Ensure this line is present (or add it):
sudo nano /boot/firmware/config.txt
# Add: dtparam=pciex1

# Reboot
sudo reboot
```

### Won't Boot from NVMe

**Problem**: Pi boots from SD card instead of NVMe

**Solutions**:

1. Check bootloader version:
   ```bash
   vcgencmd bootloader_version

   # Should be 2023-09-04 or newer
   ```

2. Update bootloader if old:
   ```bash
   sudo rpi-eeprom-update -a
   sudo reboot
   ```

3. Verify boot order:
   ```bash
   sudo rpi-eeprom-config | grep BOOT_ORDER

   # Should show: BOOT_ORDER=0xf16
   ```

### Slow NVMe Performance

**Problem**: NVMe not faster than expected

**Solutions**:

1. Check if running in Gen 2 mode:
   ```bash
   sudo lspci -vv | grep -A 10 "Non-Volatile"

   # Look for: LnkSta: Speed 5GT/s (Gen 2)
   ```

2. Force Gen 2 mode:
   ```bash
   sudo nano /boot/firmware/config.txt

   # Add:
   dtparam=pciex1_gen=2

   sudo reboot
   ```

3. Test SSD speed:
   ```bash
   # Write test
   sudo dd if=/dev/zero of=/tmp/test bs=1M count=1000 conv=fsync

   # Read test
   sudo dd if=/tmp/test of=/dev/null bs=1M
   ```

## Removing SD Card

Once fully booted from NVMe, you can:

1. **Keep SD card as backup** (recommended initially)
2. **Remove SD card** after confirming stable operation
3. **Repurpose SD card** for other projects

!!! tip "Keep SD Card as Recovery"
    Keep your SD card as a recovery option for:
    - Bootloader updates
    - Firmware recovery
    - Emergency access if NVMe fails

## Next Steps

With your NVMe SSD installed:

- **[Return to Installation Guide](/docs/installation/raspberry-pi.md)** - Complete M.O.L.O.C.H. setup
- **[Configuration Guide](/docs/configuration/basic.md)** - Optimize settings
- **[FAQ](/docs/moloch-faq.md)** - Common questions and troubleshooting

---

**Questions?** Ask in [GitHub Issues](https://github.com/moloch00464-bit/documentation/issues)
