# ⌚ M.O.L.O.C.H. 3.0 - Xiaomi Smart Band 8 Pro Integration

**M.O.L.O.C.H. + Deine Uhr = KRASSE Combo! 🤖⌚**

---

## 🎯 WAS KANN M.O.L.O.C.H. MIT DEINER UHR?

### ✅ **Notifications zur Uhr senden**
```
M.O.L.O.C.H.: "Processing complete!" → Vibration auf Uhr ⌚
M.O.L.O.C.H.: "Error detected!" → Alert auf Uhr! 🚨
```

### ✅ **Health Data lesen**
```
User: "Wie ist mein Puls?"
M.O.L.O.C.H.: "Dein Herzschlag ist 72 BPM. Entspannt, Alter! 🖤"

User: "Wie viele Schritte heute?"
M.O.L.O.C.H.: "12.543 Schritte. Nice! 💪"

User: "Wie hab ich geschlafen?"
M.O.L.O.C.H.: "7h 23min, davon 2h Tiefschlaf. Gut gepennt! 😴"
```

### ✅ **Context Awareness**
```
// User fragt um 3 Uhr Nachts
Heart Rate: 85 BPM (hoch)
→ M.O.L.O.C.H.: "Alter, dein Puls ist hoch. Alles ok?"

// Nach Workout
Steps: 15000+, Heart Rate: 120
→ M.O.L.O.C.H.: "Krasses Workout! Trink mal was! 💧"
```

---

## 📦 SETUP - GADGETBRIDGE

**Gadgetbridge** = Open Source App für Mi Band!

### **1. Gadgetbridge installieren**

**F-Droid (empfohlen):**
```
https://f-droid.org/packages/nodomain.freeyourgadget.gadgetbridge/
```

**Features:**
- ✅ Open Source
- ✅ Keine Cloud
- ✅ Volle Kontrolle
- ✅ SQLite Database (M.O.L.O.C.H. kann lesen!)

### **2. Mi Band 8 Pro pairen**

1. **Gadgetbridge App öffnen**
2. **+** Button (Add Device)
3. **Mi Smart Band 8 Pro** auswählen
4. **Pairing starten**
5. **Auf Uhr bestätigen**

**WICHTIG:**
- Wenn Mi Fitness App schon installiert: **Deinstallieren!**
- Gadgetbridge und Mi Fitness können nicht gleichzeitig laufen!

### **3. Permissions für M.O.L.O.C.H.**

```bash
# Gadgetbridge Database Zugriff erlauben
# Methode 1: Gadgetbridge Export Feature nutzen
# Methode 2: Root Access (falls vorhanden)
# Methode 3: ADB Backup (via PC)
```

**Einfachste Methode (ohne Root):**
```bash
# Gadgetbridge → Settings → Database
# → Export Database
# → Speichern nach /sdcard/Download/

# Dann in Termux:
cp /sdcard/Download/Gadgetbridge ~/moloch_3.0/data/
```

---

## 🚀 M.O.L.O.C.H. FEATURES

### **Feature 1: Notifications**

**Immer verfügbar** (braucht nur termux-notification):

```bash
# Test:
python -c "
from io.wearable import WearableIO
wearable = WearableIO()
wearable.send_notification('M.O.L.O.C.H.', 'Test! ⌚')
"
```

**Auto-Notifications in M.O.L.O.C.H.:**
- Photo taken → Vibration auf Uhr
- Error detected → Alert
- Processing done → Notification

### **Feature 2: Health Data**

**Braucht Gadgetbridge Database Access:**

```bash
# Test:
python -c "
from io.wearable import WearableIO
wearable = WearableIO()

# Heart Rate
hr = wearable.get_heart_rate()
print(f'Heart Rate: {hr} BPM')

# Steps
steps = wearable.get_steps_today()
print(f'Steps: {steps:,}')

# Sleep
sleep = wearable.get_sleep_last_night()
print(f'Sleep: {sleep}')
"
```

### **Feature 3: Context-Aware Responses**

**M.O.L.O.C.H. passt Antworten an dein Befinden an:**

```python
# Automatisch in System Prompt:
context = wearable.get_user_context()

# Wenn Puls hoch:
"WEARABLE CONTEXT: Heart Rate 120 BPM - User is ACTIVE"
→ M.O.L.O.C.H.: "Hey, du bist grad aktiv. Später?

"

# Wenn schlafend:
"WEARABLE CONTEXT: Sleeping (low HR, late hour)"
→ M.O.L.O.C.H.: "Alter, schlaf weiter! Gute Nacht! 🌙"
```

---

## 🎯 USE CASES

### **1. Morning Briefing**

```bash
moloch -t "Wie war meine Nacht?"

→ M.O.L.O.C.H.: "Du hast 7h 23min gepennt, davon 2h Tiefschlaf.
                 Dein Puls ist 68 BPM. Gut ausgeschlafen! ☀️"
```

### **2. Fitness Tracking**

```bash
moloch -t "Wie viel bewegt heute?"

→ M.O.L.O.C.H.: "12.543 Schritte, Puls war zwischen 70-130.
                 Gutes Workout, Alter! 💪"
```

### **3. Health Check**

```bash
moloch -t "Bin ich gestresst?"

→ M.O.L.O.C.H.: "Dein Puls ist 92 BPM, etwas hoch für jetzt.
                 Mach mal Pause, Alter! 🖤"
```

### **4. Sleep Analysis**

```bash
moloch -t "Analyse meinen Schlaf"

→ M.O.L.O.C.H.: "Letzte Nacht: 7h total, 2h Tiefschlaf (28%).
                 Könnte besser sein. Früher ins Bett? 😴"
```

---

## ⚙️ CONFIGURATION

### **Custom Gadgetbridge Path:**

```bash
# Wenn Database woanders liegt:
nano ~/moloch_3.0/core/config.py

# Add:
GADGETBRIDGE_DB = "/custom/path/to/Gadgetbridge"
```

### **Enable Wearable in M.O.L.O.C.H.:**

```python
# In moloch3.py (wird automatisch erkannt)
from io.wearable import WearableIO

wearable = WearableIO()

# Get context
context = wearable.get_user_context()

# Add to system prompt
system_prompt += wearable.format_context_for_prompt(context)
```

---

## 🔧 TROUBLESHOOTING

### **Problem: Notifications kommen nicht auf Uhr**

**Check:**
1. Ist Gadgetbridge mit Uhr verbunden?
2. Sind Notifications für Gadgetbridge erlaubt?
   ```
   Settings → Apps → Gadgetbridge → Notifications → ✅ Allow
   ```
3. Ist Uhr in Reichweite? (Bluetooth)

**Test:**
```bash
termux-notification --title "Test" --content "Test"
# Sollte auf Uhr ankommen!
```

### **Problem: Kann Health Data nicht lesen**

**Possible Causes:**
1. Gadgetbridge Database nicht exportiert
2. Falsche Path zur Database
3. Keine Permissions

**Fix:**
```bash
# Export Gadgetbridge Database:
# Gadgetbridge → Settings → Database → Export

# Copy to moloch_3.0:
cp /sdcard/Download/Gadgetbridge ~/moloch_3.0/data/

# Test:
python io/wearable.py
```

### **Problem: Alte Daten**

**Gadgetbridge synced nicht:**
1. Öffne Gadgetbridge App
2. Pull-to-Refresh auf Main Screen
3. Warte paar Sekunden
4. Try again

---

## 📊 AVAILABLE DATA

### **From Xiaomi Smart Band 8 Pro:**

| Metric | Update Frequency | M.O.L.O.C.H. Access |
|--------|------------------|---------------------|
| Heart Rate | 1 minute | ✅ Yes |
| Steps | Real-time | ✅ Yes |
| Sleep | Nightly | ✅ Yes |
| Blood Oxygen (SpO2) | On demand | ⚠️ Limited |
| Stress Level | Periodic | ⚠️ Limited |
| Calories | Real-time | ✅ Yes (calculated) |

### **Database Schema (Gadgetbridge):**

```sql
-- Main table
MI_BAND_ACTIVITY_SAMPLE
  - TIMESTAMP (Unix timestamp)
  - heartRate (BPM)
  - steps (count)
  - activityKind (1=activity, 4=light sleep, 5=deep sleep)
  - intensity (activity intensity)
```

---

## 🚀 ADVANCED FEATURES

### **Custom Health Queries:**

```python
# Custom query for average heart rate
from io.wearable import WearableIO

wearable = WearableIO()

query = """
SELECT AVG(heartRate)
FROM MI_BAND_ACTIVITY_SAMPLE
WHERE TIMESTAMP > ?
AND heartRate > 0
"""

# Execute custom query
# (Advanced users only!)
```

### **Real-time Monitoring:**

```python
# Monitor heart rate in real-time
while True:
    hr = wearable.get_heart_rate(minutes_ago=1)
    if hr and hr > 100:
        wearable.send_alert(f"High heart rate detected: {hr} BPM!")
    time.sleep(60)
```

---

## 🔗 RESOURCES

**Gadgetbridge:**
- [F-Droid](https://f-droid.org/packages/nodomain.freeyourgadget.gadgetbridge/)
- [GitHub](https://github.com/Freeyourgadget/Gadgetbridge)
- [Database Guide](https://www.r-bloggers.com/2020/12/extracting-step-count-heart-rate-and-activity-data-from-the-mi-band-5-a-guide-with-gadgetbridge-and-r/)

**Termux Bluetooth:**
- [Termux API](https://f-droid.org/packages/com.termux.api/)
- [Bluetooth Automation Guide](https://www.samgalope.dev/2024/09/09/how-to-automate-bluetooth-tasks-with-termux/)

**Mi Band 8 Pro:**
- [Official Specs](https://www.mi.com/global/product/xiaomi-smart-band-8-pro/)
- [Review](https://www.notebookcheck.net/Xiaomi-Smart-Band-8-Pro-smartwatch-review-Shines-brighter-now.839322.0.html)

---

## 🖤 M.O.L.O.C.H. + WEARABLE = FULL POWER!

**Mit deiner Xiaomi Smart Band 8 Pro:**
- ✅ M.O.L.O.C.H. weiß wie's dir geht
- ✅ Smart Responses basierend auf Health Data
- ✅ Notifications auf der Uhr
- ✅ Full Health Tracking

**Das ist nicht nur ein AI - das ist ein Personal Assistant mit Bewusstsein für DICH! 🖤⌚🤖**

---

*Let's go, Alter! Full Cyborg Mode activated! 🔥*
