# 📱 PodridaScoring - Android App Guide

Complete guide for converting and building your Flask application as a native Android app.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Build Guide](#build-guide)
4. [Technical Documentation](#technical-documentation)
5. [Conversion Summary](#conversion-summary)
6. [Troubleshooting](#troubleshooting)

---

# Overview

## 🎯 What is this?

Your Flask application **PodridaScoring** can now run as a **native Android app** that works completely **offline** without the need for external web servers (Render, Heroku, etc.).

## 🔑 Key Concepts

### How does it work?

```
┌────────────────────────┐
│   Android App          │
│  ┌──────────────────┐  │
│  │   MainActivity   │  │
│  │   (Kotlin)       │  │
│  └────────┬─────────┘  │
│           │            │
│  ┌────────▼─────────┐  │
│  │   WebView        │  │ ← User sees this
│  │  (localhost:5000)│  │
│  └────────▲─────────┘  │
│           │            │
│  ┌────────┴─────────┐  │
│  │  Flask Server    │  │
│  │  (Python/Chaquopy)│ │ ← Runs locally
│  └──────────────────┘  │
│           │            │
│  ┌────────▼─────────┐  │
│  │ Google Sheets API│  │ ← Syncs data
│  └──────────────────┘  │
└────────────────────────┘
```

### Advantages:
- ✅ **No external server**: No need to pay for Render/Heroku
- ✅ **Works offline**: Only needs internet for Google Sheets
- ✅ **Same code**: Reuses 100% of your Flask app
- ✅ **Easy distribution**: Installable APK
- ✅ **Play Store ready**: Can be published

### Limitations:
- ⚠️ **Large APK**: ~50-70 MB (includes Python)
- ⚠️ **Slow first load**: ~20-30 seconds
- ⚠️ **Android 7.0+**: API 24 minimum

## 📂 Project Structure

```
F:\PodridaScoring\
│
├── 📱 ANDROID PROJECT (NEW)
│   └── android/
│       ├── app/
│       │   ├── build.gradle
│       │   └── src/main/
│       │       ├── AndroidManifest.xml
│       │       ├── java/.../MainActivity.kt
│       │       ├── res/ (layouts, resources)
│       │       └── assets/ (Flask code)
│       ├── build.gradle
│       └── settings.gradle
│
├── 🌐 ORIGINAL FLASK PROJECT (UNCHANGED)
│   ├── app/
│   ├── static/
│   ├── templates/
│   └── run.py
│
├── 📄 ANDROID-SPECIFIC FILES
│   ├── run_android.py
│   ├── android_config.py
│   └── requirements-android.txt
│
└── 🛠️ SCRIPTS
    └── copy-to-android.ps1
```

---

# Quick Start

## ✅ What you have right now

Everything is ready:
- ✅ Complete Android project in `F:\PodridaScoring\android\`
- ✅ Flask code copied to `assets`
- ✅ Chaquopy configuration ready
- ✅ MainActivity implemented

## 📥 Step 1: Install Android Studio

1. Download: https://developer.android.com/studio
2. Run installer
3. Select:
   - ✅ Android SDK
   - ✅ Android SDK Platform  
   - ✅ Android Virtual Device
4. Finish

**Time**: ~15 minutes (depends on your internet)

## 📂 Step 2: Open Project

1. Open **Android Studio**
2. `File` → `Open`
3. Navigate to: **`F:\PodridaScoring\android`**
4. Click `OK`

## ⚙️ Step 3: Wait for Sync

Android Studio will do this automatically:
- Download Gradle
- Download Android dependencies
- Download Chaquopy and Python
- Index project

**Message you'll see**: "Gradle sync in progress..."

**Time**: 5-15 minutes (first time)

**When finished**: You'll see "Gradle sync finished" at the bottom right

## 🔨 Step 4: Build

1. `Build` → `Make Project`
   - Or press `Ctrl+F9`

**Time**: 10-15 minutes (first time)

**When finished**: "Build: SUCCESS" in the Build tab

## 📱 Step 5: Create Emulator (if you don't have a device)

1. `Tools` → `Device Manager`
2. Click `Create Device`
3. Select: **Pixel 4**
4. Select image: **Android 11 (API 30)** or higher
5. Click `Next` → `Finish`
6. Click ▶️ to start the emulator

**Alternative**: Connect your phone via USB with USB debugging enabled

## ▶️ Step 6: Run App

1. Select device in the dropdown (top, next to ▶️)
2. Click ▶️ **Run**
3. Wait for installation (~1 minute)
4. **The app will open!**

### First execution:
- Loading screen: "Starting Flask server..."
- Python loads (~10 seconds)
- Flask starts (~5 seconds)  
- WebView loads the interface (~5 seconds)
- **Total: ~20-30 seconds**

### Subsequent executions:
- Only ~5-10 seconds

## ✅ Verify it Works

1. You should see the **login** screen
2. Username: `admin`
3. Password: `admin`
4. Navigate and use the app normally!

---

# Build Guide

## Detailed Compilation Steps

### Step 1: Copy Flask Files

Run the copy script from PowerShell:

```powershell
cd F:\PodridaScoring
.\copy-to-android.ps1
```

This will copy all your Flask code to the `assets` folder of the Android project.

Remove-Item -Path "F:\PodridaScoring\android\app\build" -Recurse -Force

### Step 3: Gradle Sync

1. Android Studio will show: **"Gradle files have changed"**
2. Click **"Sync Now"**
3. Wait 5-10 minutes (first time downloads many dependencies)
4. In the **"Build"** tab you'll see the progress

#### Common Sync Issues:

**Error: "Failed to download Chaquopy"**
```
Solution: Check internet connection and retry
```

**Error: "Python version not supported"**
```
Solution: In app/build.gradle, verify it says:
python {
    version "3.8"
}
```

**Error: "Minimum SDK version"**
```
Solution: In app/build.gradle, verify:
minSdk 24
```

### Step 4: Build Project

1. `Build` → `Make Project` (or `Ctrl+F9`)
2. Wait for compilation (first time: 10-15 minutes)
3. Verify there are no errors in the **"Build"** tab

#### Common Build Errors:

**Error: "Cannot resolve symbol 'R'"**
```
Solution: 
- Build → Clean Project
- Build → Rebuild Project
```

**Error: "Kotlin not found"**
```
Solution: Verify in build.gradle (project):
classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.20'
```

**Error: "Failed to find target with hash string 'android-34'"**
```
Solution:
1. Tools → SDK Manager
2. SDK Platforms → Check "Android 14.0 (API 34)"
3. Click Apply
4. Sync Project
```

### Step 5: Configure Emulator or Device

#### Option A: Use Emulator

1. `Tools` → `Device Manager`
2. Click `Create Device`
3. Select:
   - **Phone**: Pixel 4 or higher
   - **System Image**: Android 11 (R) or higher with API 30+
   - **RAM**: 2048 MB or more
4. Click `Finish`
5. Click ▶️ to start the emulator

#### Option B: Use Physical Device

1. **On your Android device**:
   - `Settings` → `About phone`
   - Tap 7 times on "Build number"
   - Go back to Settings → `System` → `Developer options`
   - Enable **"USB debugging"**

2. **Connect via USB**:
   - Connect device to PC
   - Authorize debugging on the device
   - Verify it appears in Android Studio (top, next to Run button)

### Step 6: Run the App

1. Select device/emulator in the dropdown (top)
2. Click ▶️ **Run** (or `Shift+F10`)
3. Wait for installation and execution

#### First Execution:

The app will:
1. Show loading screen
2. Start Python (takes ~10 seconds)
3. Import Flask modules (~5 seconds)
4. Start Flask server (~3 seconds)
5. Load WebView with interface

**Total time first execution**: ~20-30 seconds

#### Verify it Works:

1. You should see the login screen
2. Test login with: `admin` / `admin`
3. Navigate through the interface

### Step 7: View Logs (Debugging)

1. `View` → `Tool Windows` → `Logcat`
2. Filter by: `com.alesoftware.podridascoring`
3. Look for logs starting with:
   - `PodridaScoring:` (Kotlin logs)
   - `python.stdout:` (Python/Flask logs)

#### Important Logs:

```
=== CONFIGURING ANDROID ENVIRONMENT ===
=== STARTING FLASK FROM ANDROID ===
Host: 127.0.0.1
Port: 5000
```

If you see these logs, Flask is running correctly.

### Step 8: Modify Code (Development)

To make changes:

1. **Modify Flask code** in `F:\PodridaScoring`
2. **Run copy script**:
   ```powershell
   .\copy-to-android.ps1
   ```
3. **In Android Studio**: `Build` → `Clean Project`
4. **Rebuild**: `Build` → `Rebuild Project`
5. **Run** again

### Step 9: Generate APK for Distribution

#### Debug APK (Testing):

1. `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
2. Wait for compilation
3. Click `locate` in the notification
4. APK at: `android/app/build/outputs/apk/debug/app-debug.apk`

#### Release APK (Production):

1. **Create Keystore** (first time):
   ```powershell
   cd F:\PodridaScoring\android
   keytool -genkey -v -keystore podridascoring.keystore -alias podridascoring -keyalg RSA -keysize 2048 -validity 10000
   ```
   - Enter password (save it well)
   - Complete data (name, organization, etc.)

2. **Configure Signing** in `app/build.gradle`:
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file("../podridascoring.keystore")
               storePassword "YOUR_PASSWORD"
               keyAlias "podridascoring"
               keyPassword "YOUR_PASSWORD"
           }
       }
       
       buildTypes {
           release {
               signingConfig signingConfigs.release
               minifyEnabled true
               shrinkResources true
           }
       }
   }
   ```

3. **Generate Release APK**:
   - `Build` → `Generate Signed Bundle / APK`
   - Select `APK`
   - Choose keystore and passwords
   - Select `release`
   - `Finish`

4. **APK generated at**: `android/app/release/app-release.apk`

---

# Technical Documentation

## Complete Android Conversion

This section provides complete step-by-step instructions for converting the PodridaScoring Flask project into a hybrid Android app.

## Concept: Hybrid Architecture

The Android app will run your Flask server **locally inside the device** using:
- **Chaquopy**: Plugin that allows running Python on Android
- **WebView**: Android component that displays your web interface
- **Local Flask**: Runs on internal `localhost`
- **Google Sheets API**: Works the same, direct access from device

**Execution flow**:
1. User opens Android app
2. App starts Flask server on internal port (e.g., 5000)
3. WebView loads `http://localhost:5000`
4. User interacts with your normal Flask interface
5. When closing app, Flask server stops

## Prerequisites

### On your development PC

1. **Android Studio**: Download from https://developer.android.com/studio
2. **Java JDK 17**: Chaquopy requires JDK 17
3. **Python 3.8-3.11**: Compatible with Chaquopy (your project already uses 3.8+)
4. **Your current Flask project**: Complete copy in a new folder

### Basic Knowledge

- You don't need advanced Kotlin/Java knowledge
- You'll continue using Python/Flask for logic
- You'll only configure basic Android structure

## Files Created

### 1. Android Configuration Files:
- ✅ `android/build.gradle` - Project configuration
- ✅ `android/settings.gradle` - Project modules
- ✅ `android/app/build.gradle` - Dependencies and Chaquopy
- ✅ `android/app/src/main/AndroidManifest.xml` - Permissions and configuration

### 2. Android Code:
- ✅ `MainActivity.kt` - Main logic with WebView and Flask server
- ✅ `activity_main.xml` - Layout with loading screen and WebView
- ✅ `strings.xml` - App texts
- ✅ `colors.xml` - Color palette
- ✅ `themes.xml` - Application theme

### 3. Python Files for Android:
- ✅ `run_android.py` - Flask entry point for Android
- ✅ `android_config.py` - Automatic environment configuration
- ✅ `requirements-android.txt` - Python dependencies
- ✅ Modified `app/__init__.py` - Automatic Android detection

### 4. Helper Scripts:
- ✅ `copy-to-android.ps1` - Automatic copy script

### 5. Files Copied to Assets:
- ✅ Complete `app/` folder with all your Flask logic
- ✅ `static/` folder with CSS and JavaScript
- ✅ `templates/` folder with all HTML views
- ✅ `credentials.json` - Google Service Account credentials
- ✅ `run_android.py` and `android_config.py`

## Important File Structures

### android/app/build.gradle

Contains Python dependencies and Chaquopy configuration:

```gradle
python {
    version "3.8"
    
    pip {
        install "Flask==2.3.3"
        install "Werkzeug==2.3.7"
        install "gspread==5.10.0"
        install "google-auth==2.23.0"
        install "google-auth-oauthlib==1.0.0"
        install "google-auth-httplib2==0.1.1"
        install "bcrypt==4.0.1"
        install "python-dotenv==1.0.0"
        install "Jinja2==3.1.2"
        install "MarkupSafe==2.1.3"
        install "click==8.1.7"
        install "itsdangerous==2.1.2"
    }
}
```

### MainActivity.kt

Main activity that:
1. Initializes Python/Chaquopy
2. Starts Flask server in background thread
3. Loads Flask interface in WebView
4. Manages app lifecycle

Key methods:
- `onCreate()`: Initializes views and starts Flask
- `setupWebView()`: Configures WebView settings
- `startFlaskServer()`: Starts Flask in coroutine
- `loadFlaskApp()`: Loads URL in WebView

### run_android.py

Flask entry point for Android:

```python
from app import create_app

app = create_app()

def start_server():
    """Starts Flask server in Android mode."""
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False
    )
```

### android_config.py

Automatic environment configuration:

```python
def setup_android_env():
    """Configures environment variables for Android."""
    for key, value in ANDROID_CONFIG.items():
        if key not in os.environ:
            os.environ[key] = value

def is_android():
    """Detects if app is running on Android."""
    try:
        import android
        return True
    except ImportError:
        return False
```

## Development Workflow

### Making changes to code:

```powershell
# 1. Edit Flask code
code F:\PodridaScoring\app\routes\game.py

# 2. Copy to Android
.\copy-to-android.ps1

# 3. Recompile in Android Studio
Build → Clean Project
Build → Rebuild Project

# 4. Run
Run ▶️
```

### Testing cycle:

1. Modify Python/Flask code
2. Run `copy-to-android.ps1`
3. Clean + Rebuild in Android Studio
4. Deploy to device/emulator
5. Check Logcat for errors
6. Iterate

## Deployment Options

### Development APK

For testing on multiple devices:

```
Build → Build Bundle(s) / APK(s) → Build APK(s)
```

Share `app-debug.apk` via email, WhatsApp, etc.

### Production APK

For distribution or Play Store:

1. Create signing keystore
2. Configure signing in build.gradle
3. Generate signed APK
4. Test on clean device
5. Upload to Play Store or distribute

## Security Considerations

### 1. Credentials

Don't hardcode in production:
- Use first-run setup screen
- Save in encrypted SharedPreferences
- Or download from secure cloud storage

### 2. Service Account JSON

Secure options:
1. First run: User uploads file
2. Cloud storage: Download from Firebase/S3 with auth
3. Encryption: Encrypt file in assets

### 3. Communication

- ✅ Use HTTPS for Google Sheets API (already does)
- ✅ Localhost (127.0.0.1) for internal Flask
- ❌ DON'T expose Flask on external network (0.0.0.0)

---

# Conversion Summary

## ✅ What Was Created

### Android Configuration Files:
- `android/build.gradle` - Project configuration
- `android/settings.gradle` - Modules
- `android/app/build.gradle` - Dependencies and Chaquopy
- `AndroidManifest.xml` - Permissions and settings

### Android Implementation:
- `MainActivity.kt` - Main logic with WebView and Flask
- `activity_main.xml` - Layout with loading screen
- Resource files (strings, colors, themes)

### Python for Android:
- `run_android.py` - Flask entry point for Android
- `android_config.py` - Auto environment config
- `requirements-android.txt` - Python dependencies
- Modified `app/__init__.py` - Android detection

### Helper Scripts:
- `copy-to-android.ps1` - Automated copy script

### Assets (Flask Code):
- Complete `app/` folder
- `static/` and `templates/` folders
- `credentials.json`
- Python scripts

## 🚀 Next Steps

1. Install Android Studio
2. Open project at `F:\PodridaScoring\android`
3. Wait for Gradle sync (5-10 min)
4. Build project (10-15 min first time)
5. Run on emulator or device

## ⏱️ Estimated Times

- **First Gradle sync**: 5-10 minutes
- **First build**: 10-15 minutes
- **First device execution**: 20-30 seconds
- **Subsequent executions**: 5-10 seconds

## 📱 How the App Works

1. User opens app
2. Loading screen: "Starting Flask server..."
3. Python initializes on device (~10s)
4. Flask starts on localhost:5000 (~3s)
5. WebView loads Flask interface
6. User interacts normally with your app

## ✨ Android App Features

### Advantages:
- ✅ No external web server (all local)
- ✅ Works offline (except for Google Sheets sync)
- ✅ Same Flask code as web version
- ✅ Identical interface to web version
- ✅ Installable from APK
- ✅ Can be distributed on Play Store

### Limitations:
- ⚠️ Large APK (~50-70 MB due to Python)
- ⚠️ Slow first load (~20-30 seconds)
- ⚠️ Requires Android 7.0 (API 24) or higher

## 🎯 Objectives Completed

- [x] Flask project adapted for Android
- [x] Complete Android project structure
- [x] MainActivity with WebView and Flask server
- [x] Android layouts and resources
- [x] Automated copy script
- [x] Complete documentation
- [x] Files copied to assets
- [x] Project ready to compile

---

# Troubleshooting

## Common Problems and Solutions

### Gradle Sync Issues

#### "Gradle sync failed"
**Solution**: 
```
File → Invalidate Caches → Invalidate and Restart
```

#### "Failed to download Chaquopy"
**Solution**: 
- Check internet connection
- Retry sync
- Check firewall settings

#### "Python version not supported" or "No module named 'cgi'"
**Solution**: 
This error occurs if your host system has Python 3.13+, which removed the `cgi` module that Chaquopy needs.

**Fix: Install Python 3.11 and configure it**
1. Download Python 3.11.9 from: https://www.python.org/downloads/release/python-3119/
2. Install it (default location is fine)

3. **Add to `android/gradle.properties` (use forward slashes):**
   ```properties
   chaquopy.defaultPython=C:/Users/YOUR_USERNAME/AppData/Local/Programs/Python/Python311/python.exe
   ```
   Or if installed system-wide:
   ```properties
   chaquopy.defaultPython=C:/Python311/python.exe
   ```

4. **Clean build directories:**
   ```powershell
   Remove-Item -Path "android\.gradle" -Recurse -Force
   Remove-Item -Path "android\app\build" -Recurse -Force
   ```

5. **Close Android Studio completely**

6. **Before reopening, add Python 3.11 to PATH (PowerShell):**
   ```powershell
   $env:PATH = "C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python311;$env:PATH"
   ```
   Then launch Android Studio from the same PowerShell window:
   ```powershell
   & "C:\Program Files\Android\Android Studio\bin\studio64.exe"
   ```

7. **Sync and rebuild project**

Also verify your app's Python version in `app/build.gradle`:
```gradle
python {
    version "3.8"
}
```

### Build Errors

#### "Cannot resolve symbol 'R'"
**Solution**: 
```
Build → Clean Project
Build → Rebuild Project
```

#### "Kotlin not found" or "Kotlin version incompatible"
**Solution**: 
Verify in `build.gradle` (project level):
```gradle
id 'org.jetbrains.kotlin.android' version '2.0.21' apply false
```

If you get coroutines compatibility errors, the Kotlin version must be 2.0+ to work with kotlinx-coroutines 1.10+

#### "Failed to find target with hash string 'android-34'"
**Solution**:
1. Tools → SDK Manager
2. SDK Platforms → Check "Android 14.0 (API 34)"
3. Click Apply
4. Sync Project

### Runtime Issues

#### App closes on startup
**Solution**:
1. Check Logcat for exact error
2. Common: `ModuleNotFoundError`
   - **Cause**: Files not copied to assets
   - **Solution**: Run `copy-to-android.ps1` again

#### WebView shows blank page
**Solution**:
1. Check logs: Is Flask running?
2. Increase delay in MainActivity:
   ```kotlin
   // In startFlaskServer(), change:
   delay(3000)  // to
   delay(5000)  // or more
   ```

#### "Error starting server"
**Solution**:
1. Verify `credentials.json` exists in assets
2. Verify all Python dependencies installed
3. Rebuild project

#### App is very slow
**Solution**:
- Normal on first execution (loads complete Python)
- Subsequent executions are faster
- Consider using:
  ```gradle
  python {
      version "3.11"  // Newer Python = faster
  }
  ```

#### Can't connect to Google Sheets
**Solution**:
1. Verify `credentials.json` in assets
2. Verify Internet permission in AndroidManifest
3. Verify service account has access to Sheet
4. Check Logcat for gspread errors

## Useful Commands

### Copy Flask files to Android
```powershell
.\copy-to-android.ps1
```

### View assets content
```powershell
Get-ChildItem android\app\src\main\assets -Recurse
```

### Check Logcat (when app runs)
```
Android Studio: View → Tool Windows → Logcat
Filter: com.alesoftware.podridascoring
```

## Verification Checklist

Before running, verify:

- [ ] Android Studio installed with JDK 17
- [ ] Project opened at `F:\PodridaScoring\android`
- [ ] Gradle synced successfully
- [ ] Script `copy-to-android.ps1` executed
- [ ] Files in `android/app/src/main/assets/`:
  - [ ] Folder `app/`
  - [ ] Folder `static/`
  - [ ] Folder `templates/`
  - [ ] File `run_android.py`
  - [ ] File `android_config.py`
  - [ ] File `credentials.json`
- [ ] Successful build without errors
- [ ] Emulator or device connected

## Important File Structure

```
android/
├── app/
│   ├── build.gradle                    # Dependencies and config
│   ├── src/main/
│   │   ├── AndroidManifest.xml         # Permissions and app config
│   │   ├── java/.../MainActivity.kt    # Main code
│   │   ├── res/
│   │   │   ├── layout/activity_main.xml # UI
│   │   │   ├── values/strings.xml       # Texts
│   │   │   ├── values/colors.xml        # Colors
│   │   │   └── values/themes.xml        # Theme
│   │   └── assets/                     # ← Flask code here
│   │       ├── app/
│   │       ├── static/
│   │       ├── templates/
│   │       ├── run_android.py
│   │       ├── android_config.py
│   │       └── credentials.json
├── build.gradle                        # Project config
└── settings.gradle                     # Modules
```

## Support Resources

### For problems with:
- **Android compilation**: Check this troubleshooting section
- **Chaquopy/Python**: https://chaquo.com/chaquopy/doc/current/faq.html
- **Flask**: Your code remains the same
- **Google Sheets**: Same as web version

### Useful Links:
- **Android Studio**: https://developer.android.com/studio
- **Chaquopy Docs**: https://chaquo.com/chaquopy/doc/current/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Stack Overflow**: Tags `chaquopy` or `android-webview`

---

## 📊 Project Status

- [x] ✅ Android project created
- [x] ✅ Kotlin code implemented
- [x] ✅ Chaquopy configuration ready
- [x] ✅ Files copied to assets
- [x] ✅ Complete documentation
- [ ] ⏳ **Compile in Android Studio** ← YOU ARE HERE
- [ ] ⏳ Run on device
- [ ] ⏳ Complete testing
- [ ] ⏳ Generate release APK

---

**Last Updated**: 2025-11-28  
**Project**: PodridaScoring Android v1.0.0  
**Base Flask Version**: 2.0.0
