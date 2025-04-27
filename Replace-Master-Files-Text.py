# !pip install ttkbootstrap # Ensure you have ttkbootstrap installed
import tkinter as tk
# from tkinter import ttk, filedialog, messagebox, scrolledtext # Original imports
import ttkbootstrap as ttk # Use ttkbootstrap
from ttkbootstrap.constants import * # Import constants like LEFT, RIGHT, TOP, BOTTOM, WORD, DISABLED, NORMAL, END, SUNKEN, W, E, NSEW, BOTH, VERTICAL, HORIZONTAL, RAISED
from tkinter import filedialog, messagebox, scrolledtext # Keep these standard tk modules
import os
import sys
import io
import shutil # For safer file saving
import re # For cleaning text (optional, but potentially useful)
import traceback # For detailed error logging


# --- Constants ---
APP_NAME = "Replace Master Files Text"
VERSION = "1.1" # Incremented version for multi-file open
DEFAULT_ENCODING = 'utf-8' # Default encoding
SEARCH_TAG = "search_highlight" # Tag for highlighting search results
# Separator template for displaying multiple files in the 'Before' pane
FILE_SEPARATOR_TEMPLATE = "\n\n--- File: {} ---\n\n"

# --- Language Strings (Add/Modify as needed for multi-file) ---
LANGUAGES = {
    "en": {
        "title": APP_NAME,
        "file": "File",
        "open": "Open File(s)...", # Changed label
        "save": "Save",
        "save_as": "Save Preview As...", # Clarified Save As action
        "exit": "Exit",
        "edit": "Edit",
        "copy": "Copy",
        "cut": "Cut",
        "paste": "Paste",
        "select_all": "Select All",
        "clear_all": "Clear All / Reset", # Clarified action
        "language": "Language",
        "english": "English",
        "arabic": "Arabic",
        "help": "Help",
        "about": "About",
        "search_for": "Search For (one per line):",
        "replace_with": "Replace With (corresponding line):",
        "perform_replace": "Preview Replacements",
        "clean_inputs": "Clean All",
        "before": "Before (Original Content):", # Updated label
        "after": "After (Preview):",
        "status_ready": "Ready. Open file(s) to begin.", # Updated default message
        "status_opened_single": "File opened: {}",
        "status_opened_multiple": "Opened {} files.",
        "status_opened_partial": "Opened {} of {} files. Some failed.",
        "status_opened_none": "Failed to open any selected files.",
        "status_saved_single": "File saved: {}",
        "status_saved_multiple": "Saved {} files.",
        "status_saved_partial": "Saved {} files. Some failed.",
        "status_save_failed": "Save failed for all files.",
        "status_saved_as": "Preview saved as: {}. Workspace reset.", # Updated Save As message
        "status_cleared": "All fields cleared. Workspace reset.",
        "status_replaced": "Preview generated. {} replacements shown across all content.", # Updated
        "status_no_file": "No file(s) loaded or content pasted.", # Updated
        "status_error": "Error: {}",
        "status_mismatch": "Error: Search and Replace lists must have the same number of lines.",
        "status_no_search": "Error: Search list cannot be empty.",
        "status_cleaned": "Input fields cleaned.",
        "status_search_found": "Found at index {}.",
        "status_search_not_found": "Phrase not found.",
        "about_title": "About " + APP_NAME,
        "about_text": f"{APP_NAME} Version {VERSION}\n\nA tool for searching and replacing multiple text blocks across files.\n\nCan open and save multiple files.\n\n'Save' overwrites originals, 'Save Preview As' saves the combined preview to a new file.\n\nTreats all files as text-based. Use with caution on binary files.\n\n  multi-file support, in-text search, and context menus!\n\nAll rights reserved MrGamesKingPro\n\nhttps://github.com/MrGamesKingPro.", # Updated about text
        "file_select_title": "Select File(s)", # Updated
        "file_types": (("All files", "*.*"),),
        "save_file_title": "Save Preview Content As", # Updated
        "warn_unsaved_title": "Unsaved Changes",
        "warn_unsaved_msg": "There are unsaved changes in the 'After' preview (relative to the original files).\nDo you want to save the changes to the original file(s) before proceeding?", # Updated message
        "warn_clear_title": "Confirm Clear / Reset",
        "warn_clear_msg": "Are you sure you want to clear all fields and reset the application state?\nAny loaded files and unsaved changes in the preview will be lost.",
        "search_in_pane": "Search:",
        "find_next": "Find Next",
        "rtl": False,
        "font": ('Segoe UI', 10),
        "text_align": LEFT,
        "status_title_multiple": "[Multiple Files]", # Title indicator
    },
    "ar": {
        "title": "ماستر استبدال ملفات النصوص",
        "file": "ملف",
        "open": "فتح ملف / ملفات...", # Changed label
        "save": "حفظ",
        "save_as": "حفظ المعاينة باسم...", # Clarified Save As action
        "exit": "خروج",
        "edit": "تحرير",
        "copy": "نسخ",
        "cut": "قص",
        "paste": "لصق",
        "select_all": "تحديد الكل",
        "clear_all": "مسح الكل / إعادة تعيين", # Clarified action
        "language": "اللغة",
        "english": "الإنجليزية",
        "arabic": "العربية",
        "help": "مساعدة",
        "about": "حول البرنامج",
        "search_for": ":ابحث عن (كل عنصر في سطر)",
        "replace_with": ":استبدل بـ (السطر المقابل)",
        "perform_replace": "معاينة الاستبدالات",
        "clean_inputs": "تنظيف الكل",
        "before": ":(المحتوى الأصلي) قبل", # Updated label
        "after": ":(معاينة) بعد",
        "status_ready": "جاهز. افتح ملف / ملفات للبدء.", # Updated default message
        "status_opened_single": "تم فتح الملف: {}",
        "status_opened_multiple": "تم فتح {} ملفات.",
        "status_opened_partial": "تم فتح {} من {} ملفات. فشل البعض.",
        "status_opened_none": "فشل فتح أي من الملفات المحددة.",
        "status_saved_single": "تم حفظ الملف: {}",
        "status_saved_multiple": "تم حفظ {} ملفات.",
        "status_saved_partial": "تم حفظ {} ملفات. فشل البعض.",
        "status_save_failed": "فشل حفظ جميع الملفات.",
        "status_saved_as": "تم حفظ المعاينة باسم: {}. إعادة تعيين مساحة العمل.", # Updated Save As message
        "status_cleared": "تم مسح جميع الحقول. إعادة تعيين مساحة العمل.",
        "status_replaced": "تم إنشاء المعاينة. تم عرض {} استبدالات عبر كل المحتوى.", # Updated
        "status_no_file": "لم يتم تحميل ملفات أو لصق محتوى.", # Updated
        "status_error": "خطأ: {}",
        "status_mismatch": "خطأ: يجب أن تحتوي قوائم البحث والاستبدال على نفس العدد من الأسطر.",
        "status_no_search": "خطأ: قائمة البحث لا يمكن أن تكون فارغة.",
        "status_cleaned": "تم تنظيف حقول الإدخال.",
        "status_search_found": "تم العثور عند المؤشر {}.",
        "status_search_not_found": "لم يتم العثور على النص.",
        "about_title": "حول " + "بحث واستبدال متعدد الأسطر",
        "about_text": f"ماستر استبدال ملفات النصوص {VERSION}\n\nبرنامج للبحث عن سطور نصية متعددة واستبدالها عبر الملفات.\n\nيمكن فتح وحفظ ملفات متعددة.\n\n'حفظ' يستبدل الملفات الأصلية، 'حفظ المعاينة باسم' يحفظ المعاينة المجمعة في ملف جديد.\nيعامل كل الملفات كنصية. استخدم بحذر مع الملفات الثنائية.\n\n  دعم ملفات متعددة، بحث ضمن النص، وقوائم سياق! \n\n MrGamesKingPro جميع الحقوق محفوظة  \n\n https://github.com/MrGamesKingPro ", # Updated about text
        "file_select_title": "اختر ملف / ملفات", # Updated
        "file_types": (("كل الملفات", "*.*"),),
        "save_file_title": "حفظ محتوى المعاينة باسم", # Updated
        "warn_unsaved_title": "تغييرات غير محفوظة",
        "warn_unsaved_msg": "هناك تغييرات غير محفوظة في معاينة 'بعد' (بالنسبة للملفات الأصلية).\nهل تريد حفظ التغييرات في الملف (الملفات) الأصلي قبل المتابعة؟", # Updated message
        "warn_clear_title": "تأكيد المسح / إعادة التعيين",
        "warn_clear_msg": "هل أنت متأكد أنك تريد مسح جميع الحقول وإعادة تعيين حالة التطبيق؟\nسيتم فقدان أي ملفات محملة وتغييرات غير محفوظة في المعاينة.",
        "search_in_pane": ":بحث",
        "find_next": "بحث عن التالي",
        "rtl": True,
        "font": ('Tahoma', 10),
        "text_align": RIGHT,
        "status_title_multiple": "[ملفات متعددة]", # Title indicator
    }
}


# --- Main Application Class ---
class SearchReplaceApp:
    def __init__(self, root):
        self.root = root
        # --- Data Structures for Multi-File ---
        self.current_file_paths = [] # List of paths for loaded files
        self.contents_before = []    # List of original content strings (one per file)
        self.encodings = []          # List of detected encodings (one per file)
        self.combined_content_before = "" # String for display in 'Before' pane

        # --- Other State Variables ---
        self.content_after = ""      # Combined preview content
        self.replacements_made = 0   # Total replacements shown in preview
        self.unsaved_changes = False # Flag if 'After' differs from original(s)
        self.current_lang = "en"     # Default language

        # Search state for Before/After panes
        self.search_before_pos = "1.0"
        self.search_after_pos = "1.0"

        # --- Window Setup ---
        self.root.geometry("950x750")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Paned Window for resizable sections ---
        self.paned_window = tk.PanedWindow(self.root, orient=VERTICAL, sashrelief=RAISED, bg=self.root["background"], sashwidth=8)
        self.paned_window.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # --- Top Frame (Search/Replace Inputs) ---
        self.top_frame = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(self.top_frame, height=180) # Initial height

        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        # Search Frame
        self.search_frame = ttk.Frame(self.top_frame, padding=5)
        self.search_frame.grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(0, 5))
        self.search_frame.rowconfigure(1, weight=1)
        self.search_frame.columnconfigure(0, weight=1)
        self.lbl_search = ttk.Label(self.search_frame, text=LANGUAGES[self.current_lang]["search_for"])
        self.lbl_search.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.txt_search = scrolledtext.ScrolledText(self.search_frame, wrap=WORD, height=6, width=40, font=LANGUAGES[self.current_lang]['font'])
        self.txt_search.grid(row=1, column=0, sticky=NSEW)
        self.txt_search.bind("<KeyRelease>", self.mark_unsaved_potential)

        # Replace Frame
        self.replace_frame = ttk.Frame(self.top_frame, padding=5)
        self.replace_frame.grid(row=0, column=1, rowspan=2, sticky=NSEW, padx=(5, 0))
        self.replace_frame.rowconfigure(1, weight=1)
        self.replace_frame.columnconfigure(0, weight=1)
        self.lbl_replace = ttk.Label(self.replace_frame, text=LANGUAGES[self.current_lang]["replace_with"])
        self.lbl_replace.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.txt_replace = scrolledtext.ScrolledText(self.replace_frame, wrap=WORD, height=6, width=40, font=LANGUAGES[self.current_lang]['font'])
        self.txt_replace.grid(row=1, column=0, sticky=NSEW)
        self.txt_replace.bind("<KeyRelease>", self.mark_unsaved_potential)

        # --- Middle Frame (Action Buttons) ---
        self.action_frame = ttk.Frame(self.paned_window, padding=(0, 5, 0, 5))
        self.paned_window.add(self.action_frame, height=50, stretch="never")
        self.action_button_frame = ttk.Frame(self.action_frame)
        self.action_button_frame.pack()
        self.btn_perform_replace = ttk.Button(self.action_button_frame, text=LANGUAGES[self.current_lang]["perform_replace"], command=self.perform_replace, bootstyle=SUCCESS)
        self.btn_perform_replace.pack(side=LEFT, padx=5, pady=5)
        self.btn_clean_inputs = ttk.Button(self.action_button_frame, text=LANGUAGES[self.current_lang]["clean_inputs"], command=self.clean_input_fields, bootstyle=INFO)
        self.btn_clean_inputs.pack(side=LEFT, padx=5, pady=5)


        # --- Bottom Frame (Before/After Preview) ---
        self.bottom_frame = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(self.bottom_frame, stretch="always")

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1) # Text area row expands
        self.bottom_frame.rowconfigure(3, weight=0) # Search row doesn't expand

        # Before Frame
        self.before_frame = ttk.Frame(self.bottom_frame, padding=5)
        self.before_frame.grid(row=0, column=0, rowspan=4, sticky=NSEW, padx=(0, 5))
        self.before_frame.rowconfigure(1, weight=1)
        self.before_frame.columnconfigure(0, weight=1)

        self.lbl_before = ttk.Label(self.before_frame, text=LANGUAGES[self.current_lang]["before"])
        self.lbl_before.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.txt_before = scrolledtext.ScrolledText(self.before_frame, wrap=WORD, state=NORMAL, font=LANGUAGES[self.current_lang]['font']) # Start NORMAL for pasting
        self.txt_before.grid(row=1, column=0, sticky=NSEW)
        self.txt_before.bind("<KeyRelease>", self.mark_unsaved_potential) # Mark potential changes if user types/pastes here directly
        self.search_before_frame = self.create_search_frame(self.before_frame, self.txt_before, "before")
        self.search_before_frame.grid(row=2, column=0, sticky=EW, pady=(5,0))


        # After Frame
        self.after_frame = ttk.Frame(self.bottom_frame, padding=5)
        self.after_frame.grid(row=0, column=1, rowspan=4, sticky=NSEW, padx=(5, 0))
        self.after_frame.rowconfigure(1, weight=1)
        self.after_frame.columnconfigure(0, weight=1)

        self.lbl_after = ttk.Label(self.after_frame, text=LANGUAGES[self.current_lang]["after"])
        self.lbl_after.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.txt_after = scrolledtext.ScrolledText(self.after_frame, wrap=WORD, state=DISABLED, font=LANGUAGES[self.current_lang]['font']) # Always starts disabled
        self.txt_after.grid(row=1, column=0, sticky=NSEW)
        self.search_after_frame = self.create_search_frame(self.after_frame, self.txt_after, "after")
        self.search_after_frame.grid(row=2, column=0, sticky=EW, pady=(5,0))

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=SUNKEN, anchor=W, padding=3)
        self.status_bar.pack(side=BOTTOM, fill=X, padx=5, pady=(0,5))
        self.set_status(LANGUAGES[self.current_lang]["status_ready"])

        # --- Menu Bar ---
        self.menu_bar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=LANGUAGES[self.current_lang]["file"], menu=self.file_menu)
        self.file_menu.add_command(label=LANGUAGES[self.current_lang]["open"], accelerator="Ctrl+O", command=self.open_files) # Changed command
        self.file_menu.add_command(label=LANGUAGES[self.current_lang]["save"], accelerator="Ctrl+S", command=self.save_files) # Changed command
        self.file_menu.add_command(label=LANGUAGES[self.current_lang]["save_as"], accelerator="Ctrl+Shift+S", command=self.save_preview_as) # Changed command
        self.file_menu.add_separator()
        self.file_menu.add_command(label=LANGUAGES[self.current_lang]["exit"], command=self.on_close)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=LANGUAGES[self.current_lang]["edit"], menu=self.edit_menu)
        self.edit_menu.add_command(label=LANGUAGES[self.current_lang]["copy"], accelerator="Ctrl+C", command=self.copy_text)
        self.edit_menu.add_command(label=LANGUAGES[self.current_lang]["cut"], accelerator="Ctrl+X", command=self.cut_text)
        self.edit_menu.add_command(label=LANGUAGES[self.current_lang]["paste"], accelerator="Ctrl+V", command=self.paste_text)
        self.edit_menu.add_command(label=LANGUAGES[self.current_lang]["select_all"], accelerator="Ctrl+A", command=self.select_all_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=LANGUAGES[self.current_lang]["clear_all"], command=self.clear_all_fields)

        # Language Menu
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=LANGUAGES[self.current_lang]["language"], menu=self.lang_menu)
        self.lang_menu.add_command(label=LANGUAGES[self.current_lang]["english"], command=lambda: self.change_language("en"))
        self.lang_menu.add_command(label=LANGUAGES[self.current_lang]["arabic"], command=lambda: self.change_language("ar"))

        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=LANGUAGES[self.current_lang]["help"], menu=self.help_menu)
        self.help_menu.add_command(label=LANGUAGES[self.current_lang]["about"], command=self.show_about)

        # --- Bind Keyboard Shortcuts ---
        self.root.bind_all("<Control-o>", lambda event: self.open_files()) # Changed command
        self.root.bind_all("<Control-s>", lambda event: self.save_files()) # Changed command
        self.root.bind_all("<Control-Shift-S>", lambda event: self.save_preview_as()) # Changed command
        self.root.bind_all("<Control-a>", self.select_all_text_event)

        # Bind Enter key in search entries to trigger find_next
        self.search_before_entry.bind("<Return>", lambda event: self.find_in_text(self.txt_before, self.search_before_entry, "before"))
        self.search_after_entry.bind("<Return>", lambda event: self.find_in_text(self.txt_after, self.search_after_entry, "after"))

        # --- Bind Context Menu ---
        self.txt_search.bind("<Button-3>", lambda e: self._show_context_menu(e, self.txt_search))
        self.txt_replace.bind("<Button-3>", lambda e: self._show_context_menu(e, self.txt_replace))
        self.txt_before.bind("<Button-3>", lambda e: self._show_context_menu(e, self.txt_before))
        self.txt_after.bind("<Button-3>", lambda e: self._show_context_menu(e, self.txt_after))

        # --- Apply Initial Language Settings ---
        self.update_ui_language()

        # --- Configure Search Highlight Tag ---
        style = ttk.Style()
        highlight_bg = "#FFA500" # Orange
        highlight_fg = "#000000"
        try:
             for txt_widget in [self.txt_before, self.txt_after, self.txt_search, self.txt_replace]:
                 txt_widget.tag_configure(SEARCH_TAG, background=highlight_bg, foreground=highlight_fg)
        except tk.TclError as e:
             print(f"Warning: Could not configure search highlight tag: {e}")

    # --- Context Menu Handling (Unchanged) ---
    # ... (Keep _show_context_menu, _context_cut, _context_copy, _context_paste, _context_select_all methods as they were) ...
    def _show_context_menu(self, event, text_widget):
        """Shows a context menu for ScrolledText widgets."""
        context_menu = tk.Menu(self.root, tearoff=0)
        lang = LANGUAGES[self.current_lang]

        # Determine widget state - allow actions based on widget role and content
        is_editable_input = text_widget in [self.txt_search, self.txt_replace]
        is_editable_before = text_widget is self.txt_before and not self.current_file_paths # Before is editable only if no file loaded
        is_editable = is_editable_input or is_editable_before

        has_selection = False
        has_content = False
        # Need to check state before accessing selection/content of disabled widgets
        original_state = text_widget.cget("state")
        widget_temporarily_enabled = False
        if original_state == DISABLED:
            text_widget.config(state=NORMAL)
            widget_temporarily_enabled = True

        try:
             has_selection = bool(text_widget.tag_ranges(tk.SEL))
             # Check content even if disabled (after enabling)
             has_content = bool(text_widget.get("1.0", END + "-1c").strip())
        except tk.TclError as e:
            print(f"Error checking text widget state for context menu: {e}")
        finally:
             if widget_temporarily_enabled:
                 text_widget.config(state=original_state) # Restore original state

        has_clipboard = False
        try:
            if text_widget.clipboard_get():
                has_clipboard = True
        except tk.TclError:
            has_clipboard = False
        except Exception as e:
             print(f"Error checking clipboard: {e}")
             has_clipboard = False

        # Add commands based on state
        context_menu.add_command(
            label=lang["cut"],
            command=lambda w=text_widget: self._context_cut(w),
            state=NORMAL if is_editable and has_selection else DISABLED
        )
        context_menu.add_command(
            label=lang["copy"],
            command=lambda w=text_widget: self._context_copy(w),
            state=NORMAL if has_selection else DISABLED # Can copy from disabled if selected
        )
        context_menu.add_command(
            label=lang["paste"],
            command=lambda w=text_widget: self._context_paste(w),
            state=NORMAL if is_editable and has_clipboard else DISABLED
        )
        context_menu.add_separator()
        context_menu.add_command(
            label=lang["select_all"],
            command=lambda w=text_widget: self._context_select_all(w),
            state=NORMAL if has_content else DISABLED # Enable only if there's content (check after enabling)
        )

        # Display the menu
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _context_cut(self, widget):
        """Handles Cut action from context menu."""
        # Double check editability here too
        is_editable_input = widget in [self.txt_search, self.txt_replace]
        is_editable_before = widget is self.txt_before and not self.current_file_paths
        if not (is_editable_input or is_editable_before): return

        try:
            widget.event_generate("<<Cut>>")
            # If cut from search/replace/before(manual), mark unsaved potential
            if widget in [self.txt_search, self.txt_replace, self.txt_before]:
                self.mark_unsaved_potential()
        except tk.TclError as e:
            print(f"Context Cut error: {e}")

    def _context_copy(self, widget):
        """Handles Copy action from context menu. Allows copying from disabled."""
        original_state = widget.cget("state")
        widget_temporarily_enabled = False
        if original_state == DISABLED:
            widget.config(state=NORMAL)
            widget_temporarily_enabled = True
        try:
            widget.event_generate("<<Copy>>")
        except tk.TclError as e:
            print(f"Context Copy error: {e}")
        finally:
            if widget_temporarily_enabled:
                widget.config(state=original_state)


    def _context_paste(self, widget):
        """Handles Paste action from context menu."""
        # Double check editability
        is_editable_input = widget in [self.txt_search, self.txt_replace]
        is_editable_before = widget is self.txt_before and not self.current_file_paths
        if not (is_editable_input or is_editable_before): return

        try:
            widget.event_generate("<<Paste>>")
            # If pasted into search/replace/before(manual), mark unsaved potential
            if widget in [self.txt_search, self.txt_replace, self.txt_before]:
                 self.mark_unsaved_potential()
        except tk.TclError as e:
            print(f"Context Paste error: {e}")

    def _context_select_all(self, widget):
        """Handles Select All action from context menu. Works on disabled."""
        original_state = widget.cget("state")
        widget_temporarily_enabled = False
        if original_state == DISABLED:
            widget.config(state=NORMAL)
            widget_temporarily_enabled = True
        try:
            widget.tag_add(tk.SEL, "1.0", END)
            widget.mark_set(tk.INSERT, "1.0") # Move cursor to start
            widget.see(tk.INSERT)
        except tk.TclError as e:
            print(f"Context Select All error: {e}")
        finally:
            if widget_temporarily_enabled:
                widget.config(state=original_state)


    # --- Helper to Create Search UI (Unchanged) ---
    def create_search_frame(self, parent, text_widget, pane_name):
        """Creates the search UI elements for a text pane."""
        frame = ttk.Frame(parent)
        frame.columnconfigure(1, weight=1) # Make entry expand

        lbl = ttk.Label(frame, text=LANGUAGES[self.current_lang]["search_in_pane"])
        entry = ttk.Entry(frame, font=LANGUAGES[self.current_lang]['font'])
        setattr(self, f"search_{pane_name}_entry", entry)

        btn = ttk.Button(frame, text=LANGUAGES[self.current_lang]["find_next"],
                         command=lambda: self.find_in_text(text_widget, entry, pane_name),
                         bootstyle=SECONDARY)

        setattr(self, f"search_{pane_name}_lbl", lbl)
        setattr(self, f"search_{pane_name}_btn", btn)

        lbl.grid(row=0, column=0, padx=(0, 5), sticky=W)
        entry.grid(row=0, column=1, padx=5, sticky=EW)
        btn.grid(row=0, column=2, padx=(5, 0), sticky=E)

        return frame

    # --- Search Functionality for Before/After (Unchanged) ---
    def find_in_text(self, text_widget, search_entry, pane_name):
        """Finds the next occurrence of text in the specified widget."""
        search_term = search_entry.get()
        if not search_term:
            self.set_status(LANGUAGES[self.current_lang]["status_search_not_found"] + " (Empty search term)")
            return

        text_widget.tag_remove(SEARCH_TAG, "1.0", END)
        start_pos = getattr(self, f"search_{pane_name}_pos", "1.0")
        search_target = text_widget

        try:
            current_state = search_target.cget("state")
            search_target.config(state=NORMAL)

            index = search_target.search(search_term, start_pos, stopindex=END, nocase=True)

            if index:
                end_index = f"{index}+{len(search_term)}c"
                search_target.tag_add(SEARCH_TAG, index, end_index)
                search_target.see(index)
                setattr(self, f"search_{pane_name}_pos", end_index)
                self.set_status(LANGUAGES[self.current_lang]["status_search_found"].format(index))
            else:
                setattr(self, f"search_{pane_name}_pos", "1.0")
                index = search_target.search(search_term, "1.0", stopindex=END, nocase=True)
                if index:
                    end_index = f"{index}+{len(search_term)}c"
                    search_target.tag_add(SEARCH_TAG, index, end_index)
                    search_target.see(index)
                    setattr(self, f"search_{pane_name}_pos", end_index)
                    self.set_status(LANGUAGES[self.current_lang]["status_search_found"].format(index) + " (Wrapped)")
                else:
                    self.set_status(LANGUAGES[self.current_lang]["status_search_not_found"])
                    self.root.bell()

        except tk.TclError as e:
            self.set_status(f"Search Error: {e}")
            traceback.print_exc() # More detail for debugging TclErrors
        except AttributeError:
             self.set_status(f"Search Error: Widget does not support search.")
        except Exception as e:
             self.set_status(f"Unexpected Search Error: {e}")
             traceback.print_exc()
        finally:
             search_target.config(state=current_state)

    # --- Clean Input Fields (Unchanged) ---
    def clean_input_fields(self):
        """Cleans whitespace from the search and replace input fields."""
        search_content = self.txt_search.get("1.0", END)
        replace_content = self.txt_replace.get("1.0", END)

        cleaned_search = [line.strip() for line in search_content.splitlines()]
        final_search = "\n".join(cleaned_search)

        cleaned_replace = [line.strip() for line in replace_content.splitlines()]
        final_replace = "\n".join(cleaned_replace)

        self._update_text_widget(self.txt_search, final_search + "\n")
        self._update_text_widget(self.txt_replace, final_replace + "\n")

        self.set_status(LANGUAGES[self.current_lang]["status_cleaned"])
        self.mark_unsaved_potential()


    # --- Core Logic Functions (Modified for Multi-File) ---

    def set_status(self, message, *args):
        """Updates the status bar."""
        try:
            self.status_var.set(message.format(*args))
        except Exception as e:
             self.status_var.set(f"Status formatting error: {e}")

    def mark_unsaved(self, is_unsaved=True):
        """Marks changes as unsaved and updates title."""
        if self.unsaved_changes != is_unsaved:
            self.unsaved_changes = is_unsaved

        title = LANGUAGES[self.current_lang]["title"]
        num_files = len(self.current_file_paths)

        if num_files == 1:
            try:
                basename = os.path.basename(self.current_file_paths[0])
                title += f" - {basename if basename else self.current_file_paths[0]}"
            except Exception:
                title += f" - {self.current_file_paths[0]}"
        elif num_files > 1:
            title += f" - {LANGUAGES[self.current_lang]['status_title_multiple']}"
        # If num_files is 0, just the base title is used

        if self.unsaved_changes:
            title += " *"
        self.root.title(title)

    def mark_unsaved_potential(self, event=None):
        """Called when search/replace/before(manual) terms change, implies preview is outdated or manual edits occurred."""
        # Preview is potentially outdated if search/replace terms change AND a preview exists
        preview_exists = bool(self.content_after.strip())
        inputs_changed = event and event.widget in [self.txt_search, self.txt_replace]

        # Direct edit to 'Before' pane when no file is loaded
        manual_before_edit = event and event.widget is self.txt_before and not self.current_file_paths

        if (inputs_changed and preview_exists) or manual_before_edit:
             self.mark_unsaved(True)


    def check_unsaved(self):
        """Checks for unsaved changes and prompts the user. Returns True to proceed, False to cancel."""
        if not self.unsaved_changes:
            return True

        # Determine if Save operation is possible (needs loaded files)
        can_save_originals = bool(self.current_file_paths)

        # Ask Yes/No/Cancel
        # Yes -> Save (if possible)
        # No -> Proceed without saving
        # Cancel -> Stop the current action
        response = messagebox.askyesnocancel(
            LANGUAGES[self.current_lang]["warn_unsaved_title"],
            LANGUAGES[self.current_lang]["warn_unsaved_msg"],
            parent=self.root,
        )

        if response is True:  # Yes (Save)
            if can_save_originals:
                return self.save_files() # Returns True if save succeeds, False otherwise
            else:
                # Cannot save originals (no files loaded), but user wants to save *something*.
                # Offer Save As for the preview instead.
                save_as_confirm = messagebox.askyesno(
                    LANGUAGES[self.current_lang]["save_file_title"], # Re-use title
                    "No original files are loaded.\nDo you want to save the current preview content to a new file?",
                    parent=self.root
                )
                if save_as_confirm:
                    return self.save_preview_as() # Returns True on success
                else:
                    # User said Yes to save, but No to Save As. Treat as Cancel.
                    return False
        elif response is False: # No (Don't Save)
            return True # Proceed with the original action (open, clear, exit etc.)
        else:  # Cancel
            return False # Cancel the original action


    def _detect_encoding(self, filepath):
        """Detects encoding for a single file."""
        detected_encoding = DEFAULT_ENCODING # Default assumption
        encodings_to_try = ['utf-8', 'cp1256', 'iso-8859-6', 'latin-1', 'cp1252', 'utf-16']
        try:
            with open(filepath, 'rb') as f:
                sample = f.read(1024) # Read a sample
                if sample.startswith(b'\xef\xbb\xbf'):
                    return 'utf-8-sig'
                elif sample.startswith(b'\xff\xfe') or sample.startswith(b'\xfe\xff'):
                    return 'utf-16'
                else:
                    # Try decoding with common encodings
                    for enc in encodings_to_try:
                        try:
                            # Use io.open to leverage text mode decoding nuances for the test read
                            with io.open(filepath, 'r', encoding=enc) as test_f:
                                test_f.read(1024) # Try reading as text
                            return enc # Success
                        except (UnicodeDecodeError, LookupError):
                            continue # Try next encoding
                        except Exception:
                            continue # Ignore other potential errors during test read

        except FileNotFoundError:
            raise # Let caller handle FileNotFoundError
        except PermissionError:
            raise # Let caller handle PermissionError
        except Exception as e:
            print(f"Encoding detection error for {os.path.basename(filepath)}: {e}. Using default {DEFAULT_ENCODING}")
            # Fallback to default if detection fails unexpectedly
            return DEFAULT_ENCODING

        # If loop finishes without finding a suitable encoding
        print(f"Could not reliably auto-detect encoding for {os.path.basename(filepath)}, using default {DEFAULT_ENCODING}")
        return DEFAULT_ENCODING


    def open_files(self, event=None):
        """Opens one or more files, replacing current content."""
        if not self.check_unsaved():
            return

        filepaths = filedialog.askopenfilenames( # Use askopenfilenames
            title=LANGUAGES[self.current_lang]["file_select_title"],
            filetypes=LANGUAGES[self.current_lang]["file_types"]
        )
        if not filepaths: # User cancelled
            return

        # --- Reset state before loading ---
        self._reset_workspace(clear_inputs=False) # Keep search/replace terms

        # --- Process selected files ---
        opened_files = 0
        failed_files = []
        combined_content_builder = []

        for i, filepath in enumerate(filepaths):
            try:
                detected_encoding = self._detect_encoding(filepath)

                print(f"Opening file '{filepath}' with encoding '{detected_encoding}'")
                with io.open(filepath, 'r', encoding=detected_encoding, errors='replace') as f:
                     content = f.read()

                # Append data for successfully opened file
                self.current_file_paths.append(filepath)
                self.contents_before.append(content)
                self.encodings.append(detected_encoding)

                # Add separator before appending content (except for the first file)
                if i > 0:
                    combined_content_builder.append(FILE_SEPARATOR_TEMPLATE.format("")) # Add separator without filename first
                # Now add file content
                combined_content_builder.append(content)

                opened_files += 1

            except FileNotFoundError:
                failed_files.append(f"{os.path.basename(filepath)} (Not Found)")
            except PermissionError:
                failed_files.append(f"{os.path.basename(filepath)} (Permission Denied)")
            except UnicodeDecodeError as e:
                 # Try to proceed with replacement characters if decode fails mid-way
                 print(f"Warning: UnicodeDecodeError for {os.path.basename(filepath)} with {detected_encoding}: {e}")
                 # Attempt to add potentially partial content with replacement chars
                 self.current_file_paths.append(filepath)
                 self.contents_before.append(content) # content might hold partial read
                 self.encodings.append(detected_encoding)
                 if i > 0: combined_content_builder.append(FILE_SEPARATOR_TEMPLATE.format(""))
                 combined_content_builder.append(content)
                 opened_files += 1 # Count as opened, but with issues
                 failed_files.append(f"{os.path.basename(filepath)} (Encoding Error: {e})")
            except Exception as e:
                failed_files.append(f"{os.path.basename(filepath)} (Error: {e})")
                traceback.print_exc()

        # --- Update UI and State after processing all files ---
        if opened_files > 0:
            # Rebuild combined content inserting actual filenames into separators now
            self.combined_content_before = ""
            final_builder = []
            for idx, content in enumerate(self.contents_before):
                filepath = self.current_file_paths[idx]
                if idx > 0:
                    final_builder.append(FILE_SEPARATOR_TEMPLATE.format(os.path.basename(filepath)))
                final_builder.append(content)
            self.combined_content_before = "".join(final_builder)


            self._update_text_widget(self.txt_before, self.combined_content_before)
            self.txt_before.config(state=DISABLED) # Disable 'Before' after loading files
            self._clear_text_widget(self.txt_after) # Clear previous preview
            self.content_after = ""
            self.replacements_made = 0
            self.mark_unsaved(False) # Freshly opened = saved state

            # Reset search positions
            self.search_before_pos = "1.0"
            self.search_after_pos = "1.0"
            if hasattr(self, 'search_before_entry'): self.search_before_entry.delete(0, END)
            if hasattr(self, 'search_after_entry'): self.search_after_entry.delete(0, END)
            self.txt_before.tag_remove(SEARCH_TAG, "1.0", END)
            self.txt_after.tag_remove(SEARCH_TAG, "1.0", END)

            # Update Status Bar
            if not failed_files:
                if opened_files == 1:
                    self.set_status(LANGUAGES[self.current_lang]["status_opened_single"], os.path.basename(self.current_file_paths[0]))
                else:
                    self.set_status(LANGUAGES[self.current_lang]["status_opened_multiple"], opened_files)
            else:
                self.set_status(LANGUAGES[self.current_lang]["status_opened_partial"], opened_files, len(filepaths))
                messagebox.showwarning("File Open Warning",
                                       f"Opened {opened_files} of {len(filepaths)} files.\nCould not open:\n- " + "\n- ".join(failed_files),
                                       parent=self.root)
        else:
            # No files opened successfully
            self.set_status(LANGUAGES[self.current_lang]["status_opened_none"])
            if failed_files:
                 messagebox.showerror("File Open Error",
                                      f"Failed to open any selected files.\nErrors:\n- " + "\n- ".join(failed_files),
                                      parent=self.root)
            # Ensure 'Before' is editable if nothing loaded
            self.txt_before.config(state=NORMAL)


    def perform_replace(self):
        """Performs the search and replace operation and updates the 'After' preview
           on the combined content."""
        # Reset 'After' search state before generating new preview
        self.search_after_pos = "1.0"
        self.txt_after.tag_remove(SEARCH_TAG, "1.0", END)

        # Determine the source content
        original_content_source = ""
        if self.current_file_paths:
            original_content_source = self.combined_content_before
        else:
            # If no files loaded, get content directly from 'Before' widget
            try:
                before_state = self.txt_before.cget("state")
                self.txt_before.config(state=NORMAL)
                original_content_source = self.txt_before.get("1.0", END + "-1c")
                self.txt_before.config(state=before_state) # Restore state
            except Exception as e:
                 print(f"Error reading txt_before for replacement: {e}")
                 self.set_status(LANGUAGES[self.current_lang]["status_error"].format("Could not read 'Before' content."))
                 return

        # Check if source is empty
        if not original_content_source.strip():
             self.set_status(LANGUAGES[self.current_lang]["status_no_file"])
             # Optionally show a warning message
             # messagebox.showwarning("No Content", "The 'Before' area is empty.", parent=self.root)
             # Clear preview if source is empty
             self._clear_text_widget(self.txt_after)
             self.content_after = ""
             self.replacements_made = 0
             self.mark_unsaved(False) # No content means no unsaved changes
             return

        # Get search and replace terms
        search_terms_raw = self.txt_search.get("1.0", tk.END).strip()
        replace_terms_raw = self.txt_replace.get("1.0", tk.END)
        if replace_terms_raw.endswith('\n'):
            replace_terms_raw = replace_terms_raw[:-1]

        if not search_terms_raw:
             self.set_status(LANGUAGES[self.current_lang]["status_no_search"])
             messagebox.showerror("Input Error", "The 'Search For' list cannot be empty.", parent=self.root)
             return

        search_terms = search_terms_raw.splitlines()
        replace_terms = replace_terms_raw.splitlines()

        if len(search_terms) != len(replace_terms):
            self.set_status(LANGUAGES[self.current_lang]["status_mismatch"])
            messagebox.showerror("Input Error", "The number of lines in 'Search For' must match the number of lines in 'Replace With'.", parent=self.root)
            return

        # Filter out pairs with empty search term
        valid_pairs = [(s, r) for s, r in zip(search_terms, replace_terms) if s]

        if not valid_pairs:
            self.set_status(LANGUAGES[self.current_lang]["status_no_search"])
            messagebox.showwarning("Input Error", "No valid (non-empty string) search terms provided.", parent=self.root)
            # Clear preview if no valid terms
            self._clear_text_widget(self.txt_after)
            self.content_after = ""
            self.replacements_made = 0
            self.mark_unsaved(False)
            return

        # --- Perform Replacement on the source content ---
        temp_content = original_content_source
        total_replacements = 0
        try:
            for search, replace in valid_pairs:
                # Count occurrences *before* replacing this term
                count = temp_content.count(search)
                if count > 0:
                    temp_content = temp_content.replace(search, replace)
                    total_replacements += count

            self.content_after = temp_content # Store the combined result

        except Exception as e:
             self.set_status(LANGUAGES[self.current_lang]["status_error"], f"Replacement error: {e}")
             messagebox.showerror("Replacement Error", f"An error occurred during the replacement process:\n{e}", parent=self.root)
             self._clear_text_widget(self.txt_after)
             self.content_after = ""
             traceback.print_exc()
             return

        # --- Update Preview Pane ---
        self.replacements_made = total_replacements
        self._update_text_widget(self.txt_after, self.content_after)
        self.txt_after.config(state=DISABLED) # Ensure 'After' is disabled
        self.set_status(LANGUAGES[self.current_lang]["status_replaced"], self.replacements_made)

        # --- Mark Unsaved ---
        # Mark unsaved *only if* the final preview differs from the initial source
        if self.content_after != original_content_source:
             self.mark_unsaved(True)
        else:
             # If replace resulted in no change, ensure not marked unsaved
             self.mark_unsaved(False)


    def _get_valid_replacement_pairs(self):
        """Gets and validates search/replace terms, returning valid pairs or None."""
        search_terms_raw = self.txt_search.get("1.0", tk.END).strip()
        replace_terms_raw = self.txt_replace.get("1.0", tk.END)
        if replace_terms_raw.endswith('\n'):
            replace_terms_raw = replace_terms_raw[:-1]

        if not search_terms_raw:
             self.set_status(LANGUAGES[self.current_lang]["status_no_search"])
             messagebox.showerror("Input Error", "The 'Search For' list cannot be empty.", parent=self.root)
             return None

        search_terms = search_terms_raw.splitlines()
        replace_terms = replace_terms_raw.splitlines()

        if len(search_terms) != len(replace_terms):
            self.set_status(LANGUAGES[self.current_lang]["status_mismatch"])
            messagebox.showerror("Input Error", "The number of lines in 'Search For' must match the number of lines in 'Replace With'.", parent=self.root)
            return None

        valid_pairs = [(s, r) for s, r in zip(search_terms, replace_terms) if s]

        if not valid_pairs:
            self.set_status(LANGUAGES[self.current_lang]["status_no_search"])
            messagebox.showwarning("Input Error", "No valid (non-empty string) search terms provided.", parent=self.root)
            return None

        return valid_pairs

    def save_files(self, event=None):
        """Saves modified content back to the original files."""
        if not self.current_file_paths:
            # If no files loaded, maybe try saving the preview 'As'?
            # Or just state nothing to save. Let's do the latter for 'Save'.
            self.set_status(LANGUAGES[self.current_lang]["status_no_file"] + " (Cannot perform 'Save')")
            return False # Indicate save did not happen

        if not self.unsaved_changes:
            self.set_status(LANGUAGES[self.current_lang]["status_ready"] + " (No changes to save)")
            return True # Indicate 'success' as there was nothing to do

        # Get the replacement rules
        valid_pairs = self._get_valid_replacement_pairs()
        if valid_pairs is None:
            return False # Stop if terms are invalid

        # --- Perform replacements and save each file individually ---
        success_count = 0
        fail_count = 0
        errors = []
        new_contents_before = [] # To store the successfully saved content

        for i, original_content in enumerate(self.contents_before):
            filepath = self.current_file_paths[i]
            encoding = self.encodings[i]
            basename = os.path.basename(filepath)

            # Apply replacements to this specific file's original content
            modified_content = original_content
            file_had_changes = False
            try:
                for search, replace in valid_pairs:
                    if search in modified_content: # Optimization: check if search term exists
                        new_modified_content = modified_content.replace(search, replace)
                        if new_modified_content != modified_content:
                            modified_content = new_modified_content
                            file_had_changes = True # Mark that this specific file changed

            except Exception as e:
                 print(f"Error applying replacements to {basename}: {e}")
                 errors.append(f"{basename}: Replacement error ({e})")
                 fail_count += 1
                 new_contents_before.append(original_content) # Keep original content if replacement fails
                 traceback.print_exc()
                 continue # Skip saving this file

            # Save only if the content for this file actually changed
            if file_had_changes:
                temp_filepath = filepath + ".tmp_save"
                try:
                    print(f"Saving file '{filepath}' with encoding '{encoding}'")
                    with io.open(temp_filepath, 'w', encoding=encoding, errors='replace') as f:
                        f.write(modified_content)
                    shutil.move(temp_filepath, filepath)
                    success_count += 1
                    new_contents_before.append(modified_content) # Store saved content

                except PermissionError as e:
                     errors.append(f"{basename}: Save failed (Permission Denied)")
                     fail_count += 1
                     new_contents_before.append(original_content) # Revert to original on save failure
                except OSError as e:
                     errors.append(f"{basename}: Save failed (OS Error: {e})")
                     fail_count += 1
                     new_contents_before.append(original_content)
                except Exception as e:
                    errors.append(f"{basename}: Save failed (Error: {e})")
                    fail_count += 1
                    new_contents_before.append(original_content)
                    traceback.print_exc()

                # Cleanup temp file if move failed/wasn't reached
                if os.path.exists(temp_filepath):
                    try: os.remove(temp_filepath)
                    except Exception as rem_e: print(f"Error removing temp file for {basename}: {rem_e}")
            else:
                # No changes for this file, keep original content
                new_contents_before.append(original_content)
                # Should we count this as success? Yes, as no action was needed.
                success_count += 1


        # --- Update state based on overall success ---
        if fail_count == 0:
            self.contents_before = new_contents_before # Update original content list
            # Rebuild combined content for 'Before' pane
            final_builder = []
            for idx, content in enumerate(self.contents_before):
                 filepath = self.current_file_paths[idx]
                 if idx > 0:
                     final_builder.append(FILE_SEPARATOR_TEMPLATE.format(os.path.basename(filepath)))
                 final_builder.append(content)
            self.combined_content_before = "".join(final_builder)

            self._update_text_widget(self.txt_before, self.combined_content_before)
            self.txt_before.config(state=DISABLED) # Re-disable 'Before'

            # Reset search state for 'Before' as its content might have changed
            self.search_before_pos = "1.0"
            self.txt_before.tag_remove(SEARCH_TAG, "1.0", END)

            self.mark_unsaved(False) # Mark as saved

            if len(self.current_file_paths) == 1:
                self.set_status(LANGUAGES[self.current_lang]["status_saved_single"].format(os.path.basename(self.current_file_paths[0])))
            else:
                self.set_status(LANGUAGES[self.current_lang]["status_saved_multiple"].format(success_count))
            return True
        else:
            # Some or all failed
            if success_count > 0:
                 self.set_status(LANGUAGES[self.current_lang]["status_saved_partial"].format(success_count))
            else:
                 self.set_status(LANGUAGES[self.current_lang]["status_save_failed"])

            messagebox.showerror("Save Error",
                                 f"Failed to save {fail_count} file(s).\nErrors:\n- " + "\n- ".join(errors),
                                 parent=self.root)
            # Do NOT mark as saved, keep unsaved_changes = True
            # Do NOT update contents_before or txt_before, keep the pre-save state visible
            return False


    def save_preview_as(self, event=None):
        """Saves the content of the 'After' preview (combined) to a new file and resets."""
        content_to_save = self.content_after
        source_info = "'After' preview"

        # If 'After' is empty, check if 'Before' has content to save instead
        if not content_to_save.strip():
            current_before_text = ""
            # Determine source of 'Before' content (loaded files or manual paste)
            if self.combined_content_before:
                current_before_text = self.combined_content_before
                source_info = "original loaded content" if len(self.current_file_paths)>1 else f"original '{os.path.basename(self.current_file_paths[0])}'"
            else:
                 # Try reading from widget if no files loaded
                 try:
                     before_state = self.txt_before.cget("state")
                     self.txt_before.config(state=NORMAL)
                     current_before_text = self.txt_before.get("1.0", END + "-1c")
                     self.txt_before.config(state=before_state)
                     if current_before_text.strip():
                          source_info = "current 'Before' content (pasted)"
                 except Exception as e:
                      print(f"Error reading txt_before for Save As check: {e}")


            if current_before_text.strip():
                response = messagebox.askyesno(
                    "Save As Warning",
                    f"The 'After' preview is empty.\nDo you want to save the {source_info} to a new file instead?",
                    parent=self.root
                )
                if response:
                     content_to_save = current_before_text
                else:
                     self.set_status("Save As cancelled - Nothing to save.")
                     # messagebox.showinfo("Nothing to Save", "There is no content in the 'After' preview to save.", parent=self.root)
                     return False # Cancelled
            else:
                 self.set_status(LANGUAGES[self.current_lang]["status_ready"] + " (Nothing to save)")
                 messagebox.showinfo("Nothing to Save", "There is no content in the 'Before' or 'After' areas to save.", parent=self.root)
                 return False # Nothing to save

        # --- Ask for filename ---
        initial_filename = "combined_preview_content"
        if len(self.current_file_paths) == 1:
             try:
                 initial_filename = "modified_" + os.path.basename(self.current_file_paths[0])
             except Exception: pass
        elif len(self.current_file_paths) > 1:
            initial_filename = "combined_modified_files"

        filepath = filedialog.asksaveasfilename(
            title=LANGUAGES[self.current_lang]["save_file_title"],
            filetypes=LANGUAGES[self.current_lang]["file_types"],
            defaultextension=".txt",
            initialfile=initial_filename
        )

        if not filepath:
            return False # User cancelled

        # --- Save the chosen content (combined) to the new file ---
        temp_filepath = filepath + ".tmp_save"
        try:
             # Save combined preview always using default encoding (UTF-8) for simplicity
             save_encoding = DEFAULT_ENCODING
             print(f"Saving combined preview to '{filepath}' with encoding '{save_encoding}'")
             with io.open(temp_filepath, 'w', encoding=save_encoding, errors='replace') as f:
                f.write(content_to_save)
             shutil.move(temp_filepath, filepath)

             # --- Reset Workspace: Treat the saved file as the new single 'Before' state ---
             new_basename = os.path.basename(filepath)

             # Clear multi-file state
             self.current_file_paths = [filepath]
             self.contents_before = [content_to_save]
             self.encodings = [save_encoding]
             self.combined_content_before = content_to_save # Combined is just the single file now

             # Update UI
             self._update_text_widget(self.txt_before, self.combined_content_before)
             self.txt_before.config(state=DISABLED) # It's now 'saved' content
             self._clear_text_widget(self.txt_after)
             self.content_after = ""
             self.replacements_made = 0

             # Reset search states
             self.search_before_pos = "1.0"
             self.search_after_pos = "1.0"
             self.txt_before.tag_remove(SEARCH_TAG, "1.0", END)
             self.txt_after.tag_remove(SEARCH_TAG, "1.0", END)
             if hasattr(self, 'search_before_entry'): self.search_before_entry.delete(0, END)
             if hasattr(self, 'search_after_entry'): self.search_after_entry.delete(0, END)

             self.mark_unsaved(False) # Mark as saved
             self.set_status(LANGUAGES[self.current_lang]["status_saved_as"].format(new_basename))
             return True

        except PermissionError as e:
             self.set_status(LANGUAGES[self.current_lang]["status_error"], f"Save As failed (Permission): {e}")
             messagebox.showerror("Save Error", f"Could not save file as (Permission Denied):\n{filepath}\n\nError: {e}", parent=self.root)
        except OSError as e:
             self.set_status(LANGUAGES[self.current_lang]["status_error"], f"Save As failed (OS Error): {e}")
             messagebox.showerror("Save Error", f"Could not save file as (OS Error):\n{filepath}\n\nError: {e}", parent=self.root)
        except Exception as e:
            self.set_status(LANGUAGES[self.current_lang]["status_error"], f"Save As failed: {e}")
            messagebox.showerror("Save Error", f"Could not save the file as:\n{filepath}\n\nError: {e}", parent=self.root)
            traceback.print_exc()

        # Cleanup temp file if move failed
        if os.path.exists(temp_filepath):
            try: os.remove(temp_filepath)
            except Exception as rem_e: print(f"Error removing temp file: {rem_e}")
        return False


    def _reset_workspace(self, clear_inputs=True):
        """Resets the main workspace state (files, content, preview)."""
        # Clear multi-file data
        self.current_file_paths = []
        self.contents_before = []
        self.encodings = []
        self.combined_content_before = ""

        # Clear preview data
        self.content_after = ""
        self.replacements_made = 0

        # Clear UI Panes
        if clear_inputs:
            self._clear_text_widget(self.txt_search)
            self._clear_text_widget(self.txt_replace)
        self._clear_text_widget(self.txt_before)
        self._clear_text_widget(self.txt_after)

        # Clear search entries
        if hasattr(self, 'search_before_entry'): self.search_before_entry.delete(0, END)
        if hasattr(self, 'search_after_entry'): self.search_after_entry.delete(0, END)

        # Reset search positions
        self.search_before_pos = "1.0"
        self.search_after_pos = "1.0"

        # Reset unsaved flag and title
        self.mark_unsaved(False)

        # Set 'Before' state (allow pasting if no files loaded)
        self.txt_before.config(state=NORMAL)
        self.txt_after.config(state=DISABLED) # Ensure 'After' is disabled


    def clear_all_fields(self):
        """Clears all text fields and resets the entire application state."""
        # Check if there's anything significant to lose
        has_text_in_inputs = (self.txt_search.get("1.0", END + "-1c").strip() or
                              self.txt_replace.get("1.0", END + "-1c").strip())
        has_preview = self.content_after.strip()
        has_loaded_files = bool(self.current_file_paths)
        has_pasted_content = (not has_loaded_files and
                                self.txt_before.get("1.0", END + "-1c").strip())

        # Prompt for confirmation if there are loaded files, unsaved changes, or any significant text
        if self.unsaved_changes or has_loaded_files or has_text_in_inputs or has_pasted_content:
            # Check unsaved changes first (prompts to save if needed)
             if self.unsaved_changes:
                  if not self.check_unsaved(): # Asks to save preview/originals
                       return # User cancelled save prompt

             # If check_unsaved passed (or no unsaved changes initially),
             # ask for final confirmation to clear everything else.
             confirm = messagebox.askyesno(
                 LANGUAGES[self.current_lang]["warn_clear_title"],
                 LANGUAGES[self.current_lang]["warn_clear_msg"],
                 parent=self.root)
             if not confirm:
                  return

        # --- Proceed with Clearing ---
        self._reset_workspace(clear_inputs=True) # Full reset
        self.set_status(LANGUAGES[self.current_lang]["status_cleared"])
        self.root.title(LANGUAGES[self.current_lang]["title"]) # Reset title completely


    # --- Edit Functions (Target Focused Widget - Unchanged logic, but consider txt_before state) ---
    # ... (Keep get_focused_text_widget, copy_text, cut_text, paste_text, select_all_text, select_all_text_event as they were) ...
    # Note: cut/paste on txt_before should only work if no files are loaded. Context menu handlers updated for this.
    # Menu/shortcut handlers might need slight adjustment if directly calling widget methods instead of context helpers.
    # Let's refine cut/paste/select_all to use the context helpers for consistency.

    def get_focused_text_widget(self):
        """Identifies the text or scrolledtext widget that currently has focus."""
        try:
            focused = self.root.focus_get()
            if not focused: return None

            # Check our main ScrolledText widgets
            # Need to handle inner tk.Text focus for ScrolledText
            if isinstance(focused, tk.Text):
                master = getattr(focused, 'master', None)
                if isinstance(master, scrolledtext.ScrolledText):
                    focused = master # Treat focus on inner Text as focus on outer ScrolledText

            if focused is self.txt_search: return self.txt_search
            if focused is self.txt_replace: return self.txt_replace
            if focused is self.txt_before: return self.txt_before
            if focused is self.txt_after: return self.txt_after

            # Check the Entry widgets
            if hasattr(self, 'search_before_entry') and focused is self.search_before_entry: return self.search_before_entry
            if hasattr(self, 'search_after_entry') and focused is self.search_after_entry: return self.search_after_entry

        except Exception as e:
            print(f"Error getting focused widget: {e}")
        return None

    def copy_text(self, event=None):
        """Handles Copy action (Menu/Shortcut)."""
        widget = self.get_focused_text_widget()
        if isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
            self._context_copy(widget) # Use the context menu helper
        elif isinstance(widget, ttk.Entry):
             try: widget.event_generate("<<Copy>>")
             except tk.TclError: pass

    def cut_text(self, event=None):
        """Handles Cut action (Menu/Shortcut)."""
        widget = self.get_focused_text_widget()
        if isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
             # Check editability before attempting cut via context helper
             is_editable_input = widget in [self.txt_search, self.txt_replace]
             is_editable_before = widget is self.txt_before and not self.current_file_paths
             if is_editable_input or is_editable_before:
                 self._context_cut(widget)
        elif isinstance(widget, ttk.Entry):
             try: widget.event_generate("<<Cut>>")
             except tk.TclError: pass


    def paste_text(self, event=None):
        """Handles Paste action (Menu/Shortcut)."""
        widget = self.get_focused_text_widget()
        if isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
             # Check editability before attempting paste via context helper
             is_editable_input = widget in [self.txt_search, self.txt_replace]
             is_editable_before = widget is self.txt_before and not self.current_file_paths
             if is_editable_input or is_editable_before:
                 self._context_paste(widget)
        elif isinstance(widget, ttk.Entry):
             try: widget.event_generate("<<Paste>>")
             except tk.TclError: pass


    def select_all_text(self, event=None): # Renamed menu command handler slightly
        """Handles Select All action from Edit Menu."""
        widget = self.get_focused_text_widget()
        if isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
            self._context_select_all(widget) # Use the context menu helper
        elif isinstance(widget, ttk.Entry):
             widget.select_range(0, END)
             widget.icursor(END)


    def select_all_text_event(self, event):
        """Handles Select All for Ctrl+A keybinding."""
        # event.widget should give the widget that received the event
        widget = event.widget

        # Need to handle inner Text vs outer ScrolledText again
        target_widget = None
        if isinstance(widget, tk.Text):
             master = getattr(widget, 'master', None)
             if isinstance(master, scrolledtext.ScrolledText):
                  target_widget = master # Use the ScrolledText instance
             else:
                 target_widget = widget # It's just a Text widget (shouldn't happen here)
        elif isinstance(widget, scrolledtext.ScrolledText):
             target_widget = widget
        elif isinstance(widget, ttk.Entry):
             target_widget = widget

        # Apply select all using context helper or standard methods
        if isinstance(target_widget, scrolledtext.ScrolledText):
            # Check if it's one of ours
            if target_widget in [self.txt_search, self.txt_replace, self.txt_before, self.txt_after]:
                 self._context_select_all(target_widget)
                 return "break"
        elif isinstance(target_widget, ttk.Entry):
             # Check if it's one of ours
             is_search_entry = False
             if hasattr(self, 'search_before_entry') and target_widget is self.search_before_entry: is_search_entry = True
             if hasattr(self, 'search_after_entry') and target_widget is self.search_after_entry: is_search_entry = True
             if is_search_entry:
                 target_widget.select_range(0, END)
                 target_widget.icursor(END)
                 return "break"

        # Allow default Ctrl+A behavior for other potential widgets
        return None


    # --- Help and Language (Update UI elements, Check status translation) ---

    def show_about(self):
        """Displays the About dialog."""
        messagebox.showinfo(
            LANGUAGES[self.current_lang]["about_title"],
            LANGUAGES[self.current_lang]["about_text"].format(VERSION=VERSION),
            parent=self.root
        )

    def change_language(self, lang_code):
        """Switches the UI language."""
        if lang_code in LANGUAGES and self.current_lang != lang_code:
            if not self.check_unsaved():
                 return

            self.current_lang = lang_code
            # Store current status before updating UI (which might change keys)
            current_status_text = self.status_var.get()
            # Find the key corresponding to the current status in the *old* language
            old_lang_code = "en" if lang_code == "ar" else "ar"
            status_key = None
            status_args = []
            for key, value in LANGUAGES[old_lang_code].items():
                 if key.startswith("status_"):
                     # Simple check: if the value (template) is a prefix of the current status
                     template_base = value.split("{}")[0]
                     if current_status_text.startswith(template_base):
                          # Potential match, try to extract args
                          if "{}" in value:
                               try:
                                   # Basic extraction, might fail for complex formats
                                   parts = value.split("{}")
                                   arg_part = current_status_text
                                   if parts[0]: arg_part = arg_part.split(parts[0], 1)[1]
                                   if parts[1]: arg_part = arg_part.rsplit(parts[1], 1)[0]
                                   # If multiple {}, this simple logic fails. Assume one arg for now.
                                   status_args = [arg_part.strip()]
                                   # Verify format roughly matches
                                   if value.format(*status_args) == current_status_text:
                                        status_key = key
                                        break
                               except Exception:
                                   pass # Ignore extraction errors
                          elif value == current_status_text: # Exact match for statuses without args
                              status_key = key
                              break

            # Update all UI elements to the new language
            self.update_ui_language()

            # Now, try to set the status bar using the found key in the *new* language
            new_status = LANGUAGES[self.current_lang]["status_ready"] # Default
            if status_key and status_key in LANGUAGES[self.current_lang]:
                 new_template = LANGUAGES[self.current_lang][status_key]
                 try:
                     if status_args and new_template.count("{}") == len(status_args):
                         new_status = new_template.format(*status_args)
                     elif not status_args and "{}" not in new_template:
                          new_status = new_template
                     else:
                          # Fallback if arg count mismatch
                          print(f"Status arg mismatch translating key '{status_key}'. Falling back.")
                          new_status = new_template.split("{}")[0].strip() # Use base part

                 except Exception as e:
                     print(f"Error formatting translated status for key '{status_key}': {e}")
                     new_status = LANGUAGES[self.current_lang]["status_ready"] # Fallback hard
            else:
                 print(f"Could not translate status key for: '{current_status_text}'")

            self.status_var.set(new_status)
            # Re-apply title with new language and correct unsaved marker
            self.mark_unsaved(self.unsaved_changes)


    def update_ui_language(self):
        """Applies the current language strings to all UI elements."""
        lang_dict = LANGUAGES[self.current_lang]
        is_rtl = lang_dict["rtl"]
        font_tuple = lang_dict["font"]
        text_align = lang_dict["text_align"]

        self.mark_unsaved(self.unsaved_changes) # Update window title first

        # --- Update Menus ---
        try: self.menu_bar.entryconfig(LANGUAGES["en"]["file"], label=lang_dict["file"])
        except tk.TclError: pass
        try: self.menu_bar.entryconfig(LANGUAGES["en"]["edit"], label=lang_dict["edit"])
        except tk.TclError: pass
        try: self.menu_bar.entryconfig(LANGUAGES["en"]["language"], label=lang_dict["language"])
        except tk.TclError: pass
        try: self.menu_bar.entryconfig(LANGUAGES["en"]["help"], label=lang_dict["help"])
        except tk.TclError: pass

        menu_map = {
            self.file_menu: [(0, "open"), (1, "save"), (2, "save_as"), (4, "exit")],
            self.edit_menu: [(0, "copy"), (1, "cut"), (2, "paste"), (3, "select_all"), (5, "clear_all")],
            self.lang_menu: [(0, "english"), (1, "arabic")],
            self.help_menu: [(0, "about")]
        }
        for menu, items in menu_map.items():
            for index, key in items:
                try: menu.entryconfig(index, label=lang_dict[key])
                except (tk.TclError, KeyError, IndexError) as e: print(f"Warn: Menu update failed for {key}: {e}")


        # --- Update Labels & Buttons ---
        self.lbl_search.config(text=lang_dict["search_for"])
        self.lbl_replace.config(text=lang_dict["replace_with"])
        self.lbl_before.config(text=lang_dict["before"])
        self.lbl_after.config(text=lang_dict["after"])
        self.btn_perform_replace.config(text=lang_dict["perform_replace"])
        self.btn_clean_inputs.config(text=lang_dict["clean_inputs"])

        # Update search pane labels/buttons safely
        if hasattr(self, 'search_before_lbl'): self.search_before_lbl.config(text=lang_dict["search_in_pane"])
        if hasattr(self, 'search_before_btn'): self.search_before_btn.config(text=lang_dict["find_next"])
        if hasattr(self, 'search_after_lbl'): self.search_after_lbl.config(text=lang_dict["search_in_pane"])
        if hasattr(self, 'search_after_btn'): self.search_after_btn.config(text=lang_dict["find_next"])

        # --- Update Text Area & Entry Font & Alignment ---
        text_widgets = [self.txt_search, self.txt_replace, self.txt_before, self.txt_after]
        entry_widgets = []
        if hasattr(self, 'search_before_entry'): entry_widgets.append(self.search_before_entry)
        if hasattr(self, 'search_after_entry'): entry_widgets.append(self.search_after_entry)

        for ctrl in text_widgets + entry_widgets:
            try:
                ctrl.config(font=font_tuple)
                if isinstance(ctrl, (scrolledtext.ScrolledText, tk.Text)):
                     # Need to handle potential TclError if widget is destroyed during lang change
                     try:
                        self._apply_text_alignment(ctrl, text_align)
                     except tk.TclError: pass # Ignore if widget gone
                elif isinstance(ctrl, ttk.Entry):
                     ctrl.config(justify=text_align)
            except tk.TclError as e:
                 print(f"Error configuring control font/alignment during language change: {e}")

        # --- Update Widget Layout/Direction (RTL/LTR) ---
        # (Keep the existing RTL/LTR grid switching logic as it was)
        if is_rtl:
            self.replace_frame.grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(0, 5))
            self.search_frame.grid(row=0, column=1, rowspan=2, sticky=NSEW, padx=(5, 0))
            self.after_frame.grid(row=0, column=0, rowspan=4, sticky=NSEW, padx=(0, 5))
            self.before_frame.grid(row=0, column=1, rowspan=4, sticky=NSEW, padx=(5, 0))
            self.lbl_search.grid(sticky='ne')
            self.lbl_replace.grid(sticky='ne')
            self.lbl_before.grid(sticky='ne')
            self.lbl_after.grid(sticky='ne')
            if hasattr(self, 'search_before_frame'):
                self.search_before_lbl.grid(row=0, column=2, padx=(5, 0), sticky=E)
                self.search_before_entry.grid(row=0, column=1, padx=5, sticky=EW)
                self.search_before_btn.grid(row=0, column=0, padx=(0, 5), sticky=W)
            if hasattr(self, 'search_after_frame'):
                self.search_after_lbl.grid(row=0, column=2, padx=(5, 0), sticky=E)
                self.search_after_entry.grid(row=0, column=1, padx=5, sticky=EW)
                self.search_after_btn.grid(row=0, column=0, padx=(0, 5), sticky=W)
            self.status_bar.config(anchor=E)
        else: # LTR
            self.search_frame.grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(0, 5))
            self.replace_frame.grid(row=0, column=1, rowspan=2, sticky=NSEW, padx=(5, 0))
            self.before_frame.grid(row=0, column=0, rowspan=4, sticky=NSEW, padx=(0, 5))
            self.after_frame.grid(row=0, column=1, rowspan=4, sticky=NSEW, padx=(5, 0))
            self.lbl_search.grid(sticky='nw')
            self.lbl_replace.grid(sticky='nw')
            self.lbl_before.grid(sticky='nw')
            self.lbl_after.grid(sticky='nw')
            if hasattr(self, 'search_before_frame'):
                self.search_before_lbl.grid(row=0, column=0, padx=(0, 5), sticky=W)
                self.search_before_entry.grid(row=0, column=1, padx=5, sticky=EW)
                self.search_before_btn.grid(row=0, column=2, padx=(5, 0), sticky=E)
            if hasattr(self, 'search_after_frame'):
                self.search_after_lbl.grid(row=0, column=0, padx=(0, 5), sticky=W)
                self.search_after_entry.grid(row=0, column=1, padx=5, sticky=EW)
                self.search_after_btn.grid(row=0, column=2, padx=(5, 0), sticky=E)
            self.status_bar.config(anchor=W)

        self.status_bar.config(font=font_tuple)


    def on_close(self):
        """Handles the window close event."""
        if self.check_unsaved():
            self.root.destroy()

    # --- Helper Functions for Text Widgets (Unchanged) ---
    def _apply_text_alignment(self, text_widget, text_align):
         """Applies alignment tag to a ScrolledText widget."""
         current_state = text_widget.cget("state")
         is_disabled = current_state == DISABLED
         if is_disabled:
             text_widget.config(state=NORMAL)

         try:
             # Remove previous alignment tags first
             for tag in text_widget.tag_names():
                 if tag.startswith("alignment_"):
                      try: text_widget.tag_remove(tag, "1.0", END)
                      except tk.TclError: pass # Ignore if tag doesn't exist

             # Define and apply the new tag
             align_tag = f"alignment_{text_align}"
             text_widget.tag_configure(align_tag, justify=text_align)
             text_widget.tag_add(align_tag, "1.0", END)
         except tk.TclError as e:
              print(f"TclError applying alignment tag '{align_tag}': {e}")
         except Exception as e:
              print(f"Error applying alignment: {e}")
              traceback.print_exc()
         finally:
              if is_disabled:
                 try: text_widget.config(state=DISABLED)
                 except tk.TclError: pass # Ignore if widget destroyed

    def _update_text_widget(self, text_widget, content):
        """Safely updates the content of a ScrolledText widget."""
        current_state = text_widget.cget("state")
        is_currently_disabled = current_state == DISABLED
        yview_pos = None

        try:
            # Remember scroll only if not disabled (yview fails on disabled)
            if not is_currently_disabled:
                yview_pos = text_widget.yview()

            text_widget.config(state=NORMAL)
            text_widget.delete("1.0", END)
            if content is not None: # Allow inserting empty string
                text_widget.insert("1.0", content)

            # Re-apply Alignment
            text_align = LANGUAGES[self.current_lang]["text_align"]
            self._apply_text_alignment(text_widget, text_align)

            # Restore Scroll Position (or top)
            is_empty = not text_widget.get("1.0", END + "-1c").strip()
            if is_empty:
                 text_widget.yview_moveto(0.0)
            elif yview_pos and len(yview_pos) == 2 and not is_currently_disabled:
                 text_widget.yview_moveto(yview_pos[0]) # Try restoring previous top position
            else:
                 text_widget.yview_moveto(0.0) # Default to top

            # Reset Search Highlight
            text_widget.tag_remove(SEARCH_TAG, "1.0", END)

        except tk.TclError as e:
             print(f"TclError updating text widget: {e}")
        except Exception as e:
             print(f"Error updating text widget: {e}")
             traceback.print_exc()
        finally:
            # Restore original state if it was disabled initially
            if is_currently_disabled:
                try: text_widget.config(state=DISABLED)
                except tk.TclError: pass # Ignore if widget destroyed


    def _clear_text_widget(self, text_widget):
         """Safely clears the content of a ScrolledText widget."""
         current_state = text_widget.cget("state")
         try:
             text_widget.config(state=NORMAL)
             text_widget.delete("1.0", END)
             text_widget.tag_remove(SEARCH_TAG, "1.0", END)
             text_widget.yview_moveto(0.0)
             # Re-apply alignment tag
             text_align = LANGUAGES[self.current_lang]["text_align"]
             self._apply_text_alignment(text_widget, text_align)
         except tk.TclError as e:
             print(f"TclError clearing text widget: {e}")
         except Exception as e:
             print(f"Error clearing text widget: {e}")
             traceback.print_exc()
         finally:
             # Restore original state unless it should be left NORMAL (e.g. after reset)
             if current_state == DISABLED:
                 try: text_widget.config(state=DISABLED)
                 except tk.TclError: pass # Ignore if widget destroyed


# --- Main Execution ---
if __name__ == "__main__":
    # root = ttk.Window(themename="superhero")
    root = ttk.Window(themename="flatly")

    app = SearchReplaceApp(root)
    app.mark_unsaved(False) # Set initial title correctly

    # Initial state: 'Before' is editable, 'After' is not.
    app.txt_before.config(state=NORMAL)
    app.txt_after.config(state=DISABLED)

    root.mainloop()
