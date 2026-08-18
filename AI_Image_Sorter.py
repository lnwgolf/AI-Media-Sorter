"""
AI Media Sorter (Premium Modern Desktop UI)
Supports:
  - Face Detection via YuNet
  - Object & Animal Detection via YOLOv8
  - Document / Slip / QR Detection
  - Multi-threaded processing with real-time UI updates
  - Ultra-modern GUI with Theme & Bilingual Switcher
  - JPG, PNG, WEBP, BMP, HEIC, MP4, MOV, AVI, MKV
"""

APP_VERSION = "v1.0.0"

import os
import sys
import time
import shutil
import threading
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

# -----------------------------------------------------------------------------
# Dependency Checks
# -----------------------------------------------------------------------------
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORT = True
except Exception:
    HEIC_SUPPORT = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception:
    YOLO_AVAILABLE = False

# -----------------------------------------------------------------------------
# Configuration & Theming
# -----------------------------------------------------------------------------
class ThemeConfig:
    """Centralized Theme and Styling Configuration"""
    
    # Colors: (Light Mode, Dark Mode)
    BG_ROOT        = ("#F1F5F9", "#0F172A")
    BG_CARD        = ("#FFFFFF", "#1E293B")
    BG_INPUT       = ("#F8FAFC", "#0F172A")
    BG_PILL_GROUP  = ("#F8FAFC", "#0F172A")
    
    BORDER         = ("#E2E8F0", "#334155")
    BORDER_INPUT   = ("#CBD5E1", "#475569")
    
    TEXT_MAIN      = ("#0F172A", "#F8FAFC")
    TEXT_SUB       = ("#64748B", "#94A3B8")
    TEXT_ACCENT    = ("#3B82F6", "#60A5FA")
    
    BTN_PRIMARY    = ("#2563EB", "#3B82F6")
    BTN_PRIMARY_HV = ("#1D4ED8", "#2563EB")
    
    BTN_DANGER     = ("#EF4444", "#DC2626")
    BTN_DANGER_HV  = ("#DC2626", "#B91C1C")
    
    BTN_DONATE     = ("#F59E0B", "#D97706")
    BTN_DONATE_HV  = ("#D97706", "#B45309")
    
    BTN_GHOST      = ("#F1F5F9", "#334155")
    BTN_GHOST_HV   = ("#E2E8F0", "#475569")
    
    BADGE_BG       = ("#EFF6FF", "#1E3A8A")
    BADGE_FG       = ("#2563EB", "#93C5FD")
    
    SUCCESS        = ("#10B981", "#34D399")
    ERROR          = ("#EF4444", "#F87171")

    @staticmethod
    def font_title(size=22, weight="bold"): return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)
    @staticmethod
    def font_body(size=12, weight="normal"): return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)
    @staticmethod
    def font_mono(size=11): return ctk.CTkFont(family="Consolas", size=size)


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------
def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    local_path = os.path.join(base_path, relative_path)
    if os.path.exists(local_path): return local_path
    
    assets_path = os.path.join(base_path, "assets", relative_path)
    if os.path.exists(assets_path): return assets_path
    
    cwd_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(cwd_path): return cwd_path
    
    cwd_assets = os.path.join(os.getcwd(), "assets", relative_path)
    if os.path.exists(cwd_assets): return cwd_assets
        
    internal_path = os.path.join(base_path, "_internal", relative_path)
    if os.path.exists(internal_path): return internal_path

    return local_path

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic', '.mp4', '.mov', '.avi', '.mkv', '.webm'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}

# -----------------------------------------------------------------------------
# Localization Data
# -----------------------------------------------------------------------------
LANGUAGES = {
    "English": {
        "app_title": f"AI Media Sorter {APP_VERSION} • Smart Offline Photo & Video Organizer",
        "header_title": f"AI Media Sorter {APP_VERSION}",
        "badge_offline": "100% OFFLINE & PRIVATE",
        "header_subtitle": "Intelligent photo and video classification powered by YuNet, YOLOv8 & Document AI",
        "section_folders": "📁 FOLDER PATHS",
        "src_label": "Source Folder",
        "src_placeholder": "Select folder containing photos to scan...",
        "dst_label": "Destination Folder",
        "dst_placeholder": "Select output folder to store classified images...",
        "browse_btn": "Browse...",
        "include_subfolders": "Include Subfolders",
        "section_targets": "🎯 DETECTION TARGET",
        "target_person": "👤 Person & Face",
        "target_doc": "📄 Document / Slip / QR",
        "target_dog": "🐶 Dog",
        "target_cat": "🐱 Cat",
        "target_pet": "🐾 Pets (All)",
        "target_vehicle": "🚗 Vehicles",
        "section_options": "⚙️ PROCESS SETTINGS",
        "media_type_label": "Media Type:",
        "media_img": "🖼️ Images Only",
        "media_vid": "🎬 Videos Only",
        "media_both": "📁 Both (Img & Vid)",
        "mode_label": "File Operation:",
        "mode_copy": "Copy (Keep Original)",
        "mode_move": "Move (Relocate)",
        "conf_label": "Confidence Level:",
        "status_ready": "● READY TO SCAN",
        "status_scanning": "● SCANNING ACTIVE...",
        "status_stopping": "● STOPPING WORKER...",
        "status_complete": "● COMPLETED SUCCESSFULLY",
        "status_stopped": "● PROCESS HALTED",
        "stat_box_total": "TOTAL FILES",
        "stat_box_matched": "SORTED",
        "stat_box_time": "ELAPSED",
        "stat_box_eta": "EST. REMAINING",
        "start_btn": "▶  START AI SORTING",
        "stop_btn": "⏹  STOP PROCESS",
        "donate_btn": "☕ Buy me a coffee",
        "confirm_move_title": "Confirm Move Operation",
        "confirm_move_body": "You selected MOVE mode.\n\nOriginal files will be relocated from the source folder.\nThis cannot be undone.\n\nDo you want to proceed?",
        "err_permission": "Permission denied: Cannot access this folder.\nPlease choose a different folder or run as Administrator.",
        "err_src_invalid": "Please select a valid source directory containing images.",
        "err_dst_create": "Cannot create destination directory:\n",
        "err_same_folder": "Source and destination folders cannot be identical.",
        "msg_done_title": "Sorting Completed",
        "msg_done_body": "AI Classification Finished!\n\n• Total Scanned: {total}\n• Sorted: {matched}\n• Elapsed: {elapsed:.1f}s",
        "log_init_check": "🔍 Initializing AI subsystem & verifying local model weights...",
        "log_yunet_found": "  ✓ Face AI Model (YuNet): Active [{name}]",
        "log_yunet_missing": "  ✗ Face AI Model (YuNet): Missing (face_detection_yunet.onnx)",
        "log_yolo_found": "  ✓ Object & Animal AI (YOLOv8): Active [{name}]",
        "log_yolo_missing": "  ✗ Object AI (YOLOv8): Missing (yolov8n.pt)",
        "log_doc_ready": "  ✓ Document & Bank Slip Vision Engine: Ready",
        "log_heic_ready": "  ✓ Apple iPhone (.HEIC) Decoder: Enabled",
        "log_heic_missing": "  ℹ Apple iPhone (.HEIC) Decoder: Disabled (install pillow_heif)",
        "log_ready_hint": "✨ Ready! Configure folders and click 'START AI SORTING' to begin.",
        "log_start_scan": "\n🚀 Starting AI Scan Workflow on: {src}",
        "log_target_info": "🎯 Target: {target} | Mode: {mode} | Confidence: {conf:.0%}",
        "log_no_images": "❌ No supported media files found in source.",
        "log_found_images": "📸 Found {total} media files to process.",
        "log_user_stopped": "🛑 Worker halted by user request.",
        "log_done_summary": "\n" + "="*50 + "\n🎉 COMPLETED in {elapsed:.1f}s\n📊 Scanned: {total} | Sorted: {matched} | Non-target: {unmatched}\n" + "="*50,
    },
    "ภาษาไทย (Thai)": {
        "app_title": f"AI Media Sorter {APP_VERSION} • โปรแกรมคัดแยกรูปภาพและวิดีโออัจฉริยะแบบออฟไลน์",
        "header_title": f"AI Media Sorter {APP_VERSION}",
        "badge_offline": "100% ออฟไลน์ & ความเป็นส่วนตัวสูงสุด",
        "header_subtitle": "คัดแยกและจัดระเบียบรูปภาพและวิดีโออัตโนมัติด้วย YuNet, YOLOv8 และ Document AI",
        "section_folders": "📁 โฟลเดอร์ต้นทางและปลายทาง",
        "src_label": "โฟลเดอร์รูปภาพต้นทาง (Source)",
        "src_placeholder": "เลือกโฟลเดอร์รูปภาพที่ต้องการสแกน...",
        "dst_label": "โฟลเดอร์สำหรับจัดเก็บ (Destination)",
        "dst_placeholder": "เลือกโฟลเดอร์ปลายทาง...",
        "browse_btn": "เลือกโฟลเดอร์...",
        "include_subfolders": "รวมโฟลเดอร์ย่อยทั้งหมด",
        "section_targets": "🎯 สิ่งที่ต้องการคัดแยก (AI Target)",
        "target_person": "👤 รูปคนและใบหน้า",
        "target_doc": "📄 เอกสาร / สลิป / QR",
        "target_dog": "🐶 สุนัข (Dog)",
        "target_cat": "🐱 แมว (Cat)",
        "target_pet": "🐾 สัตว์เลี้ยง (หมา/แมว)",
        "target_vehicle": "🚗 ยานพาหนะ",
        "section_options": "⚙️ การตั้งค่าการทำงาน",
        "media_type_label": "ประเภทไฟล์สื่อ:",
        "media_img": "🖼️ เฉพาะรูปภาพ",
        "media_vid": "🎬 เฉพาะวิดีโอ",
        "media_both": "📁 สแกนทั้งหมด",
        "mode_label": "โหมดจัดการไฟล์:",
        "mode_copy": "คัดลอกไฟล์ (Copy)",
        "mode_move": "ย้ายไฟล์ (Move)",
        "conf_label": "ความแม่นยำ (Confidence):",
        "status_ready": "● พร้อมทำงาน",
        "status_scanning": "● กำลังสแกนและประมวลผล...",
        "status_stopping": "● กำลังหยุดการทำงาน...",
        "status_complete": "● เสร็จสมบูรณ์เรียบร้อย",
        "status_stopped": "● หยุดการทำงานแล้ว",
        "stat_box_total": "ไฟล์ทั้งหมด",
        "stat_box_matched": "คัดแยกสำเร็จ",
        "stat_box_time": "เวลาที่ใช้",
        "stat_box_eta": "คาดว่าจะเสร็จ",
        "start_btn": "▶  เริ่มต้นการคัดแยกรูปภาพ",
        "stop_btn": "⏹  หยุดการทำงาน",
        "donate_btn": "☕ เลี้ยงกาแฟผู้พัฒนา",
        "confirm_move_title": "ยืนยันการย้ายไฟล์",
        "confirm_move_body": "คุณเลือกโหมด \"ย้ายไฟล์ (Move)\"\n\nไฟล์ต้นฉบับจะถูกย้ายออกจากโฟลเดอร์ต้นทาง\nการดำเนินการนี้ไม่สามารถย้อนกลับได้\n\nต้องการดำเนินการต่อหรือไม่?",
        "err_permission": "ไม่มีสิทธิ์เข้าถึงโฟลเดอร์นี้\nกรุณาเลือกโฟลเดอร์อื่น หรือรันโปรแกรมในฐานะ Administrator",
        "err_src_invalid": "กรุณาระบุโฟลเดอร์ต้นทางให้ถูกต้อง",
        "err_dst_create": "ไม่สามารถสร้างโฟลเดอร์ปลายทางได้:\n",
        "err_same_folder": "โฟลเดอร์ต้นทางและปลายทางต้องไม่ซ้ำกัน",
        "msg_done_title": "คัดแยกเสร็จสิ้น",
        "msg_done_body": "คัดแยกรูปภาพเรียบร้อยแล้ว!\n\n• จำนวนทั้งหมด: {total}\n• คัดแยกสำเร็จ: {matched}\n• ใช้เวลาทั้งสิ้น: {elapsed:.1f} วิ",
        "log_init_check": "🔍 กำลังตรวจสอบระบบ AI และไฟล์โมเดลในเครื่อง...",
        "log_yunet_found": "  ✓ โมเดลตรวจจับใบหน้า (YuNet): พร้อมใช้งาน [{name}]",
        "log_yunet_missing": "  ✗ ไม่พบโมเดล YuNet (face_detection_yunet.onnx)",
        "log_yolo_found": "  ✓ โมเดลตรวจจับสัตว์และวัตถุ (YOLOv8): พร้อมใช้งาน [{name}]",
        "log_yolo_missing": "  ✗ ไม่พบโมเดล YOLOv8 (yolov8n.pt)",
        "log_doc_ready": "  ✓ ระบบตรวจจับเอกสารและสลิปโอนเงิน (Document AI): พร้อมใช้งาน",
        "log_heic_ready": "  ✓ รองรับภาพถ่าย iPhone (.HEIC): เปิดใช้งาน",
        "log_heic_missing": "  ℹ ไม่พบตัวอ่านภาพ .HEIC (ต้องติดตั้ง pillow_heif)",
        "log_ready_hint": "✨ ระบบพร้อมทำงาน! เลือกโฟลเดอร์และกดปุ่ม 'เริ่มต้นการคัดแยก' ได้ทันที",
        "log_start_scan": "\n🚀 เริ่มต้นสแกนโฟลเดอร์: {src}",
        "log_target_info": "🎯 เป้าหมาย: {target} | โหมด: {mode} | ความแม่นยำ: {conf:.0%}",
        "log_no_images": "❌ ไม่พบไฟล์สื่อที่รองรับในโฟลเดอร์ต้นทาง",
        "log_found_images": "📸 พบไฟล์รูปภาพและวิดีโอทั้งหมด {total} ไฟล์",
        "log_user_stopped": "🛑 ผู้ใช้สั่งหยุดการทำงาน",
        "log_done_summary": "\n" + "="*50 + "\n🎉 เสร็จสมบูรณ์ในเวลา {elapsed:.1f} วินาที\n📊 สแกนทั้งหมด: {total} | คัดแยกสำเร็จ: {matched} | ไม่ตรงเงื่อนไข: {unmatched}\n" + "="*50,
    }
}

# -----------------------------------------------------------------------------
# Main Application Class
# -----------------------------------------------------------------------------
class ImageSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ensure Windows Taskbar uses custom App Icon
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ai_media_sorter.app.v1")
        except Exception:
            pass

        self.current_lang = "English"
        self.current_theme = "Light"
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.title(self.t("app_title"))
        self.geometry("1100x760")
        self.minsize(900, 600)

        # Set app icon with multi-size PhotoImages for pin-sharp display at any scale/DPI
        ico_path = get_resource_path("app_icon.ico")
        png_path = get_resource_path("app_icon.png")
        if os.path.exists(png_path):
            try:
                base_img = Image.open(png_path)
                self._app_icon_imgs = []
                for s in (16, 20, 24, 32, 40, 48, 64, 128, 256):
                    p_path = get_resource_path(f"app_icon_{s}.png")
                    if os.path.exists(p_path):
                        self._app_icon_imgs.append(ImageTk.PhotoImage(file=p_path))
                    else:
                        self._app_icon_imgs.append(ImageTk.PhotoImage(base_img.resize((s, s), Image.LANCZOS)))
                self.wm_iconphoto(True, *self._app_icon_imgs)
            except Exception:
                pass
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # Open Maximized (Full Screen) on startup
        try:
            self.after(50, lambda: self.state('zoomed'))
        except Exception:
            pass

        self.is_running = False
        self.stop_requested = False
        self.qr_detector = cv2.QRCodeDetector()

        self._build_ui()
        self._check_models()

    def t(self, key: str) -> str:
        return LANGUAGES.get(self.current_lang, LANGUAGES["English"]).get(key, key)

    # -------------------------------------------------------------------------
    # UI Construction
    # -------------------------------------------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, fg_color=ThemeConfig.BG_ROOT, corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(3, weight=1)
        self.main_container.grid_rowconfigure(4, weight=0)

        self._build_header(self.main_container, row=0)
        self._build_folders_card(self.main_container, row=1)
        self._build_targets_card(self.main_container, row=2)
        self._build_monitor_card(self.main_container, row=3)
        self._build_actions_card(self.main_container, row=4)

    def _create_card(self, parent, row):
        card = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=ThemeConfig.BG_CARD,
            border_width=1,
            border_color=ThemeConfig.BORDER
        )
        card.grid(row=row, column=0, padx=24, pady=5, sticky="ew")
        return card

    def _build_header(self, parent, row):
        card = self._create_card(parent, row)
        card.grid(pady=(12, 5))
        card.grid_columnconfigure(0, weight=1)

        # Left Info
        left_fr = ctk.CTkFrame(card, fg_color="transparent")
        left_fr.pack(side="left", padx=20, pady=16, fill="y")

        title_fr = ctk.CTkFrame(left_fr, fg_color="transparent")
        title_fr.pack(anchor="w")

        self.title_label = ctk.CTkLabel(title_fr, text=self.t("header_title"), 
                                        font=ThemeConfig.font_title(24), text_color=ThemeConfig.TEXT_MAIN)
        self.title_label.pack(side="left")

        self.badge_label = ctk.CTkLabel(title_fr, text=f"  {self.t('badge_offline')}  ",
                                        font=ThemeConfig.font_title(10), fg_color=ThemeConfig.BADGE_BG,
                                        text_color=ThemeConfig.BADGE_FG, corner_radius=8)
        self.badge_label.pack(side="left", padx=(12, 0))

        self.subtitle_label = ctk.CTkLabel(left_fr, text=self.t("header_subtitle"),
                                           font=ThemeConfig.font_body(13), text_color=ThemeConfig.TEXT_SUB)
        self.subtitle_label.pack(anchor="w", pady=(4, 0))

        # Right Controls
        right_fr = ctk.CTkFrame(card, fg_color="transparent")
        right_fr.pack(side="right", padx=20, pady=16)

        self.lang_menu = ctk.CTkOptionMenu(right_fr, values=["English", "ภาษาไทย (Thai)"], width=140, height=32,
                                           corner_radius=8, fg_color=ThemeConfig.BTN_GHOST, text_color=ThemeConfig.TEXT_MAIN,
                                           command=self.change_language)
        self.lang_menu.set(self.current_lang)
        self.lang_menu.grid(row=0, column=0, padx=(0, 10), pady=4)

        self.theme_menu = ctk.CTkOptionMenu(right_fr, values=["Light", "Dark", "System"], width=110, height=32,
                                            corner_radius=8, fg_color=ThemeConfig.BTN_GHOST, text_color=ThemeConfig.TEXT_MAIN,
                                            command=self.change_theme)
        self.theme_menu.set(self.current_theme)
        self.theme_menu.grid(row=0, column=1, padx=0, pady=4)

        self.donate_btn = ctk.CTkButton(right_fr, text=self.t("donate_btn"), font=ThemeConfig.font_title(12),
                                        height=30, corner_radius=8, fg_color=ThemeConfig.BTN_DONATE,
                                        hover_color=ThemeConfig.BTN_DONATE_HV, text_color="white",
                                        command=lambda: webbrowser.open("https://ezdn.app/golfeasy"))
        self.donate_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    def _build_folders_card(self, parent, row):
        card = self._create_card(parent, row)
        card.grid_columnconfigure(1, weight=1)

        self.sec_folders_label = ctk.CTkLabel(card, text=self.t("section_folders"), font=ThemeConfig.font_title(13), text_color=ThemeConfig.TEXT_ACCENT)
        self.sec_folders_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(16, 8), sticky="w")

        default_pics = os.path.join(os.path.expanduser("~"), "Pictures")
        if not os.path.exists(default_pics): default_pics = os.getcwd()

        # Source
        self.src_label = ctk.CTkLabel(card, text=self.t("src_label"), font=ThemeConfig.font_title(13))
        self.src_label.grid(row=1, column=0, padx=20, pady=6, sticky="w")
        self.src_entry = ctk.CTkEntry(card, placeholder_text=self.t("src_placeholder"), height=36, corner_radius=8,
                                      fg_color=ThemeConfig.BG_INPUT, border_color=ThemeConfig.BORDER_INPUT)
        self.src_entry.grid(row=1, column=1, padx=8, pady=6, sticky="ew")
        self.src_entry.insert(0, default_pics)
        self.src_browse_btn = ctk.CTkButton(card, text=self.t("browse_btn"), width=110, height=36, corner_radius=8,
                                            fg_color=ThemeConfig.BTN_GHOST, hover_color=ThemeConfig.BTN_GHOST_HV, text_color=ThemeConfig.TEXT_MAIN,
                                            command=lambda: self._browse_dir(self.src_entry))
        self.src_browse_btn.grid(row=1, column=2, padx=20, pady=6)

        # Source Subfolders Checkbox
        self.include_subfolders_var = ctk.BooleanVar(value=False)
        self.include_subfolders_cb = ctk.CTkCheckBox(card, text=self.t("include_subfolders"), variable=self.include_subfolders_var, font=ThemeConfig.font_body(12))
        self.include_subfolders_cb.grid(row=2, column=1, padx=8, pady=(0, 6), sticky="w")

        # Destination
        self.dst_label = ctk.CTkLabel(card, text=self.t("dst_label"), font=ThemeConfig.font_title(13))
        self.dst_label.grid(row=3, column=0, padx=20, pady=(6, 20), sticky="w")
        self.dst_entry = ctk.CTkEntry(card, placeholder_text=self.t("dst_placeholder"), height=36, corner_radius=8,
                                      fg_color=ThemeConfig.BG_INPUT, border_color=ThemeConfig.BORDER_INPUT)
        self.dst_entry.grid(row=3, column=1, padx=8, pady=(6, 20), sticky="ew")
        self.dst_entry.insert(0, os.path.join(default_pics, "SORTED_OUTPUT"))
        self.dst_browse_btn = ctk.CTkButton(card, text=self.t("browse_btn"), width=110, height=36, corner_radius=8,
                                            fg_color=ThemeConfig.BTN_GHOST, hover_color=ThemeConfig.BTN_GHOST_HV, text_color=ThemeConfig.TEXT_MAIN,
                                            command=lambda: self._browse_dir(self.dst_entry))
        self.dst_browse_btn.grid(row=3, column=2, padx=20, pady=(6, 20))

    def _build_targets_card(self, parent, row):
        card = self._create_card(parent, row)
        card.grid_columnconfigure(0, weight=1)

        self.sec_targets_label = ctk.CTkLabel(card, text=self.t("section_targets"), font=ThemeConfig.font_title(13), text_color=ThemeConfig.TEXT_ACCENT)
        self.sec_targets_label.pack(anchor="w", padx=20, pady=(16, 8))

        # Pills
        self.target_type = ctk.StringVar(value="person_all")
        pills_fr = ctk.CTkFrame(card, fg_color=ThemeConfig.BG_PILL_GROUP, corner_radius=12)
        pills_fr.pack(fill="x", padx=20, pady=(0, 12))

        targets = [
            ("r_person", "target_person", "person_all"),
            ("r_doc", "target_doc", "document"),
            ("r_dog", "target_dog", "dog"),
            ("r_cat", "target_cat", "cat"),
            ("r_pet", "target_pet", "pet"),
            ("r_vehicle", "target_vehicle", "vehicle"),
        ]
        
        for attr, key, val in targets:
            rb = ctk.CTkRadioButton(pills_fr, text=self.t(key), variable=self.target_type, value=val, font=ThemeConfig.font_title(13))
            rb.pack(side="left", padx=14, pady=12)
            setattr(self, attr, rb)

        # Options
        opt_fr = ctk.CTkFrame(card, fg_color="transparent")
        opt_fr.pack(fill="x", padx=20, pady=(0, 16))
        
        # Media Type Selection
        self.media_type_label = ctk.CTkLabel(opt_fr, text=self.t("media_type_label"), font=ThemeConfig.font_title(13))
        self.media_type_label.pack(side="left", padx=(0, 10))
        
        self.media_type = ctk.StringVar(value="img")
        self.r_media_img = ctk.CTkRadioButton(opt_fr, text=self.t("media_img"), variable=self.media_type, value="img")
        self.r_media_img.pack(side="left", padx=10)
        self.r_media_vid = ctk.CTkRadioButton(opt_fr, text=self.t("media_vid"), variable=self.media_type, value="vid")
        self.r_media_vid.pack(side="left", padx=10)
        self.r_media_both = ctk.CTkRadioButton(opt_fr, text=self.t("media_both"), variable=self.media_type, value="both")
        self.r_media_both.pack(side="left", padx=10)
        
        # Spacer
        ctk.CTkFrame(opt_fr, width=2, height=20, fg_color=ThemeConfig.BORDER).pack(side="left", padx=20)

        self.mode_header_label = ctk.CTkLabel(opt_fr, text=self.t("mode_label"), font=ThemeConfig.font_title(13))
        self.mode_header_label.pack(side="left", padx=(0, 10))

        self.action_mode = ctk.StringVar(value="move")
        self.r_copy = ctk.CTkRadioButton(opt_fr, text=self.t("mode_copy"), variable=self.action_mode, value="copy")
        self.r_copy.pack(side="left", padx=10)
        self.r_move = ctk.CTkRadioButton(opt_fr, text=self.t("mode_move"), variable=self.action_mode, value="move")
        self.r_move.pack(side="left", padx=10)

        self.conf_val_label = ctk.CTkLabel(opt_fr, text="50%", font=ThemeConfig.font_title(13), text_color=ThemeConfig.TEXT_ACCENT)
        self.conf_val_label.pack(side="right", padx=(6, 0))
        self.conf_slider = ctk.CTkSlider(opt_fr, from_=0.25, to=0.85, number_of_steps=12, width=140, command=lambda v: self.conf_val_label.configure(text=f"{int(v*100)}%"))
        self.conf_slider.set(0.50)
        self.conf_slider.pack(side="right", padx=10)
        self.conf_header_label = ctk.CTkLabel(opt_fr, text=self.t("conf_label"), font=ThemeConfig.font_body(13))
        self.conf_header_label.pack(side="right", padx=(20, 2))

    def _build_monitor_card(self, parent, row):
        card = self._create_card(parent, row)
        card.grid(sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        top_fr = ctk.CTkFrame(card, fg_color="transparent")
        top_fr.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="ew")
        top_fr.grid_columnconfigure(0, weight=1)

        self.status_badge = ctk.CTkLabel(top_fr, text=self.t("status_ready"), font=ThemeConfig.font_title(13), text_color=ThemeConfig.SUCCESS)
        self.status_badge.grid(row=0, column=0, sticky="w")
        
        self.current_file_label = ctk.CTkLabel(top_fr, text="", font=ThemeConfig.font_mono(12), text_color=ThemeConfig.TEXT_SUB)
        self.current_file_label.grid(row=0, column=1, sticky="e")

        self.progress_bar = ctk.CTkProgressBar(card, height=14, corner_radius=7, fg_color=ThemeConfig.BORDER, progress_color=ThemeConfig.BTN_PRIMARY)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(4, 12), sticky="ew")
        self.progress_bar.set(0.0)

        self.log_textbox = ctk.CTkTextbox(card, font=ThemeConfig.font_mono(12), fg_color=ThemeConfig.BG_INPUT,
                                          text_color=ThemeConfig.TEXT_MAIN, border_width=1, border_color=ThemeConfig.BORDER_INPUT,
                                          corner_radius=12, wrap="none")
        self.log_textbox.grid(row=2, column=0, padx=20, pady=(0, 12), sticky="nsew")

        ribbon = ctk.CTkFrame(card, fg_color=ThemeConfig.BG_PILL_GROUP, corner_radius=12)
        ribbon.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        ribbon.grid_columnconfigure((0,1,2,3), weight=1)

        def make_stat(col, title, val, hl=False):
            f = ctk.CTkFrame(ribbon, fg_color="transparent")
            f.grid(row=0, column=col, padx=8, pady=10)
            ctk.CTkLabel(f, text=title, font=ThemeConfig.font_title(11), text_color=ThemeConfig.TEXT_SUB).pack()
            val_lbl = ctk.CTkLabel(f, text=val, font=ThemeConfig.font_title(16), text_color=ThemeConfig.TEXT_ACCENT if hl else ThemeConfig.TEXT_MAIN)
            val_lbl.pack()
            return val_lbl

        self.stat_val_total = make_stat(0, self.t("stat_box_total"), "0")
        self.stat_val_matched = make_stat(1, self.t("stat_box_matched"), "0", True)
        self.stat_val_time = make_stat(2, self.t("stat_box_time"), "0s")
        self.stat_val_eta = make_stat(3, self.t("stat_box_eta"), "--")
        
        # Store for translation updates
        self.stat_titles = ribbon.winfo_children()

    def _build_actions_card(self, parent, row):
        bar = ctk.CTkFrame(parent, fg_color="transparent")
        bar.grid(row=row, column=0, padx=24, pady=(4, 20), sticky="ew")
        bar.grid_columnconfigure(0, weight=3)
        bar.grid_columnconfigure(1, weight=1)

        self.start_btn = ctk.CTkButton(bar, text=self.t("start_btn"), font=ThemeConfig.font_title(16), height=52, corner_radius=12,
                                       fg_color=ThemeConfig.BTN_PRIMARY, hover_color=ThemeConfig.BTN_PRIMARY_HV, text_color="white",
                                       command=self.start_sorting)
        self.start_btn.grid(row=0, column=0, padx=(0, 12), sticky="ew")

        self.stop_btn = ctk.CTkButton(bar, text=self.t("stop_btn"), font=ThemeConfig.font_title(16), height=52, corner_radius=12,
                                      fg_color=ThemeConfig.BTN_DANGER, hover_color=ThemeConfig.BTN_DANGER_HV, text_color="white",
                                      state="disabled", command=self.stop_sorting)
        self.stop_btn.grid(row=0, column=1, padx=(12, 0), sticky="ew")

    # -------------------------------------------------------------------------
    # UI Interactions
    # -------------------------------------------------------------------------
    def _browse_dir(self, entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, os.path.normpath(folder))

    def change_theme(self, new_theme):
        self.current_theme = new_theme
        ctk.set_appearance_mode(new_theme)

    def change_language(self, new_lang):
        self.current_lang = new_lang
        self.title(self.t("app_title"))
        self.title_label.configure(text=self.t("header_title"))
        self.badge_label.configure(text=f"  {self.t('badge_offline')}  ")
        self.subtitle_label.configure(text=self.t("header_subtitle"))
        
        self.sec_folders_label.configure(text=self.t("section_folders"))
        self.src_label.configure(text=self.t("src_label"))
        self.src_browse_btn.configure(text=self.t("browse_btn"))
        self.include_subfolders_cb.configure(text=self.t("include_subfolders"))
        self.dst_label.configure(text=self.t("dst_label"))
        self.dst_browse_btn.configure(text=self.t("browse_btn"))

        self.sec_targets_label.configure(text=self.t("section_targets"))
        self.r_person.configure(text=self.t("target_person"))
        self.r_doc.configure(text=self.t("target_doc"))
        self.r_dog.configure(text=self.t("target_dog"))
        self.r_cat.configure(text=self.t("target_cat"))
        self.r_pet.configure(text=self.t("target_pet"))
        self.r_vehicle.configure(text=self.t("target_vehicle"))

        self.media_type_label.configure(text=self.t("media_type_label"))
        self.r_media_img.configure(text=self.t("media_img"))
        self.r_media_vid.configure(text=self.t("media_vid"))
        self.r_media_both.configure(text=self.t("media_both"))

        self.mode_header_label.configure(text=self.t("mode_label"))
        self.r_copy.configure(text=self.t("mode_copy"))
        self.r_move.configure(text=self.t("mode_move"))
        self.conf_header_label.configure(text=self.t("conf_label"))

        if not self.is_running:
            self.status_badge.configure(text=self.t("status_ready"))

        # Update stats titles
        for frame, key in zip(self.stat_titles, ["stat_box_total", "stat_box_matched", "stat_box_time", "stat_box_eta"]):
            frame.winfo_children()[0].configure(text=self.t(key))

        self.start_btn.configure(text=self.t("start_btn"))
        self.stop_btn.configure(text=self.t("stop_btn"))
        self.donate_btn.configure(text=self.t("donate_btn"))

    def log(self, msg: str):
        self.log_textbox.insert("end", f"{msg}\n")
        self.log_textbox.see("end")

    # -------------------------------------------------------------------------
    # Core Logic
    # -------------------------------------------------------------------------
    def _check_models(self):
        self.log(self.t("log_init_check"))
        
        self.yunet_path = get_resource_path("face_detection_yunet.onnx")
        if os.path.exists(self.yunet_path):
            self.log(self.t("log_yunet_found").format(name=os.path.basename(self.yunet_path)))
        else:
            self.log(self.t("log_yunet_missing"))
            self.yunet_path = None

        self.yolo_path = get_resource_path("yolov8n.pt")
        if os.path.exists(self.yolo_path):
            self.log(self.t("log_yolo_found").format(name=os.path.basename(self.yolo_path)))
        else:
            self.log(self.t("log_yolo_missing"))
            self.yolo_path = None

        self.log(self.t("log_doc_ready"))
        self.log(self.t("log_heic_ready") if HEIC_SUPPORT else self.t("log_heic_missing"))
        self.log(self.t("log_ready_hint"))

    def _load_image(self, filepath: Path):
        ext = filepath.suffix.lower()
        if ext == '.heic' and HEIC_SUPPORT:
            try:
                pil_img = Image.open(str(filepath)).convert('RGB')
                return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            except Exception:
                return None
        else:
            try: return cv2.imread(str(filepath))
            except Exception: return None

    def _is_doc(self, img, yolo=None) -> tuple[bool, str]:
        if img is None: return False, ""
        h, w = img.shape[:2]
        scale = min(1.0, 900 / max(h, w))
        small = cv2.resize(img, (int(w * scale), int(h * scale))) if scale < 1.0 else img
        sh, sw = small.shape[:2]
        s_tot = sh * sw

        # 1. Negative Filter: Reject Vehicles and Clutter if they take a large portion of frame
        if yolo:
            try:
                res = yolo.predict(small, conf=0.25, verbose=False)[0]
                clutter_classes = {
                    "car", "motorcycle", "bus", "truck", "boat", "train", "airplane",
                    "bottle", "cup", "bowl", "tv", "laptop", "mouse", "remote", 
                    "keyboard", "cell phone", "microwave", "oven", "toaster", 
                    "sink", "refrigerator", "chair", "couch", "bed", "dining table", 
                    "toilet", "bicycle", "suitcase", "backpack", "umbrella", "handbag"
                }
                for b in res.boxes:
                    cls_name = res.names[int(b.cls[0])]
                    bw_obj = float(b.xywh[0][2])
                    bh_obj = float(b.xywh[0][3])
                    obj_area_ratio = (bw_obj * bh_obj) / s_tot
                    if cls_name in clutter_classes and obj_area_ratio >= 0.15:
                        return False, ""
                    if cls_name == "person" and obj_area_ratio >= 0.20:
                        return False, ""
                    if cls_name == "book" and obj_area_ratio >= 0.40:
                        return False, ""
            except Exception:
                pass

        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        h_ch, s_ch, v_ch = cv2.split(hsv)

        # 2. Check for QR Code (PromptPay / Bank Transfer Slips / QR Invoices)
        try:
            ret, _, pts, _ = self.qr_detector.detectAndDecodeMulti(small)
            if ret and len(pts) > 0:
                light_pixels = np.sum(v_ch > 120) / s_tot
                if light_pixels >= 0.25:
                    return True, "Bank Transfer Slip / QR Code"
        except Exception:
            pass

        # 3. Paper Color Mask
        # A) White/Off-white/Gray paper: Sat < 38, Val > 115
        # B) Pastel Carbon Slips (Blue, Green, Pink, Purple): Hue in [35, 180], Sat < 120, Val > 135
        # C) Pale Yellow Slips: Hue in [15, 34], Sat < 45, Val > 150
        # (Explicitly filters out Brown Cardboard, Wood, Floor Tiles: Hue 10-30 with Sat > 45)
        white_paper = (s_ch < 38) & (v_ch > 115)
        # TIGHTENED PASTEL SLIP MASK TO EXCLUDE VIVID BLUE WATER/SKY
        pastel_slip = (h_ch >= 35) & (h_ch <= 160) & (s_ch < 60) & (v_ch > 150)
        yellow_slip = (h_ch >= 15) & (h_ch < 35) & (s_ch < 45) & (v_ch > 150)

        paper_mask = (white_paper | pastel_slip | yellow_slip).astype(np.uint8) * 255
        paper_ratio = np.sum(paper_mask > 0) / s_tot

        # 4. Text Line Detection
        gx = cv2.convertScaleAbs(cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3))
        _, th_edge = cv2.threshold(gx, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        valid_text_strokes = th_edge & paper_mask
        line_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (22, 2))
        connected_lines = cv2.morphologyEx(valid_text_strokes, cv2.MORPH_CLOSE, line_kernel)

        cnts, _ = cv2.findContours(connected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        text_lines = []
        y_centers = []
        total_text_area = 0

        for c in cnts:
            bx, by, bw, bh = cv2.boundingRect(c)
            asp = bw / bh if bh > 0 else 0
            area = bw * bh

            if 1.8 <= asp <= 55 and 3 <= bh <= 35 and bw >= 20 and area <= s_tot * 0.15:
                roi = valid_text_strokes[by:by+bh, bx:bx+bw]
                density = np.sum(roi > 0) / (bw * bh)
                if 0.07 <= density <= 0.65:
                    text_lines.append((bx, by, bw, bh))
                    y_centers.append(by + bh / 2)
                    total_text_area += area

        num_lines = len(text_lines)
        y_span = (max(y_centers) - min(y_centers)) / sh if len(y_centers) >= 4 else 0
        text_area_ratio = total_text_area / s_tot

        # 5. Connected Paper Region / Blob (for receipts in hand or documents on desk)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(paper_mask)
        max_blob_area_ratio = 0
        blob_bbox = None
        if num_labels > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            max_idx = np.argmax(areas) + 1
            max_blob_area_ratio = stats[max_idx, cv2.CC_STAT_AREA] / s_tot
            bx, by, bw, bh = stats[max_idx, cv2.CC_STAT_LEFT], stats[max_idx, cv2.CC_STAT_TOP], stats[max_idx, cv2.CC_STAT_WIDTH], stats[max_idx, cv2.CC_STAT_HEIGHT]
            blob_bbox = (bx, by, bw, bh)

        lines_in_main_blob = 0
        blob_y_centers = []
        if blob_bbox:
            bbx, bby, bbw, bbh = blob_bbox
            for (lx, ly, lw, lh) in text_lines:
                if bbx - 5 <= lx <= bbx + bbw + 5 and bby - 5 <= ly <= bby + bbh + 5:
                    lines_in_main_blob += 1
                    blob_y_centers.append(ly + lh / 2)

        blob_y_span = (max(blob_y_centers) - min(blob_y_centers)) / bbh if (blob_bbox and len(blob_y_centers) >= 4 and bbh > 0) else 0

        # 6. Classification Rules
        blob_aspect = 0
        if blob_bbox:
            _, _, bbw, bbh = blob_bbox
            blob_aspect = bbh / bbw if bbw > 0 else 0

        # Rule 1: Full-page Document / Invoice / A4 Sheet Scan (> 60% paper, bright)
        if paper_ratio >= 0.60 and np.mean(v_ch) >= 145:
            if num_lines >= 12 and y_span >= 0.45 and text_area_ratio >= 0.022 and (blob_aspect >= 1.10 or blob_aspect <= 0.75):
                return True, f"Paper Document ({num_lines} lines, {paper_ratio*100:.0f}% paper)"
            if num_lines >= 8 and y_span >= 0.60 and text_area_ratio >= 0.040 and (blob_aspect >= 1.10 or blob_aspect <= 0.75):
                return True, f"Slip/Document ({num_lines} lines)"
            if num_lines >= 8 and text_area_ratio >= 0.045 and y_span >= 0.38 and (blob_aspect >= 1.10 or blob_aspect <= 0.75):
                return True, f"Document/Slip ({num_lines} lines)"

        # Rule 2: Receipt / Bank Slip / Note (Held in hand or on desk, paper is 15% - 60% of image)
        if max_blob_area_ratio >= 0.15 and blob_bbox:
            if blob_aspect >= 1.10 and lines_in_main_blob >= 8 and blob_y_span >= 0.40 and text_area_ratio >= 0.022:
                return True, f"Receipt/Slip ({lines_in_main_blob} lines in paper)"
            if blob_aspect >= 1.25 and lines_in_main_blob >= 12 and blob_y_span >= 0.35 and text_area_ratio >= 0.022:
                return True, f"Thermal Receipt ({lines_in_main_blob} lines)"

        return False, ""

    def _check_video(self, filepath: Path, doc_on, yunet_on, yolo, y_cls, conf) -> tuple[bool, str]:
        try:
            cap = cv2.VideoCapture(str(filepath))
            if not cap.isOpened():
                return False, ""
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames <= 0:
                total_frames = 100
                
            check_points = [
                int(total_frames * 0.20),
                int(total_frames * 0.40),
                int(total_frames * 0.60),
                int(total_frames * 0.80)
            ]
            
            matched = False
            reason = ""
            
            for pt in check_points:
                if self.stop_requested: break
                cap.set(cv2.CAP_PROP_POS_FRAMES, pt)
                ret, frame = cap.read()
                if not ret or frame is None:
                    continue
                    
                # 1. Document
                if doc_on:
                    matched, reason = self._is_doc(frame, yolo)
                    if matched: break
                    
                # 2. YuNet
                if not matched and yunet_on and self.yunet_path:
                    h, w = frame.shape[:2]
                    sc = min(1.0, 640 / max(h, w))
                    nw, nh = int(w * sc), int(h * sc)
                    sml = cv2.resize(frame, (nw, nh)) if sc < 1.0 else frame
                    det = cv2.FaceDetectorYN_create(self.yunet_path, "", (nw, nh), score_threshold=conf, nms_threshold=0.3, top_k=5000)
                    _, faces = det.detect(sml)
                    if faces is not None and len(faces) > 0:
                        matched, reason = True, f"Face Video ({len(faces)})"
                        break
                        
                # 3. YOLO
                if not matched and yolo and y_cls:
                    res = yolo.predict(frame, conf=conf, classes=y_cls, verbose=False)
                    if res and len(res[0].boxes) > 0:
                        matched, reason = True, f"YOLO Video ({len(res[0].boxes)} obj)"
                        break
            
            cap.release()
            return matched, reason
        except Exception:
            return False, ""

    def start_sorting(self):
        src, dst = Path(self.src_entry.get().strip()), Path(self.dst_entry.get().strip())

        if not src.is_dir():
            return messagebox.showerror("Error", self.t("err_src_invalid"))
        
        # Permission check for source folder
        try:
            list(src.iterdir())
        except PermissionError:
            return messagebox.showerror("Error", self.t("err_permission"))
        
        if not dst.exists():
            try: dst.mkdir(parents=True, exist_ok=True)
            except PermissionError: return messagebox.showerror("Error", self.t("err_permission"))
            except Exception as e: return messagebox.showerror("Error", self.t("err_dst_create") + str(e))
        
        if src.resolve() == dst.resolve():
            return messagebox.showerror("Error", self.t("err_same_folder"))

        # Confirm Move operation
        if self.action_mode.get() == "move":
            confirm = messagebox.askyesno(self.t("confirm_move_title"), self.t("confirm_move_body"), icon="warning")
            if not confirm:
                return

        self.is_running = True
        self.stop_requested = False
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0.0)
        self.status_badge.configure(text=self.t("status_scanning"), text_color=ThemeConfig.TEXT_ACCENT)

        threading.Thread(target=self._run_worker, args=(src, dst), daemon=True).start()

    def stop_sorting(self):
        if self.is_running:
            self.stop_requested = True
            self.status_badge.configure(text=self.t("status_stopping"), text_color=ThemeConfig.ERROR)
            self.log(self.t("log_user_stopped"))

    def _run_worker(self, src: Path, dst: Path):
        t0 = time.time()
        mode, tgt, conf = self.action_mode.get(), self.target_type.get(), self.conf_slider.get()
        media = self.media_type.get()

        self.log(self.t("log_start_scan").format(src=src))
        self.log(self.t("log_target_info").format(target=tgt.upper(), mode=mode.upper(), conf=conf))

        target_exts = SUPPORTED_EXTENSIONS
        if media == "img":
            target_exts = SUPPORTED_EXTENSIONS - VIDEO_EXTENSIONS
        elif media == "vid":
            target_exts = VIDEO_EXTENSIONS

        if getattr(self, "include_subfolders_var", None) and self.include_subfolders_var.get():
            files = [f for f in src.rglob('*') if f.is_file() and f.suffix.lower() in target_exts]
        else:
            files = [f for f in src.iterdir() if f.is_file() and f.suffix.lower() in target_exts]
        if not files:
            self.log(self.t("log_no_images"))
            return self._finish_worker(0, 0, 0, t0)

        self.log(self.t("log_found_images").format(total=len(files)))
        self.stat_val_total.configure(text=str(len(files)))

        # Pre-load Models
        y_cls, yolo, yunet_on, doc_on = [], None, False, False
        if tgt == "document": doc_on = True
        elif tgt == "person_all": yunet_on, y_cls = True, [0]
        elif tgt == "dog": y_cls = [16]
        elif tgt == "cat": y_cls = [15]
        elif tgt == "pet": y_cls = [15, 16]
        elif tgt == "vehicle": y_cls = [1, 2, 3, 5, 7]

        if (y_cls or tgt == "document") and YOLO_AVAILABLE and self.yolo_path:
            try: yolo = YOLO(self.yolo_path)
            except Exception as e: self.log(f"⚠️ YOLO err: {e}")

        match_cnt, err_cnt = 0, 0

        for i, f in enumerate(files, 1):
            if self.stop_requested: break

            try:
                matched, reason = False, ""
                if f.suffix.lower() in VIDEO_EXTENSIONS:
                    matched, reason = self._check_video(f, doc_on, yunet_on, yolo, y_cls, conf)
                    if not matched and not reason:  # Error opening or reading video
                        pass 
                else:
                    img = self._load_image(f)
                    if img is None:
                        err_cnt += 1
                        continue
    
                    # Document
                    if doc_on:
                        matched, reason = self._is_doc(img, yolo)
    
                    # YuNet
                    if not matched and yunet_on and self.yunet_path:
                        h, w = img.shape[:2]
                        sc = min(1.0, 640 / max(h, w))
                        nw, nh = int(w * sc), int(h * sc)
                        sml = cv2.resize(img, (nw, nh)) if sc < 1.0 else img
                        det = cv2.FaceDetectorYN_create(self.yunet_path, "", (nw, nh), score_threshold=conf, nms_threshold=0.3, top_k=5000)
                        _, faces = det.detect(sml)
                        if faces is not None and len(faces) > 0:
                            matched, reason = True, f"Face ({len(faces)})"
    
                    # YOLO
                    if not matched and yolo and y_cls:
                        res = yolo.predict(img, conf=conf, classes=y_cls, verbose=False)
                        if res and len(res[0].boxes) > 0:
                            matched, reason = True, f"YOLO ({len(res[0].boxes)} obj)"

                if matched:
                    out = dst / f.name
                    if out.exists():
                        c = 1
                        while (dst / f"{f.stem}_{c}{f.suffix}").exists(): c += 1
                        out = dst / f"{f.stem}_{c}{f.suffix}"
                    
                    if mode == "move": shutil.move(str(f), str(out))
                    else: shutil.copy2(str(f), str(out))
                    
                    match_cnt += 1
                    self.log(f"  [{'MOV' if mode=='move' else 'CPY'}] {f.name} -> {reason}")

            except PermissionError:
                err_cnt += 1
                self.log(f"  [ERR] {f.name}: Permission denied — skipped")
            except Exception as e:
                err_cnt += 1
                self.log(f"  [ERR] {f.name}: {e}")

            # Update UI
            prog = i / len(files)
            elap = time.time() - t0
            rate = i / elap if elap > 0 else 0
            eta = (len(files) - i) / rate if rate > 0 else 0

            self.progress_bar.set(prog)
            self.current_file_label.configure(text=f"{f.name[:32]} ({prog*100:.1f}%)")
            self.stat_val_total.configure(text=f"{i}/{len(files)}")
            self.stat_val_matched.configure(text=str(match_cnt))
            self.stat_val_time.configure(text=f"{int(elap)}s")
            self.stat_val_eta.configure(text=f"~{int(eta)}s")

        self._finish_worker(len(files), match_cnt, err_cnt, t0)

    def _finish_worker(self, tot, mat, err, t0):
        elap = time.time() - t0
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        
        if not self.stop_requested:
            self.status_badge.configure(text=self.t("status_complete"), text_color=ThemeConfig.SUCCESS)
        else:
            self.status_badge.configure(text=self.t("status_stopped"), text_color=ThemeConfig.ERROR)
            
        unmat = tot - mat - err
        self.log(self.t("log_done_summary").format(elapsed=elap, total=tot, matched=mat, unmatched=unmat))

        if not self.stop_requested:
            messagebox.showinfo(self.t("msg_done_title"), self.t("msg_done_body").format(total=tot, matched=mat, elapsed=elap))

if __name__ == "__main__":
    app = ImageSorterApp()
    app.mainloop()
