# 📱 M.O.L.O.C.H. 3.0 - XIAOMI/MIUI/HyperOS Setup Guide

**Spezifisch für: Xiaomi Redmi Note 13 Pro+**

---

## ⚠️ WARUM DIESER GUIDE?

Xiaomi/MIUI/HyperOS hat **sehr aggressive** Battery & Permission Management!

**Ohne diese Fixes:**
- ❌ Termux wird im Background getötet
- ❌ Camera Access wird geblockt
- ❌ Microphone funktioniert nicht
- ❌ M.O.L.O.C.H. stoppt nach paar Minuten

**Mit diesen Fixes:**
- ✅ M.O.L.O.C.H. läuft stabil
- ✅ Voice Mode funktioniert
- ✅ Vision Mode funktioniert
- ✅ Background Execution möglich

---

## 🔧 SETUP CHECKLIST

### ☑️ **Phase 1: Battery Optimization**

**KRITISCH - Sonst wird Termux getötet!**

1. **Battery Saver OFF für Termux:**
   ```
   Settings → Battery & Performance
     → Battery
     → Battery Saver
     → Apps
     → Termux → No restrictions
     → Termux:API → No restrictions
   ```

2. **App Battery Saver OFF:**
   ```
   Settings → Battery
     → App battery saver
     → Termux → No restrictions
     → Termux:API → No restrictions
   ```

3. **Background Restriction OFF:**
   ```
   Settings → Apps
     → Manage apps
     → Termux
     → Battery saver → No restrictions
     → Background restriction → OFF
   ```

4. **Autostart ENABLE:**
   ```
   Settings → Apps
     → Manage apps
     → Termux
     → Other permissions
     → Autostart → ✅ ENABLE
   ```

---

### ☑️ **Phase 2: Permissions Setup**

**Camera & Microphone für M.O.L.O.C.H.:**

1. **Termux:API Permissions:**
   ```
   Settings → Apps
     → Manage apps
     → Termux:API
     → App permissions
       → Camera → ✅ Allow
       → Microphone → ✅ Allow
       → Storage → ✅ Allow
   ```

2. **Display Over Apps:**
   ```
   Settings → Apps
     → Manage apps
     → Termux:API
     → Other permissions
     → Display over other apps → ✅ ENABLE
   ```

3. **Background Camera (wenn verfügbar):**
   ```
   Settings → Privacy
     → Permissions
     → Camera
     → Termux:API
     → Allow in background (if available)
   ```

---

### ☑️ **Phase 3: Developer Options (Optional aber empfohlen)**

**Für maximale Stabilität:**

1. **Developer Options aktivieren:**
   ```
   Settings → About phone
     → MIUI version → 10x tippen
     → "You are now a developer!"
   ```

2. **Settings optimieren:**
   ```
   Settings → Additional settings
     → Developer options
       → Don't keep activities → ✅ OFF
       → Background process limit → Standard limit
       → MIUI optimization → ✅ OFF (requires restart)
   ```

---

### ☑️ **Phase 4: MIUI Privacy Protection**

**Spezielle MIUI Features:**

```
Settings → Privacy Protection
  → Special app access
  → Termux:API → ✅ All enabled
```

```
Settings → Privacy
  → Protection
  → Manage apps
  → Termux:API → Trusted
```

---

## 🧪 TESTING

### **Test 1: Battery Optimization**

```bash
# Start M.O.L.O.C.H.
python ~/moloch_3.0/moloch3.py -i

# Lock phone
# Wait 5 minutes
# Unlock phone
# Check if Termux still running

✅ Running → Battery Optimization OFF
❌ Killed → Check Battery Settings again!
```

### **Test 2: Camera Access**

```bash
# Test camera
termux-camera-photo ~/test.jpg

# Check if photo exists
ls -lh ~/test.jpg

✅ Photo exists → Camera works
❌ Permission denied → Check Camera Permissions
```

### **Test 3: Microphone Access**

```bash
# Test microphone
termux-microphone-record -f ~/test.wav -l 5

# Check if audio exists
ls -lh ~/test.wav

✅ Audio exists → Microphone works
❌ Permission denied → Reinstall Termux:API
```

### **Test 4: Full M.O.L.O.C.H. Test**

```bash
# Text Mode
python ~/moloch_3.0/moloch3.py -t "Hey Moloch, bist du da?"
# Should respond!

# Voice Mode (if microphone works)
python ~/moloch_3.0/moloch3.py
# Should say "Ja?" and record

# Vision Mode (if camera works)
python ~/moloch_3.0/moloch3.py -a "Was siehst du?"
# Should take photo and describe
```

---

## 🚨 TROUBLESHOOTING

### **Problem: Termux wird getötet**

**Symptom:** Termux stoppt nach paar Minuten

**Lösung:**
1. Check Battery Saver → No restrictions
2. Check Autostart → Enabled
3. Check Background restriction → OFF
4. Reboot phone

### **Problem: Camera Permission Denied**

**Symptom:** `termux-camera-photo` error

**Lösung:**
1. Termux:API neu installieren (F-Droid)
2. Permissions beim Start erlauben
3. Check Display Over Apps → Enabled
4. Phone neustarten

### **Problem: Microphone funktioniert nicht**

**Symptom:** Keine Audio Aufnahme

**Lösung:**
1. Termux:API deinstallieren
2. Phone neustarten
3. Termux:API neu installieren (F-Droid!)
4. Bei Permission Prompt: ALLOW
5. Test: `termux-microphone-record -h`

### **Problem: "MIUI Optimization" blockt**

**Symptom:** Verschiedene weird Bugs

**Lösung:**
```
Developer Options → MIUI optimization → OFF
Phone restart
```

---

## 📱 XIAOMI-SPECIFIC TIPPS

### **1. Termux:Float verwenden**

Für bessere Background Performance:
```bash
pkg install termux-float
```

Termux als Floating Window → wird weniger aggressiv getötet!

### **2. Termux:Boot für Autostart**

```bash
pkg install termux-boot

mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-moloch.sh

# Add:
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/moloch_3.0
```

### **3. Keep-Alive Script**

```bash
# Für lange Sessions:
termux-wake-lock
# Verhindert phone sleep → hält Termux aktiv
```

---

## 🔗 WICHTIGE LINKS

### **Don't Kill My App - Xiaomi Guide:**
https://dontkillmyapp.com/xiaomi

### **Termux Wiki - Xiaomi:**
https://wiki.termux.com/wiki/Termux-api

### **XDA Forums - Redmi Note 13 Pro:**
https://xdaforums.com/f/redmi-note-13-pro.12865/

---

## ✅ FINAL CHECKLIST

Vor M.O.L.O.C.H. 3.0 Start:

- [ ] Battery Saver → No restrictions (Termux + Termux:API)
- [ ] Autostart → Enabled (Termux)
- [ ] Background restriction → OFF (Termux)
- [ ] Camera Permission → Allow (Termux:API)
- [ ] Microphone Permission → Allow (Termux:API)
- [ ] Display Over Apps → Enabled (Termux:API)
- [ ] Developer Options → MIUI optimization OFF (optional)
- [ ] Phone restarted nach allen Änderungen

**Dann:**
```bash
cd ~/moloch_3.0
python moloch3.py -t "Test"
```

**Wenn läuft: 🎉 READY TO GO!**

---

## 🖤 XIAOMI IST HART - ABER MACHBAR!

Mit diesen Settings sollte M.O.L.O.C.H. 3.0 auf deinem **Redmi Note 13 Pro+** laufen!

**Erfahrung:** Nach Setup ist Xiaomi actually sehr stabil für Termux!

**Let's go, Alter! 🚀**
