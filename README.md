# 📁 AI Media Sorter v1.0.0

<p align="center">
  <img src="assets/app_icon.png" width="128" height="128" alt="AI Media Sorter Logo" />
</p>

<p align="center">
  <strong>Smart, Private & 100% Offline Photo and Video Classifier</strong><br>
  <em>โปรแกรมคัดแยกรูปภาพและวิดีโออัจฉริยะแบบออฟไลน์ 100% รักษาความเป็นส่วนตัวสูงสุด</em>
</p>

<p align="center">
  <a href="#english"><img src="https://img.shields.io/badge/Language-English-blue.svg" alt="English"></a>
  <a href="#ภาษาไทย-thai"><img src="https://img.shields.io/badge/ภาษา-ไทย%20(Thai)-red.svg" alt="Thai"></a>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg" alt="100% Offline">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

## 🌐 Quick Language Links
- [English Documentation](#english)
- [คู่มือการใช้งานภาษาไทย](#ภาษาไทย-thai)

---

<a name="english"></a>
# 🇬🇧 English Documentation

## 🌟 Overview
**AI Media Sorter** is a high-performance, ultra-modern desktop application designed to automatically scan, classify, and organize your vast collections of photos and videos into designated folders without sending a single byte of data over the internet.

Powered by lightweight on-device AI models (**YuNet**, **YOLOv8 Nano**, and **Document Vision Engine**), it intelligently detects faces, people, documents, bank transfer slips, QR codes, dogs, cats, pets, and vehicles at high speeds with minimal CPU consumption.

---

## ✨ Key Features

- 🔒 **100% Offline & Private**: Zero cloud dependency. No data collection, telemetry, or internet connection required.
- 🎯 **Multi-Category AI Detection**:
  - 👤 **People & Faces**: YuNet Face Detection + YOLOv8 Person Recognition.
  - 📄 **Documents & Slips**: Bank transfer slips, invoices, receipts, and QR codes via OpenCV morphology & QR decoding.
  - 🐶 🐱 🐾 **Pets (Dogs & Cats)**: YOLOv8 animal detection.
  - 🚗 **Vehicles**: Cars, motorcycles, buses, trucks.
- 🎬 **Photos & Videos Supported**:
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.heic` (Apple iPhone Live Photos / HEIF).
  - **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` (smart multi-keyframe sampling).
- 📂 **Recursive Subfolder Scanning**: Toggle to deeply search nested folder hierarchies (ideal for iPhone `DCIM/100APPLE` backups).
- ⚙️ **Copy vs. Move Operation**: Choose whether to keep original files or relocate them with safety confirmation dialogues.
- 🎨 **Modern Fluent UI**: Dark Mode, Light Mode, and System Theme switcher with real-time ETA, file counters, and progress logs.
- 🌍 **Bilingual Support**: Instant toggle between **English** and **ภาษาไทย (Thai)**.

---

## 🚀 Installation & Getting Started

You can run **AI Media Sorter** using either the pre-built portable executable (Windows) or directly from source code (Windows / macOS / Linux).

---

### Option 1: Standalone Portable EXE (Windows — No Python Required)

1. Download the latest release `.zip` from the [Releases](https://github.com/lnwgolf/AI-Media-Sorter/releases/latest) section.
2. Extract the folder `AI_Image_Sorter`.
3. Double-click `AI_Image_Sorter.exe` to launch immediately!

---

### Option 2: Running from Source (Windows / macOS / Linux)

#### 1. Prerequisites
- **Python 3.10, 3.11, or 3.12** installed on your system.
  - Windows: Download from [python.org](https://www.python.org/downloads/) (Make sure to check **"Add Python to PATH"**).
  - macOS: `brew install python`
  - Linux (Ubuntu/Debian): `sudo apt update && sudo apt install python3 python3-pip python3-venv python3-tk`

#### 2. Clone the Repository
```bash
git clone https://github.com/lnwgolf/AI-Media-Sorter.git
cd AI-Media-Sorter
```

#### 3. Set Up Virtual Environment

- **On Windows (PowerShell / Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
  *(Or simply double-click `run_windows.bat`)*

- **On macOS / Linux (Terminal):**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
  *(Or execute `chmod +x run_mac_linux.sh && ./run_mac_linux.sh`)*

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Launch the Application
```bash
python AI_Image_Sorter.py
```

---

## 📦 Building Standalone Executable with PyInstaller

If you wish to compile the application into a standalone `.exe` on Windows:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --icon="app_icon.ico" --add-data "face_detection_yunet.onnx;." --add-data "yolov8n.pt;." --add-data "app_icon.ico;." --add-data "app_icon.png;." --add-data "app_icon_*.png;." AI_Image_Sorter.py
```
The compiled application will be placed in `dist/AI_Image_Sorter/`.

---

## 🏷️ Model & Library Credits

We gratefully acknowledge the open-source projects and AI models that make this application possible:

1. **YuNet (Face Detection)**
   - Developed by: Shiqi Yu team & OpenCV Model Zoo
   - Model: `face_detection_yunet.onnx`
   - Repository: [opencv/opencv_zoo](https://github.com/opencv/opencv_zoo)
   - License: Apache License 2.0 / MIT

2. **YOLOv8 Nano (Object & Animal Detection)**
   - Developed by: [Ultralytics](https://github.com/ultralytics/ultralytics)
   - Model: `yolov8n.pt`
   - License: AGPL-3.0 / Enterprise License

3. **CustomTkinter (Modern Desktop UI)**
   - Developed by: [Tom Schimansky](https://github.com/TomSchimansky/CustomTkinter)
   - License: MIT License

4. **Pillow-HEIF (Apple iPhone HEIC Support)**
   - Developed by: [bigcat88/pillow_heif](https://github.com/bigcat88/pillow_heif)
   - License: LGPL / Apache-2.0

5. **OpenCV & NumPy & Pillow**
   - Essential computer vision and image processing backbone.

---

## ☕ Support the Developer
If you find this software helpful, feel free to buy the developer a coffee:
- **PromptPay / Buy me a coffee**: [https://ezdn.app/golfeasy](https://ezdn.app/golfeasy)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---
---

<a name="ภาษาไทย-thai"></a>
# 🇹🇭 คู่มือการใช้งานภาษาไทย (Thai Documentation)

## 🌟 ภาพรวมโปรแกรม
**AI Media Sorter** คือโปรแกรม Desktop สำหรับคัดแยกและจัดระเบียบไฟล์รูปภาพและวิดีโอจำนวนมากเข้าโฟลเดอร์เป้าหมายอัตโนมัติ โดยทำงานแบบ **ออฟไลน์ 100% (Offline)** ภายในเครื่องของคุณ ไม่มีการส่งรูปภาพหรือข้อมูลใดๆ ออกนอกเครื่อง มั่นใจได้ในความปลอดภัยและความเป็นส่วนตัวสูงสุด

โปรแกรมขับเคลื่อนด้วยโมเดล AI ขนาดกะทัดรัดแต่แม่นยำสูง (**YuNet**, **YOLOv8 Nano** และ **Document Vision Engine**) สามารถตรวจจับใบหน้าคน, เอกสาร/สลิปโอนเงิน, สัตว์เลี้ยง (หมา/แมว) และยานพาหนะได้อย่างรวดเร็ว โดยไม่กินทรัพยากรเครื่อง

---

## ✨ ฟีเจอร์เด่น

- 🔒 **ออฟไลน์ 100% & ปลอดภัยสูงสุด**: ไม่ต้องต่ออินเทอร์เน็ต รูปภาพส่วนตัวของคุณจะไม่ถูกอัปโหลดขึ้นเซิร์ฟเวอร์ใดๆ ทั้งสิ้น
- 🎯 **ระบบตรวจจับอัจฉริยะ (AI Detection)**:
  - 👤 **รูปคนและใบหน้า**: ผสานพลัง YuNet + YOLOv8 ตรวจจับคนและใบหน้าได้อย่างแม่นยำ
  - 📄 **เอกสาร / สลิปโอนเงิน / QR Code**: ตรวจจับสลิปธนาคาร ใบเสร็จ เอกสาร และคิวอาร์โค้ด
  - 🐶 🐱 🐾 **สัตว์เลี้ยง (สุนัข / แมว)**: คัดแยกภาพน้องหมาและน้องแมวโดยเฉพาะ
  - 🚗 **ยานพาหนะ**: รถยนต์ รถมอเตอร์ไซค์ รถบรรทุก รถบัส
- 🎬 **รองรับทั้งรูปภาพและวิดีโอ**:
  - **รูปภาพ**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp` และภาพถ่ายไอโฟน `.heic`
  - **วิดีโอ**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` (สุ่มตรวจเฟรมหลักอัตโนมัติ)
- 📂 **สแกนทะลุโฟลเดอร์ย่อย (Recursive Subfolders)**: มีสวิตช์เลือกกวาดไฟล์จากโฟลเดอร์ย่อยทั้งหมด (เหมาะมากสำหรับรูปถ่าย Backup จาก iPhone หรือกล้องดิจิตอล)
- ⚙️ **โหมด Copy (คัดลอก) หรือ Move (ย้ายไฟล์)**: มีระบบแจ้งเตือนยืนยันความปลอดภัยก่อนย้ายไฟล์
- 🎨 **หน้าตาสวยงาม ทันสมัย**: รองรับทั้งโหมดมืด (Dark Mode) และโหมดสว่าง (Light Mode) พร้อมบอกเวลาที่ใช้และเวลาที่คาดว่าจะเสร็จแบบ Real-time
- 🌍 **รองรับ 2 ภาษา**: สลับเปลี่ยนภาษาไทย และภาษาอังกฤษได้ทันทีในหน้าโปรแกรม

---

## 🚀 ขั้นตอนการติดตั้งและการเปิดใช้งาน

คุณสามารถเลือกใช้งานได้ 2 รูปแบบตามความสะดวก:

---

### วิธีที่ 1: สำหรับผู้ใช้ทั่วไปบน Windows (ไฟล์ .EXE — ไม่ต้องลง Python)

1. ดาวน์โหลดไฟล์ `.zip` เวอร์ชันล่าสุดจากหน้า [Releases](https://github.com/lnwgolf/AI-Media-Sorter/releases/latest)
2. แตกไฟล์โฟลเดอร์ `AI_Image_Sorter`
3. ดับเบิ้ลคลิกเปิดไฟล์ **`AI_Image_Sorter.exe`** ใช้งานได้ทันที!

---

### วิธีที่ 2: สำหรับรันผ่าน Source Code (Windows / macOS / Linux)

#### 1. สิ่งที่ต้องเตรียมก่อนเริ่มต้น
- ติดตั้ง **Python 3.10 ขึ้นไป** (แนะนำ 3.10 หรือ 3.11)
  - Windows: ดาวน์โหลดจาก [python.org](https://www.python.org/downloads/) (*อย่าลืมติ๊กถูกที่ช่อง **"Add Python to PATH"** ตอนติดตั้ง*)
  - macOS: ติดตั้งผ่าน Homebrew ด้วยคำสั่ง `brew install python python-tk`
  - Linux (Ubuntu/Debian): รันคำสั่ง `sudo apt update && sudo apt install python3 python3-pip python3-venv python3-tk`

#### 2. ดาวน์โหลดโค้ดโปรเจกต์
```bash
git clone https://github.com/lnwgolf/AI-Media-Sorter.git
cd AI-Media-Sorter
```

#### 3. สร้างและเปิดใช้งาน Virtual Environment

- **บน Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
  *(หรือดับเบิ้ลคลิกไฟล์ `run_windows.bat` เพื่อรันแบบอัตโนมัติ)*

- **บน macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
  *(หรือรันผ่านสคริปต์ `./run_mac_linux.sh`)*

#### 4. ติดตั้ง Library และ Dependency ที่จำเป็น
```bash
pip install -r requirements.txt
```

#### 5. สั่งเริ่มทำงานโปรแกรม
```bash
python AI_Image_Sorter.py
```

---

## 🏷️ การอ้างอิงและให้เครดิตโมเดล AI (Model Credits)

ขอขอบคุณเจ้าของผลงาน Open Source และผู้พัฒนาโมเดล AI คุณภาพสูงที่นำมาใช้ในโปรเจกต์นี้:

1. **YuNet (โมเดลตรวจจับใบหน้าคน)**
   - ผู้พัฒนา: Shiqi Yu และทีมงาน OpenCV Model Zoo
   - ไฟล์โมเดล: `face_detection_yunet.onnx`
   - แหล่งที่มา: [opencv/opencv_zoo](https://github.com/opencv/opencv_zoo)
   - สัญญาอนุญาต: Apache License 2.0 / MIT

2. **YOLOv8 Nano (โมเดลตรวจจับคน สัตว์เลี้ยง และวัตถุ)**
   - ผู้พัฒนา: [Ultralytics](https://github.com/ultralytics/ultralytics)
   - ไฟล์โมเดล: `yolov8n.pt`
   - สัญญาอนุญาต: AGPL-3.0

3. **CustomTkinter (ระบบ UI Desktop สุดโมเดิร์น)**
   - ผู้พัฒนา: [Tom Schimansky](https://github.com/TomSchimansky/CustomTkinter)
   - สัญญาอนุญาต: MIT License

4. **Pillow-HEIF (ตัวถอดรหัสรูปภาพไอโฟน .HEIC)**
   - ผู้พัฒนา: [bigcat88/pillow_heif](https://github.com/bigcat88/pillow_heif)

---

## ☕ สนับสนุนผู้พัฒนา
หากโปรแกรมนี้มีประโยชน์และช่วยประหยัดเวลาในการทำงานของคุณ สามารถร่วมเลี้ยงกาแฟผู้พัฒนาได้ที่:
- **เลี้ยงกาแฟผ่าน PromptPay / QR Code**: [https://ezdn.app/golfeasy](https://ezdn.app/golfeasy)

---

## 📄 ลิขสิทธิ์และการใช้งาน (License)
โปรเจกต์นี้เผยแพร่ภายใต้สัญญาอนุญาต [MIT License](LICENSE) สามารถนำไปใช้งาน พัฒนาต่อ หรือแชร์ต่อได้อย่างอิสระครับ
