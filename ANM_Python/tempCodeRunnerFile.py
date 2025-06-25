import os
import json
from customtkinter import *
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image
import elgamal # Assuming elgamal.py is in the same directory or accessible

cwd = os.getcwd()

class ModernCard(CTkFrame):
    def __init__(self, master, title="", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=("#f8f9fa", "#1a1a1a"),
            border_width=1,
            border_color=("#e9ecef", "#333333"),
            corner_radius=15
        )
        if title:
            self.title_label = CTkLabel(self,
                text=title,
                font=("Segoe UI", 18, "bold"),
                text_color=("#2c3e50", "#ecf0f1"),
                anchor="w"
            )
            self.title_label.pack(pady=(15, 10), padx=20, fill="x")

class GradientButton(CTkButton):
    def __init__(self, master, gradient_colors=None, **kwargs):
        if gradient_colors is None:
            gradient_colors = [("#3498db", "#2980b9"), ("#e74c3c", "#c0392b")]
        super().__init__(master, **kwargs)
        self.configure(
            corner_radius=12,
            height=45,
            font=("Segoe UI", 12, "bold"),
            hover_color=gradient_colors[0][1] if len(gradient_colors) > 0 else "#2980b9"
        )

class AnimatedLabel(CTkLabel):
    def __init__(self, master, size="normal", **kwargs):
        font_sizes = {"small": 11, "normal": 13, "large": 15, "title": 18}
        font_size = font_sizes.get(size, 13)
        super().__init__(master, **kwargs)
        self.configure(
            font=("Segoe UI", font_size, "bold" if size == "title" else "normal"),
            text_color=("#34495e", "#bdc3c7")
        )

class ModernEntry(CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            height=40,
            corner_radius=8,
            border_width=2,
            font=("Segoe UI", 12),
            border_color=("#bdc3c7", "#34495e"),
            fg_color=("#ffffff", "#2c3e50"),
            text_color=("#2c3e50", "#ecf0f1")
        )

class ModernTextbox(CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            corner_radius=8,
            border_width=2,
            font=("Consolas", 11),
            border_color=("#bdc3c7", "#34495e"),
            fg_color=("#ffffff", "#2c3e50"),
            text_color=("#2c3e50", "#ecf0f1")
        )

class ModernComboBox(CTkComboBox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            height=40,
            corner_radius=8,
            border_width=2,
            font=("Segoe UI", 12),
            border_color=("#bdc3c7", "#34495e"),
            fg_color=("#ffffff", "#2c3e50"),
            text_color=("#2c3e50", "#ecf0f1"),
            button_color=("#3498db", "#2980b9"),
            button_hover_color=("#2980b9", "#1f4e79")
        )

class BeautifulElGamalApp(CTk):
    def __init__(self):
        super().__init__()
        self.mode, self.theme, self.mode_text = self.get_mode()
        self.key_bit_sizes = [256, 512, 1024, 2048]
        self.vb1_bytes_to_sign = None # Bytes of file/text from signing card before hashing
        self.vb2_bytes_to_verify = None # Bytes of file/text from verification card before hashing
        
        # For comparison in verification
        self.last_signed_doc_bytes_for_verify = None
        self.last_generated_signature_string_for_verify = None

        self.colors = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "accent": "#e74c3c",
            "warning": "#f39c12",
            "dark": "#2c3e50",
            "light": "#ecf0f1",
            "card_bg": ("#ffffff", "#1e1e1e"),
            "text_primary": ("#2c3e50", "#ecf0f1"),
            "text_secondary": ("#7f8c8d", "#95a5a6")
        }
        self.configure_window()
        self.load_icons()
        self.create_ui()
        self.setup_shortcuts()

    def configure_window(self):
        self.title("✨ ElGamal Signature ")
        self.geometry("1400x850")
        self.minsize(1200, 750)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.thoat)

    def load_icons(self):
        self.icons = {}
        icon_files = {
            "mode": ("light.png", "dark.png"), "key": "key.png", "save": "save-file.png",
            "load": "openfile.png", "clean": "clean.png", "open_file": "openfile.png",
            "ky": "ky.png", "forward": "forward.png", "check": "check.png",
            "random_key": "random.png", "input_key": "input.png" # New icons for key gen buttons
        }
        missing_icons = False
        for name, files in icon_files.items():
            try:
                if isinstance(files, tuple): # Dark/Light mode icon
                    light_img = Image.open(os.path.join("data", "images", files[0]))
                    dark_img = Image.open(os.path.join("data", "images", files[1]))
                    self.icons[name] = CTkImage(light_img, dark_img, size=(20, 20))
                else:
                    img_path = os.path.join("data", "images", files)
                    if not os.path.exists(img_path) and name == "random_key": # Fallback for new icons
                         img_path = os.path.join("data", "images", "key.png") # Fallback to key icon
                    if not os.path.exists(img_path) and name == "input_key": # Fallback for new icons
                         img_path = os.path.join("data", "images", "update.png") # Fallback to update (or key)
                         if not os.path.exists(img_path):
                             img_path = os.path.join("data", "images", "key.png")

                    if os.path.exists(img_path):
                        self.icons[name] = CTkImage(Image.open(img_path), size=(20, 20))
                    else:
                        print(f"Warning: Icon file not found: {img_path} for '{name}'")
                        missing_icons = True
                        # Create a placeholder transparent image
                        placeholder_img = Image.new('RGBA', (20, 20), (0,0,0,0))
                        self.icons[name] = CTkImage(placeholder_img, size=(20,20))

            except FileNotFoundError as e:
                print(f"Error loading icon '{name}': {e.filename} not found.")
                missing_icons = True
                placeholder_img = Image.new('RGBA', (20, 20), (0,0,0,0))
                self.icons[name] = CTkImage(placeholder_img, size=(20,20))
            except Exception as e:
                print(f"Generic error loading icon '{name}': {e}")
                missing_icons = True
                placeholder_img = Image.new('RGBA', (20, 20), (0,0,0,0))
                self.icons[name] = CTkImage(placeholder_img, size=(20,20))

        if missing_icons:
            messagebox.showwarning("Lỗi Tải Icon", "Một số file icon không tìm thấy hoặc bị lỗi. Sử dụng icon tạm thời.")


    def create_ui(self):
        header_frame = CTkFrame(self, height=80, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        title_frame = CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=(20, 0))
        CTkLabel(title_frame, text="🔐 Chữ Ký Số ElGamal",
                 font=("Segoe UI", 44, "bold"), text_color=self.colors["primary"]).pack(anchor="w")

        self.theme_btn = GradientButton(header_frame, text=f"🌙 {self.mode_text}", width=150,
                                       gradient_colors=[("#6c5ce7", "#5f3dc4")], command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=2, sticky="e", padx=(0, 20))

        main_frame = CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 10))
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=4)
        main_frame.grid_columnconfigure(2, weight=4)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_key_generation_card(main_frame)
        self.create_signing_card(main_frame)
        self.create_verification_card(main_frame)

    def create_key_generation_card(self, parent):
        key_card = ModernCard(parent, title="🔑 Tạo Khóa") # Title changed back
        key_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        content = CTkFrame(key_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content.grid_columnconfigure(1, weight=1) # Column for entries

        row = 0
        # Key Length Section
        key_length_frame = CTkFrame(content, fg_color="transparent")
        key_length_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10,15))
        key_length_frame.grid_columnconfigure(1, weight=1) # Make combobox expand if needed (though fixed width here)
        AnimatedLabel(key_length_frame, text="Độ dài khóa (bit):", size="normal").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.key_size_combo = ModernComboBox(key_length_frame, values=[str(s) for s in self.key_bit_sizes], state="readonly", width=150)
        self.key_size_combo.grid(row=0, column=1, sticky="w") # Changed sticky to w for balance
        self.key_size_combo.set("512")
        row += 1

        AnimatedLabel(content, text="Tham Số Chung (p, g)", size="large").grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        row += 1
        AnimatedLabel(content, text="Số nguyên tố p =").grid(row=row, column=0, sticky="w", pady=5, padx=(0,10))
        self.entry_p = ModernEntry(content, placeholder_text="Số nguyên tố lớn")
        self.entry_p.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        AnimatedLabel(content, text="Số sinh g =").grid(row=row, column=0, sticky="w", pady=5, padx=(0,10))
        self.entry_g = ModernEntry(content, placeholder_text="Giá trị số sinh")
        self.entry_g.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        AnimatedLabel(content, text="Khóa Bí Mật (x)", size="large").grid(row=row, column=0, columnspan=2, sticky="w", pady=(15, 5))
        row += 1
        AnimatedLabel(content, text="Khóa bí mật x =").grid(row=row, column=0, sticky="w", pady=5, padx=(0,10))
        self.entry_x = ModernEntry(content, placeholder_text="Số nguyên 1 < x < p-1")
        self.entry_x.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        AnimatedLabel(content, text="Khóa Công Khai (y)", size="large").grid(row=row, column=0, columnspan=2, sticky="w", pady=(15, 5))
        row += 1
        AnimatedLabel(content, text="Khóa công khai y =").grid(row=row, column=0, sticky="w", pady=5, padx=(0,10))
        self.entry_y = ModernEntry(content, placeholder_text="Tính từ p, g, x", state="readonly")
        self.entry_y.grid(row=row, column=1, sticky="ew", pady=5)
        row += 1

        # Key Generation Buttons (moved here)
        key_gen_btn_frame = CTkFrame(content, fg_color="transparent")
        key_gen_btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(15, 10))
        key_gen_btn_frame.grid_columnconfigure((0,1), weight=1)
        GradientButton(key_gen_btn_frame, text="✨ Tạo Khóa Từ Đầu Vào", image=self.icons.get("input_key"), # Was Update
                    gradient_colors=[("#3498db", "#2980b9")], command=self.check_and_update_key_params).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        GradientButton(key_gen_btn_frame, text="🎲 Tạo Khóa Ngẫu Nhiên", image=self.icons.get("random_key"), # Was Tạo Mới
                    gradient_colors=[("#2ecc71", "#27ae60")], command=self.generate_random_key).grid(row=0, column=1, padx=5, sticky="ew")
        row += 1

        # Spacer to push action buttons down
        CTkFrame(content, fg_color="transparent").grid(row=row, column=0, columnspan=2, sticky="nsew", pady=(5,0))
        content.grid_rowconfigure(row, weight=1)
        row += 1

        key_action_frame = CTkFrame(content, fg_color="transparent")
        key_action_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        key_action_frame.grid_columnconfigure((0, 1, 2), weight=1)
        GradientButton(key_action_frame, text="💾 Lưu Khóa", image=self.icons.get("save"),
                    gradient_colors=[("#9b59b6", "#8e44ad")], command=self.save_key).grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)
        GradientButton(key_action_frame, text="📂 Tải Khóa", image=self.icons.get("load"),
                    gradient_colors=[("#f39c12", "#e67e22")], command=self.load_key).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        GradientButton(key_action_frame, text="🗑️ Xóa Tất Cả", image=self.icons.get("clean"),
                    gradient_colors=[("#e74c3c", "#c0392b")], command=self.clear_all_data).grid(row=0, column=2, sticky="ew", padx=(5, 0), pady=5)

    def create_signing_card(self, parent):
        sign_card = ModernCard(parent, title="✍️ Ký Tài Liệu")
        sign_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=0)

        content = CTkFrame(sign_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=3)
        content.grid_rowconfigure(5, weight=2)

        doc_header = CTkFrame(content, fg_color="transparent")
        doc_header.grid(row=0, column=0, sticky="ew", pady=(10, 5))
        doc_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(doc_header, text="📄 Tài Liệu Cần Ký", size="large").grid(row=0, column=0, sticky="w")
        GradientButton(doc_header, text="📁 Mở File", width=100, image=self.icons.get("open_file"),
                      gradient_colors=[("#17a2b8", "#138496")], command=self.open_file_to_sign).grid(row=0, column=1, sticky="e")

        self.text_to_sign = ModernTextbox(content)
        self.text_to_sign.grid(row=1, column=0, sticky="nsew", pady=5)
        self.text_to_sign.bind("<KeyRelease>", self._text_to_sign_modified)
        
        k_sign_frame = CTkFrame(content, fg_color="transparent")
        k_sign_frame.grid(row=2, column=0, sticky="ew", pady=(10,5))
        k_sign_frame.grid_columnconfigure(1, weight=1)
        AnimatedLabel(k_sign_frame, text="Số ngẫu nhiên k:", size="normal").grid(row=0, column=0, sticky="w", padx=(0,10))
        self.entry_k_sign = ModernEntry(k_sign_frame, placeholder_text="Để trống để tạo tự động")
        self.entry_k_sign.grid(row=0, column=1, sticky="ew")

        params_frame = CTkFrame(content, fg_color="transparent")
        params_frame.grid(row=3, column=0, sticky="ew", pady=5)
        params_frame.grid_columnconfigure(0, weight=1)
        params_frame.grid_columnconfigure(1, weight=0) 

        AnimatedLabel(params_frame, text="🔢 Thuật Toán Hash:", size="normal").grid(row=0, column=0, sticky="w")
        self.hash_combo = ModernComboBox(params_frame, values=["SHA-256", "SHA-384", "SHA-512", "SHA-1", "MD5"], state="readonly", width=150)
        self.hash_combo.grid(row=0, column=1, sticky="e", padx=(10,0))
        self.hash_combo.set("SHA-256")

        AnimatedLabel(params_frame, text="📋 Định Dạng Chữ Ký:", size="normal").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.format_combo = ModernComboBox(params_frame, values=["Hex", "Base64"], state="readonly", width=150)
        self.format_combo.grid(row=1, column=1, sticky="e", padx=(10,0), pady=(5,0))
        self.format_combo.set("Hex")

        AnimatedLabel(content, text="🔏 Chữ Ký (r;s)", size="large").grid(row=4, column=0, sticky="w", pady=(10, 5)) # Title changed
        self.signature_output = ModernTextbox(content, state="disabled", height=50) # Reduced height for single line
        self.signature_output.grid(row=5, column=0, sticky="nsew", pady=5)

        action_frame = CTkFrame(content, fg_color="transparent")
        action_frame.grid(row=6, column=0, sticky="ew", pady=(10, 0))
        action_frame.grid_columnconfigure((0,1), weight=1)
        GradientButton(action_frame, text="✍️ Ký Tài Liệu", image=self.icons.get("ky"),
                      gradient_colors=[("#2ecc71", "#27ae60")], command=self.sign_document).grid(row=0, column=0, columnspan=2, sticky="ew", pady=2)
        GradientButton(action_frame, text="➡️ Chuyển Dữ Liệu", image=self.icons.get("forward"),
                      gradient_colors=[("#6c5ce7", "#5f3dc4")], command=self.forward_data).grid(row=1, column=0, sticky="ew", padx=(0, 2), pady=2)
        GradientButton(action_frame, text="💾 Lưu Chữ Ký", image=self.icons.get("save"),
                      gradient_colors=[("#fd79a8", "#e84393")], command=self.save_signature).grid(row=1, column=1, sticky="ew", padx=(2, 0), pady=2)

    def create_verification_card(self, parent):
        verify_card = ModernCard(parent, title="🔍 Xác Minh Chữ Ký")
        verify_card.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=0)

        content = CTkFrame(verify_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=3)
        content.grid_rowconfigure(3, weight=2)

        doc_verify_header = CTkFrame(content, fg_color="transparent")
        doc_verify_header.grid(row=0, column=0, sticky="ew", pady=(10, 5))
        doc_verify_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(doc_verify_header, text="📄 Tài Liệu Cần Xác Minh", size="large").grid(row=0, column=0, sticky="w")
        GradientButton(doc_verify_header, text="📁 Mở File", width=100, image=self.icons.get("open_file"),
                      gradient_colors=[("#17a2b8", "#138496")], command=self.open_file_to_verify).grid(row=0, column=1, sticky="e")

        self.text_to_verify = ModernTextbox(content)
        self.text_to_verify.grid(row=1, column=0, sticky="nsew", pady=5)
        self.text_to_verify.bind("<KeyRelease>", self._text_to_verify_modified)

        sig_header = CTkFrame(content, fg_color="transparent")
        sig_header.grid(row=2, column=0, sticky="ew", pady=(10, 5))
        sig_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(sig_header, text="🔏 Chữ Ký Cần Xác Minh (r;s)", size="large").grid(row=0, column=0, sticky="w") # Title changed
        GradientButton(sig_header, text="📁 Tải Chữ Ký", width=120, image=self.icons.get("open_file"),
                      gradient_colors=[("#fd79a8", "#e84393")], command=self.load_signature_file).grid(row=0, column=1, sticky="e")

        self.signature_input = ModernTextbox(content, height=50) # Reduced height
        self.signature_input.grid(row=3, column=0, sticky="nsew", pady=5)

        # Removed Hash and Format combo boxes from verification card
        CTkFrame(content, fg_color="transparent").grid(row=4, column=0, sticky="ew", pady=(10,5)) # Spacer

        GradientButton(content, text="🔍 Xác Minh Chữ Ký", image=self.icons.get("check"),
                      gradient_colors=[("#00b894", "#00a085")], command=self.verify_signature).grid(row=5, column=0, sticky="ew", pady=(10, 0))

    def setup_shortcuts(self):
        shortcuts = {
            "<Control-n>": self.generate_random_key, # N for New Random
            "<Control-i>": self.check_and_update_key_params, # I for Input
            "<Control-s>": self.save_key,
            "<Control-o>": self.load_key,
            "<Control-Delete>": self.clear_all_data,
            "<Control-Return>": self.sign_document,
            "<Control-t>": self.toggle_theme,
            "<Control-f>": self.forward_data,
            "<Control-v>": self.verify_signature,
        }
        for key, func in shortcuts.items():
            self.bind(key, lambda e, f=func: f())

    def get_mode(self):
        try:
            os.makedirs("data/mode", exist_ok=True)
            with open("data/mode/mode.json", "r") as f:
                data = json.load(f)
            mode = data.get("mode", "dark")
            theme = data.get("theme", "blue") # Default theme
            mode_text = "Chế Độ Sáng" if mode == "dark" else "Chế Độ Tối"
        except (FileNotFoundError, json.JSONDecodeError):
            mode, theme, mode_text = "dark", "blue", "Chế Độ Sáng"
            self.save_theme_config(mode, theme) # Save defaults if file problematic
        set_appearance_mode(mode)
        try:
            theme_path = os.path.join(cwd, "data", "themes", f"{theme}.json")
            if os.path.exists(theme_path):
                 set_default_color_theme(theme_path)
            else:
                 print(f"Theme file not found: {theme_path}, using default.")
                 set_default_color_theme("blue") # CustomTkinter's default
        except Exception as e:
            print(f"Error setting theme {theme}: {e}, using default.")
            set_default_color_theme("blue")
        return mode, theme, mode_text

    def save_theme_config(self, mode, theme):
        try:
            os.makedirs(os.path.join(cwd,"data","mode"), exist_ok=True)
            with open(os.path.join(cwd,"data","mode","mode.json"), "w") as f:
                json.dump({"mode": mode, "theme": theme}, f, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi Ghi Theme", f"Không thể ghi cấu hình theme: {e}")

    def toggle_theme(self):
        new_mode = "light" if self.mode == "dark" else "dark"
        self.mode = new_mode
        self.mode_text = "Chế Độ Tối" if new_mode == "light" else "Chế Độ Sáng"
        set_appearance_mode(new_mode)
        self.theme_btn.configure(text=f"🌙 {self.mode_text}")
        self.save_theme_config(new_mode, self.theme)

    def show_working_dialog(self, message):
        dialog = CTkToplevel(self)
        dialog.geometry("400x150")
        dialog.title("Đang Xử Lý...")
        dialog.transient(self)
        dialog.grab_set()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"400x150+{x}+{y}")
        CTkLabel(dialog, text="⚡ Đang xử lý", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
        CTkLabel(dialog, text=message, font=("Segoe UI", 12)).pack(pady=(0, 20))
        progress = CTkProgressBar(dialog, width=300, mode="indeterminate") # indeterminate mode
        progress.pack(pady=10)
        progress.start()
        self.update_idletasks()
        return dialog

    def _text_to_sign_modified(self, event=None):
        self.vb1_bytes_to_sign = None # Mark that file bytes are stale if text is edited

    def _text_to_verify_modified(self, event=None):
        self.vb2_bytes_to_verify = None # Mark that file bytes are stale if text is edited

    def _set_entry_text(self, entry_widget, text, read_only=False):
        current_state = entry_widget.cget("state")
        entry_widget.configure(state="normal")
        entry_widget.delete("0", END)
        entry_widget.insert("0", str(text))
        if read_only:
            entry_widget.configure(state="readonly")
        elif current_state != "readonly": # Restore original state if it was normal
             entry_widget.configure(state=current_state)


    def _set_textbox_text(self, textbox_widget, text, disabled=True):
        textbox_widget.configure(state="normal")
        textbox_widget.delete("1.0", END)
        textbox_widget.insert("1.0", text)
        if disabled:
            textbox_widget.configure(state="disabled")

    def clear_key_entries(self):
        self.entry_p.delete("0", END)
        self.entry_g.delete("0", END)
        self.entry_x.delete("0", END)
        self._set_entry_text(self.entry_y, "", read_only=True)
        if hasattr(self, 'entry_k_sign'):
            self.entry_k_sign.delete("0", END)

    def clear_all_data(self):
        if messagebox.askyesno("Xác Nhận", "🗑️ Bạn có muốn xóa toàn bộ dữ liệu trên tất cả các thẻ không?"):
            self.clear_key_entries()
            self._set_textbox_text(self.text_to_sign, "", disabled=False)
            self._set_textbox_text(self.text_to_verify, "", disabled=False)
            self._set_textbox_text(self.signature_output, "", disabled=True)
            self.signature_input.delete("1.0", END)
            
            self.vb1_bytes_to_sign = None
            self.vb2_bytes_to_verify = None
            self.last_signed_doc_bytes_for_verify = None
            self.last_generated_signature_string_for_verify = None
            
            self.hash_combo.set("SHA-256")
            self.format_combo.set("Hex")
            messagebox.showinfo("Đã Xóa", "Toàn bộ dữ liệu đã được xóa.")


    def generate_random_key(self): # Was "Tạo Mới", now "Tạo Khóa Ngẫu Nhiên"
        try:
            bits = int(self.key_size_combo.get())
            msg = f"Đang tạo cặp khóa ElGamal {bits}-bit ngẫu nhiên...\nVui lòng chờ."
            if bits >= 1024: msg += "\nQuá trình này có thể mất một chút thời gian."
            dialog = self.show_working_dialog(msg)
            p, g, x, y = elgamal.cre_key(bits)
            dialog.destroy() # Close dialog before clearing/setting entries

            self.clear_key_entries()
            self._set_entry_text(self.entry_p, p)
            self._set_entry_text(self.entry_g, g)
            self._set_entry_text(self.entry_x, x)
            self._set_entry_text(self.entry_y, y, read_only=True)
            if hasattr(self, 'entry_k_sign'): self.entry_k_sign.delete("0", END)
            
            messagebox.showinfo("Thành Công", "✅ Cặp khóa (p,g,x,y) ngẫu nhiên đã được tạo!")
        except Exception as e:
            if 'dialog' in locals() and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Tạo Khóa Ngẫu Nhiên", f"Không thể tạo khóa: {e}")

    def check_and_update_key_params(self): # Was "Cập Nhật", now "Tạo Khóa Từ Đầu Vào"
        try:
            p_str, g_str, x_str = self.entry_p.get(), self.entry_g.get(), self.entry_x.get()
            if not all([p_str, g_str, x_str]):
                messagebox.showerror("Thiếu Thông Tin", "Vui lòng nhập đầy đủ p, g, và x để tạo khóa.")
                return

            p = int(p_str)
            g = int(g_str)
            x = int(x_str)

            if not elgamal.check_prime(p):
                messagebox.showerror("Lỗi p", f"Số p ({p}) phải là số nguyên tố.")
                return
            if not (1 < g < p): # g can be p-1 in some definitions, but usually 1 < g < p
                messagebox.showerror("Lỗi g", f"Số g ({g}) phải nằm trong khoảng (1, {p-1}).")
                return
            if not (1 < x < p - 1):
                messagebox.showerror("Lỗi x", f"Số x ({x}) phải nằm trong khoảng (1, {p-1}).")
                return

            dialog = self.show_working_dialog("Đang tính toán khóa công khai y từ đầu vào...")
            y_calc = elgamal.pow_mod(g, x, p)
            dialog.destroy()
            self._set_entry_text(self.entry_y, str(y_calc), read_only=True)
            messagebox.showinfo("Thành Công", "Đã tạo khóa (p,g,x,y) từ đầu vào thành công.")
        except ValueError:
            messagebox.showerror("Lỗi Đầu Vào", "Các giá trị p, g, x phải là số nguyên.")
        except Exception as e:
            if 'dialog' in locals() and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Tạo Khóa", f"Đã xảy ra lỗi: {e}")
    
    def get_key_params_for_action(self, action_type="signing"):
        try:
            p_s, g_s, x_s, y_s = self.entry_p.get(), self.entry_g.get(), self.entry_x.get(), self.entry_y.get()

            if not p_s or not g_s:
                messagebox.showerror("Lỗi Khóa", "Giá trị p và g không được để trống.")
                return None
            
            p = int(p_s); g = int(g_s)

            if not elgamal.check_prime(p):
                messagebox.showerror("Lỗi p", f"Số p ({p}) phải là số nguyên tố."); return None
            if not (1 < g < p):
                messagebox.showerror("Lỗi g", f"Số g ({g}) phải trong (1, {p-1})."); return None

            x = None
            if action_type in ["signing", "saving"]:
                if not x_s: messagebox.showerror("Lỗi Khóa", "Giá trị x (khóa bí mật) trống."); return None
                x = int(x_s)
                if not (1 < x < p - 1): messagebox.showerror("Lỗi x", f"Số x ({x}) phải trong (1, {p-1})."); return None
            
            y = None
            expected_y_val = elgamal.pow_mod(g, x, p) if x is not None else None
            
            if not y_s: # y is empty
                if expected_y_val is not None: # Can calculate y
                    if action_type != "verification": # For signing/saving, auto-calculate if user agrees
                        if messagebox.askyesno("Thiếu y", f"Tính y từ (p,g,x)? y={expected_y_val}", icon=messagebox.WARNING):
                            self._set_entry_text(self.entry_y, str(expected_y_val), read_only=True)
                            y = expected_y_val
                        else: messagebox.showerror("Lỗi Khóa", "y là bắt buộc."); return None
                    else: # For verification, y is critical and must be present or calculated
                         messagebox.showerror("Lỗi Khóa", "y trống. Cần y để xác minh."); return None
                elif action_type == "verification": # y empty, cannot calculate (x unknown)
                    messagebox.showerror("Lỗi Khóa", "y trống và không thể tính. Cần y để xác minh."); return None
            else: # y_s is present
                y = int(y_s)
                if not (0 < y < p): messagebox.showerror("Lỗi y", f"Số y ({y}) phải trong (0, {p})."); return None
                if expected_y_val is not None and y != expected_y_val:
                    if messagebox.askyesno("Không Khớp y", f"y hiện tại ({y}) khác y tính từ (p,g,x) ({expected_y_val}). Cập nhật?", icon=messagebox.WARNING):
                        self._set_entry_text(self.entry_y, str(expected_y_val), read_only=True); y = expected_y_val
                    else: return None
            
            if action_type == "signing": return p, g, x # y not strictly needed if x is known for sign
            elif action_type == "verification":
                if y is None: messagebox.showerror("Lỗi Khóa", "Không có y để xác minh."); return None
                return p, g, y
            elif action_type == "saving":
                if x is None or y is None: messagebox.showerror("Lỗi Khóa", "Thiếu p,g,x,y để lưu."); return None
                return p, g, x, y
        except ValueError: messagebox.showerror("Lỗi Giá Trị", "p,g,x,y phải là số nguyên."); return None
        except Exception as e: messagebox.showerror("Lỗi Kiểm Tra Khóa", f"Lỗi: {e}"); return None
        return None

    def save_key(self):
        key_params = self.get_key_params_for_action(action_type="saving")
        if not key_params:
            messagebox.showerror("Lỗi Lưu Khóa", "Không thể lưu. Kiểm tra (p,g,x,y).")
            return
        p, g, x, y = key_params
        
        bits_str = self.key_size_combo.get()
        fp = filedialog.asksaveasfilename(
            initialdir=cwd, title="Lưu Khóa ElGamal",
            filetypes=(("JSON files", "*.json"),("Text files", "*.txt"),),
            defaultextension=".json"
        )
        if not fp: return
        
        key_data = {"description": "Khóa ElGamal", "bit_length": bits_str, "p": p, "g": g, "x_private_key": x, "y_public_key": y}
        try:
            with open(fp, "w", encoding="utf-8") as f:
                if fp.endswith(".txt"):
                    f.write(f"--- Khóa ElGamal ---\nĐộ dài khóa: {bits_str}\n\np: {p}\ng: {g}\ny (khóa công khai): {y}\nx (khóa bí mật): {x}\n")
                else: json.dump(key_data, f, indent=4)
            messagebox.showinfo("Thành Công", f"Đã lưu khóa vào:\n{fp}")
        except Exception as e: messagebox.showerror("Lỗi Lưu Khóa", f"Không thể lưu file:\n{e}")

    def load_key(self):
        fp = filedialog.askopenfilename(initialdir=cwd, title="Tải Khóa ElGamal",
            filetypes=(("JSON files", "*.json"),("Text files", "*.txt"), ("All files", "*.*")))
        if not fp: return
        
        kd = {}
        try:
            with open(fp, "r", encoding="utf-8") as f:
                if fp.endswith(".json"):
                    data = json.load(f)
                    kd = {k: data.get(k_map) for k, k_map in 
                          [('p','p'), ('g','g'), ('x','x_private_key'), ('y','y_public_key'), ('bit_length','bit_length')]}
                else: # TXT parsing
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if ":" in line:
                            key_part, value_part = line.split(":", 1)
                            key_part = key_part.strip().lower(); value_part = value_part.strip()
                            if key_part == "p": kd['p'] = int(value_part)
                            elif key_part == "g": kd['g'] = int(value_part)
                            elif key_part == "x (khóa bí mật)": kd['x'] = int(value_part)
                            elif key_part == "y (khóa công khai)": kd['y'] = int(value_part)
                            elif key_part == "độ dài khóa": kd['bit_length'] = value_part
            
            self.clear_key_entries()
            self._set_entry_text(self.entry_p, kd.get("p", ""))
            self._set_entry_text(self.entry_g, kd.get("g", ""))
            self._set_entry_text(self.entry_x, kd.get("x", ""))
            self._set_entry_text(self.entry_y, kd.get("y", ""), read_only=True)
            if hasattr(self, 'entry_k_sign'): self.entry_k_sign.delete("0", END)

            bits_val = kd.get("bit_length", self.key_bit_sizes[1])
            if str(bits_val) in [str(s) for s in self.key_bit_sizes]: self.key_size_combo.set(str(bits_val))
            else: self.key_size_combo.set(str(self.key_bit_sizes[1]))
            
            messagebox.showinfo("Thành Công", f"Đã tải khóa từ:\n{fp}")
        except Exception as e: messagebox.showerror("Lỗi Tải Khóa", f"Lỗi đọc file ({fp}) hoặc định dạng không đúng:\n{e}")

    def open_file_to_sign(self):
        fp = filedialog.askopenfilename(initialdir=cwd, title="Mở File Để Ký",
            filetypes=(("All", "*.*"), ("Text", "*.txt"),("Word", "*.docx"), ("PDF", "*.pdf"))).strip()
        if not fp: return
        try:
            self.vb1_bytes_to_sign = elgamal.read_file_bytes(fp)
            display_text = elgamal.get_displayable_text_from_file(fp)
            self._set_textbox_text(self.text_to_sign, display_text, disabled=False)
            messagebox.showinfo("Thành Công", f"Đã tải file để ký: {os.path.basename(fp)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đọc file '{os.path.basename(fp)}':\n{e}")
            self.vb1_bytes_to_sign = None
            self._set_textbox_text(self.text_to_sign, f"[Lỗi đọc file: {os.path.basename(fp)}]", disabled=False)

    def open_file_to_verify(self):
        fp = filedialog.askopenfilename(initialdir=cwd, title="Mở File Để Xác Minh",
            filetypes=(("All", "*.*"),("Text", "*.txt"),("Word", "*.docx"),("PDF", "*.pdf"))).strip()
        if not fp: return
        try:
            self.vb2_bytes_to_verify = elgamal.read_file_bytes(fp)
            display_text = elgamal.get_displayable_text_from_file(fp)
            self._set_textbox_text(self.text_to_verify, display_text, disabled=False)
            messagebox.showinfo("Thành Công", f"Đã tải file để xác minh: {os.path.basename(fp)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đọc file '{os.path.basename(fp)}':\n{e}")
            self.vb2_bytes_to_verify = None
            self._set_textbox_text(self.text_to_verify, f"[Lỗi đọc file: {os.path.basename(fp)}]", disabled=False)

    def load_signature_file(self):
        fp = filedialog.askopenfilename(initialdir=cwd, title="Mở File Chữ Ký",
            filetypes=(("Text or Signature", "*.txt;*.sig"), ("All", "*.*"))).strip()
        if not fp: return
        self.signature_input.delete("1.0", END)
        try:
            with open(fp, "r", encoding="utf-8") as f: data = f.read()
            self.signature_input.insert("1.0", data.strip()) # Strip to ensure single line if possible
            messagebox.showinfo("Thành Công", f"Đã tải chữ ký từ: {os.path.basename(fp)}")
        except Exception as e: messagebox.showerror("Lỗi", f"Không thể đọc file chữ ký:\n{e}")

    def sign_document(self):
        key_params = self.get_key_params_for_action(action_type="signing")
        if not key_params: messagebox.showerror("Lỗi Khóa", "Không thể ký. Kiểm tra (p,g,x)."); return
        p, g, x = key_params

        k_for_signing_str = self.entry_k_sign.get().strip()
        k_for_signing = None
        dialog = None
        try:
            if k_for_signing_str:
                k_for_signing = int(k_for_signing_str)
                if not (0 < k_for_signing < p - 1 and elgamal.find_gcd(k_for_signing, p - 1) == 1):
                    messagebox.showerror("Lỗi k", f"k ({k_for_signing}) không hợp lệ. Phải (0, {p-1}) & gcd(k, {p-1})=1.")
                    return
            else: # Generate k
                dialog_k_gen = self.show_working_dialog("Đang tạo số ngẫu nhiên k...")
                k_for_signing = elgamal.gen_k_for_signature(p)
                self._set_entry_text(self.entry_k_sign, str(k_for_signing))
                dialog_k_gen.destroy()
            
            mode_hash = self.hash_combo.get()
            format_type = self.format_combo.get()
            
            current_doc_bytes_to_sign = None
            if self.vb1_bytes_to_sign is not None: # File was loaded
                current_doc_bytes_to_sign = self.vb1_bytes_to_sign
            else: # Text input
                text_to_sign_str = self.text_to_sign.get("1.0", END).strip()
                if not text_to_sign_str: messagebox.showwarning("Thiếu Dữ Liệu", "Nội dung ký trống!"); return
                current_doc_bytes_to_sign = text_to_sign_str.encode('utf-8')
            
            if current_doc_bytes_to_sign is None: messagebox.showerror("Lỗi", "Không có dữ liệu để ký."); return

            dialog = self.show_working_dialog("Đang tạo chữ ký...")
            r_val, s_val = elgamal.create_sign(current_doc_bytes_to_sign, mode_hash, p, g, x, k_for_signing)
            
            generated_signature_str = elgamal.encode_signature(r_val, s_val, format_type)
            self._set_textbox_text(self.signature_output, generated_signature_str) # Display single line
            
            # Store for verification comparison
            self.last_signed_doc_bytes_for_verify = current_doc_bytes_to_sign
            self.last_generated_signature_string_for_verify = generated_signature_str
            
            if dialog and dialog.winfo_exists(): dialog.destroy()
            messagebox.showinfo("Thành Công", f"✅ Chữ ký đã được tạo (định dạng: {format_type})!")

        except ValueError as ve:
            if 'dialog_k_gen' in locals() and dialog_k_gen.winfo_exists(): dialog_k_gen.destroy()
            if dialog and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Tạo Chữ Ký", f"Lỗi: {ve}\nNếu s=0, thử lại (k mới nếu trống, hoặc nhập k khác).")
        except Exception as e:
            if 'dialog_k_gen' in locals() and dialog_k_gen.winfo_exists(): dialog_k_gen.destroy()
            if dialog and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Tạo Chữ Ký", f"Lỗi không mong muốn: {e}")


    def forward_data(self):
        vb_display = self.text_to_sign.get("1.0", END).strip()
        self.signature_output.configure(state="normal")
        ck = self.signature_output.get("1.0", END).strip()
        self.signature_output.configure(state="disabled")

        if not vb_display and not ck and self.vb1_bytes_to_sign is None and self.last_signed_doc_bytes_for_verify is None:
            messagebox.showwarning("Lỗi Chuyển Tiếp", "Không có dữ liệu để chuyển tiếp!")
            return

        # Forward displayed text from signing card to verification card
        self._set_textbox_text(self.text_to_verify, vb_display if vb_display else "", disabled=False)
        # Forward generated signature string from signing card to verification card
        self.signature_input.delete("1.0", END)
        if ck: self.signature_input.insert("1.0", ck)
        
        # Crucially, also forward the actual bytes and signature string used for the last signing operation
        # This allows the verification card to compare against these "originals"
        if self.vb1_bytes_to_sign is not None: # If last sign was from file
            self.vb2_bytes_to_verify = self.vb1_bytes_to_sign
        elif vb_display: # If last sign was from text
            self.vb2_bytes_to_verify = vb_display.encode('utf-8')
        else: # No document was actively on sign card, clear verify file bytes
            self.vb2_bytes_to_verify = None

        # The actual self.last_signed_doc_bytes_for_verify and self.last_generated_signature_string_for_verify
        # are already set during sign_document and will be used by verify_signature.
        
        messagebox.showinfo("Thành Công", "✅ Dữ liệu (văn bản, chữ ký) đã được chuyển sang thẻ Xác Minh!")


    def save_signature(self):
        self.signature_output.configure(state="normal")
        data = self.signature_output.get("1.0", END).strip()
        self.signature_output.configure(state="disabled")
        if not data: messagebox.showwarning("Lỗi Lưu", "Chưa có chữ ký để lưu!"); return
        
        format_type = self.format_combo.get()
        ext = ".txt"
        filetypes_list = (("Tất cả file", "*.*"),) # Default
        if format_type.lower() == "hex":
            filetypes_list = (("Chữ ký Hex", "*.txt"), ("Tất cả file", "*.*"))
            ext = ".txt"
        elif format_type.lower() == "base64":
            filetypes_list = (("Chữ ký Base64", "*.sig"),("Text files", "*.txt"), ("Tất cả file", "*.*"))
            ext = ".sig"

        fp = filedialog.asksaveasfilename(initialdir=cwd, title="Lưu File Chữ Ký",
            filetypes=filetypes_list, defaultextension=ext)
        if fp:
            try:
                with open(fp, "w", encoding="utf-8") as f: f.write(data)
                messagebox.showinfo("Thành Công", f"Đã lưu chữ ký!\n{fp}")
            except Exception as e: messagebox.showerror("Lỗi Lưu File", f"Không thể lưu:\n{e}")

    def verify_signature(self):
        key_params = self.get_key_params_for_action(action_type="verification")
        if not key_params: messagebox.showerror("Lỗi Khóa", "Không thể xác minh. Kiểm tra (p,g,y)."); return
        p_val, g_val, y_val = key_params

        # Use hash and format from SIGNING card for verification logic as per new requirement
        hash_algo_from_signing_card = self.hash_combo.get()
        format_type_from_signing_card = self.format_combo.get()
        
        current_sig_str_on_verify_card = self.signature_input.get("1.0", END).strip()
        
        current_doc_bytes_on_verify_card = None
        if self.vb2_bytes_to_verify is not None: # File was loaded/forwarded to verify card
            current_doc_bytes_on_verify_card = self.vb2_bytes_to_verify
        else: # Text input on verify card
            text_to_verify_str = self.text_to_verify.get("1.0", END).strip()
            if not text_to_verify_str: messagebox.showwarning("Thiếu Dữ Liệu", "Nội dung xác minh trống!"); return
            current_doc_bytes_on_verify_card = text_to_verify_str.encode('utf-8')
        
        if not current_sig_str_on_verify_card: messagebox.showwarning("Thiếu Chữ Ký", "Chữ ký xác minh trống!"); return
        if current_doc_bytes_on_verify_card is None: messagebox.showerror("Lỗi", "Không có dữ liệu để xác minh."); return

        dialog = None
        try:
            dialog = self.show_working_dialog("Đang kiểm tra chữ ký...")
            
            # 1. Cryptographic check of current items on verification card
            crypto_status = elgamal.verify_sign(
                current_doc_bytes_on_verify_card, 
                hash_algo_from_signing_card, 
                current_sig_str_on_verify_card, 
                format_type_from_signing_card, 
                p_val, g_val, y_val
            )
            crypto_valid_for_current_items = (crypto_status == elgamal.VerificationStatus.VALID)
            
            # 2. Comparison with last signed items (if available)
            # These 'last_..._for_verify' are set when 'sign_document' runs or 'forward_data' brings them over.
            doc_matches_last_signed = (self.last_signed_doc_bytes_for_verify is not None and \
                                       self.last_signed_doc_bytes_for_verify == current_doc_bytes_on_verify_card)
            
            sig_str_matches_last_generated = (self.last_generated_signature_string_for_verify is not None and \
                                              self.last_generated_signature_string_for_verify == current_sig_str_on_verify_card)

            if dialog and dialog.winfo_exists(): dialog.destroy()
            
            # Determine final message based on comparisons
            if crypto_valid_for_current_items:
                if doc_matches_last_signed and sig_str_matches_last_generated:
                    messagebox.showinfo("Kết Quả Xác Minh", "✅ Chữ ký hợp lệ! (Khớp với văn bản và chữ ký đã tạo gần nhất)")
                elif doc_matches_last_signed and not sig_str_matches_last_generated:
                    messagebox.showwarning("Kết Quả Xác Minh", "⚠️ Chữ ký hợp lệ cho văn bản gốc, nhưng chuỗi chữ ký khác với lần tạo gần nhất (vẫn giải mã đúng r,s).")
                elif not doc_matches_last_signed: # Crypto is valid for current doc, but current doc != last signed doc
                    messagebox.showwarning("Kết Quả Xác Minh", "⚠️ Chữ ký hợp lệ cho văn bản HIỆN TẠI, nhưng văn bản này khác với văn bản gốc đã được ký (nếu có).")
                else: # Should not happen if logic above is correct. Fallback.
                     messagebox.showinfo("Kết Quả Xác Minh", "✅ Chữ ký hợp lệ về mặt toán học cho văn bản và chữ ký hiện tại.")
            else: # Crypto is NOT valid for current items
                error_reason = crypto_status.name # e.g. INVALID_R_RANGE, CRYPTO_MISMATCH
                if doc_matches_last_signed and sig_str_matches_last_generated:
                    messagebox.showerror("Kết Quả Xác Minh", f"❌ Chữ ký KHÔNG hợp lệ! (Lỗi toán học: {error_reason})\nDù văn bản và chuỗi chữ ký khớp lần tạo gần nhất.")
                elif doc_matches_last_signed and not sig_str_matches_last_generated:
                    messagebox.showerror("Kết Quả Xác Minh", f"❌ Chữ ký bị thay đổi và KHÔNG hợp lệ! (Lỗi toán học: {error_reason})")
                elif not doc_matches_last_signed and sig_str_matches_last_generated:
                    messagebox.showerror("Kết Quả Xác Minh", f"❌ Văn bản bị thay đổi! Chữ ký gốc (nếu đây là nó) KHÔNG hợp lệ cho văn bản này. (Lỗi toán học: {error_reason})")
                else: # Both doc and sig string are different from last signed, and crypto fails for current items
                    messagebox.showerror("Kết Quả Xác Minh", f"❌ Văn bản và chữ ký có thể đã bị thay đổi. Chữ ký hiện tại KHÔNG hợp lệ! (Lỗi toán học: {error_reason})")

        except ValueError as e: # Catch potential errors from elgamal.verify_sign if not handled by VerificationStatus
            if dialog and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Kiểm Tra", f"Lỗi trong quá trình kiểm tra: {e}")
        except Exception as e:
            if dialog and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Kiểm Tra", f"Lỗi không mong muốn: {e}")


    def thoat(self):
        if messagebox.askyesno("Thông Báo", "Bạn có muốn thoát không?"):
            self.quit()

if __name__ == "__main__":
    app = BeautifulElGamalApp()
    try:
        icon_path = os.path.join(cwd, "data", "images", "icon.ico")
        if os.path.exists(icon_path): app.iconbitmap(icon_path)
        else: print(f"Không tìm thấy file icon.ico tại: {icon_path}")
    except Exception as e: print(f"Không thể tải icon.ico: {e}")
    app.mainloop()