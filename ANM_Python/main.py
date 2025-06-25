import os
import json
from customtkinter import *
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image
import elgamal 

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
        self.vb1_bytes_to_sign = None
        self.vb2_bytes_to_verify = None
        self.original_forwarded_text_for_verify = None 
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
            "random_key": "random.png", "input_key": "input.png"
        }
        missing_icons = False
        for name, files in icon_files.items():
            try:
                if isinstance(files, tuple):
                    light_img = Image.open(os.path.join("data", "images", files[0]))
                    dark_img = Image.open(os.path.join("data", "images", files[1]))
                    self.icons[name] = CTkImage(light_img, dark_img, size=(20, 20))
                else:
                    img_path = os.path.join("data", "images", files)
                    if not os.path.exists(img_path) and name == "random_key":
                        img_path = os.path.join("data", "images", "key.png")
                    if not os.path.exists(img_path) and name == "input_key":
                        img_path = os.path.join("data", "images", "update.png")
                        if not os.path.exists(img_path):
                            img_path = os.path.join("data", "images", "key.png")
                    if os.path.exists(img_path):
                        self.icons[name] = CTkImage(Image.open(img_path), size=(20, 20))
                    else:
                        print(f"Warning: Icon file not found: {img_path} for '{name}'")
                        missing_icons = True
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
        key_card = ModernCard(parent, title="🔑 Tạo Khóa")
        key_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        content = CTkFrame(key_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=3) 
        content.grid_rowconfigure(2, weight=1)
        content.grid_rowconfigure(3, weight=1)
        content.grid_rowconfigure(4, weight=0)
        content.grid_rowconfigure(5, weight=0) 

        row = 0
        key_length_frame = CTkFrame(content, fg_color="transparent")
        key_length_frame.grid(row=row, column=0, sticky="ew", pady=(10, 5))
        key_length_frame.grid_columnconfigure(1, weight=1)
        AnimatedLabel(key_length_frame, text="Độ dài khóa (bit):", size="normal").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.key_size_combo = ModernComboBox(key_length_frame, values=[str(s) for s in self.key_bit_sizes], state="readonly", width=150)
        self.key_size_combo.grid(row=0, column=1, sticky="ew")
        self.key_size_combo.set("512")
        row += 1

        public_key_frame = CTkFrame(content, fg_color=("#f1f3f5", "#2c2c2c"), corner_radius=10)
        public_key_frame.grid(row=row, column=0, sticky="nsew", pady=(5, 5))
        public_key_frame.grid_columnconfigure(1, weight=1)
        AnimatedLabel(public_key_frame, text="🔓 Khóa Công Khai (p, g, y)", size="large").grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))
        
        AnimatedLabel(public_key_frame, text="Số nguyên tố p =").grid(row=1, column=0, sticky="w", pady=5, padx=(15, 10))
        self.entry_p = ModernEntry(public_key_frame, placeholder_text="Số nguyên tố lớn")
        self.entry_p.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 15))
        
        AnimatedLabel(public_key_frame, text="Số sinh g =").grid(row=2, column=0, sticky="w", pady=5, padx=(15, 10))
        self.entry_g = ModernEntry(public_key_frame, placeholder_text="Giá trị số sinh")
        self.entry_g.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 15))
        
        AnimatedLabel(public_key_frame, text="Khóa công khai y =").grid(row=3, column=0, sticky="w", pady=5, padx=(15, 10))
        self.entry_y = ModernEntry(public_key_frame, placeholder_text="Tính từ p, g, x", state="readonly")
        self.entry_y.grid(row=3, column=1, sticky="ew", pady=(5, 10), padx=(0, 15))
        row += 1

        private_key_frame = CTkFrame(content, fg_color=("#f1f3f5", "#2c2c2c"), corner_radius=10)
        private_key_frame.grid(row=row, column=0, sticky="nsew", pady=(5, 5))
        private_key_frame.grid_columnconfigure(1, weight=1)
        AnimatedLabel(private_key_frame, text="🔒 Khóa Bí Mật (x)", size="large").grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))
        
        AnimatedLabel(private_key_frame, text="Khóa bí mật x =").grid(row=1, column=0, sticky="w", pady=5, padx=(15, 27))
        self.entry_x = ModernEntry(private_key_frame, placeholder_text="Số nguyên 1 < x < p-1")
        self.entry_x.grid(row=1, column=1, sticky="ew", pady=(5, 10), padx=(0, 15))
        row += 1

        k_frame = CTkFrame(content, fg_color=("#f1f3f5", "#2c2c2c"), corner_radius=10)
        k_frame.grid(row=row, column=0, sticky="nsew", pady=(5, 15))
        k_frame.grid_columnconfigure(1, weight=1)
        AnimatedLabel(k_frame, text="🎲 Số Ngẫu Nhiên (k)", size="large").grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))
        
        AnimatedLabel(k_frame, text="Số ngẫu nhiên k =").grid(row=1, column=0, sticky="w", pady=5, padx=(15, 10))
        self.entry_k = ModernEntry(k_frame, placeholder_text="Dùng để ký, để trống để tạo tự động")
        self.entry_k.grid(row=1, column=1, sticky="ew", pady=(5, 10), padx=(0, 15))
        row += 1

        key_gen_btn_frame = CTkFrame(content, fg_color="transparent")
        key_gen_btn_frame.grid(row=row, column=0, sticky="ew", pady=(5, 5))
        key_gen_btn_frame.grid_columnconfigure((0, 1), weight=1)
        GradientButton(key_gen_btn_frame, text="✨ Tạo Khóa Từ Đầu Vào", image=self.icons.get("input_key"),
                    gradient_colors=[("#3498db", "#2980b9")], command=self.check_and_update_key_params).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        GradientButton(key_gen_btn_frame, text="🎲 Tạo Khóa Ngẫu Nhiên", image=self.icons.get("random_key"),
                    gradient_colors=[("#2ecc71", "#27ae60")], command=self.generate_random_key).grid(row=0, column=1, padx=5, sticky="ew")
        row += 1

        key_action_frame = CTkFrame(content, fg_color="transparent")
        key_action_frame.grid(row=row, column=0, sticky="ew", pady=(5, 5))
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
        content.grid_rowconfigure(1, weight=2) 
        content.grid_rowconfigure(4, weight=3)

        doc_header = CTkFrame(content, fg_color="transparent")
        doc_header.grid(row=0, column=0, sticky="ew", pady=(10, 5))
        doc_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(doc_header, text="📄 Tài Liệu Cần Ký", size="large").grid(row=0, column=0, sticky="w")
        GradientButton(doc_header, text="📁 Mở File", width=100, image=self.icons.get("open_file"),
                      gradient_colors=[("#17a2b8", "#138496")], command=self.open_file_to_sign).grid(row=0, column=1, sticky="e")

        self.text_to_sign = ModernTextbox(content)
        self.text_to_sign.grid(row=1, column=0, sticky="nsew", pady=5)
        self.text_to_sign.bind("<KeyRelease>", self._text_to_sign_modified)
        
        params_frame = CTkFrame(content, fg_color="transparent")
        params_frame.grid(row=2, column=0, sticky="ew", pady=(10,5)) 
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

        AnimatedLabel(content, text="🔏 Chữ Ký đã tạo", size="large").grid(row=3, column=0, sticky="w", pady=(10, 5)) 
        self.signature_output = ModernTextbox(content, state="disabled")
        self.signature_output.grid(row=4, column=0, sticky="nsew", pady=5) 

        action_frame = CTkFrame(content, fg_color="transparent")
        action_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
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
        content.pack(fill="both", expand=True, padx=20, pady=(0, 5))
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=6)
        content.grid_rowconfigure(4, weight=6)

        doc_verify_header = CTkFrame(content, fg_color="transparent")
        doc_verify_header.grid(row=0, column=0, sticky="ew", pady=(5, 2))
        doc_verify_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(doc_verify_header, text="📄 Tài Liệu Cần Xác Minh", size="large").grid(row=0, column=0, sticky="w")
        GradientButton(doc_verify_header, text="📁 Mở File", width=100, image=self.icons.get("open_file"),
                    gradient_colors=[("#17a2b8", "#138496")], command=self.open_file_to_verify).grid(row=0, column=1, sticky="e")

        self.text_to_verify = ModernTextbox(content)
        self.text_to_verify.grid(row=1, column=0, sticky="nsew", pady=2)
        self.text_to_verify.bind("<KeyRelease>", self._check_verification_text_changed)

        self.verification_status_label = AnimatedLabel(content, text="", size="small")
        self.verification_status_label.grid(row=2, column=0, sticky="w", padx=5, pady=(2,5))

        sig_header = CTkFrame(content, fg_color="transparent")
        sig_header.grid(row=3, column=0, sticky="ew", pady=(5, 2))
        sig_header.grid_columnconfigure(0, weight=1)
        AnimatedLabel(sig_header, text="🔏 Chữ Ký Cần Xác Minh", size="large").grid(row=0, column=0, sticky="w")
        GradientButton(sig_header, text="📁 Tải Chữ Ký", width=120, image=self.icons.get("open_file"),
                    gradient_colors=[("#fd79a8", "#e84393")], command=self.load_signature_file).grid(row=0, column=1, sticky="e")

        self.signature_input = ModernTextbox(content)
        self.signature_input.grid(row=4, column=0, sticky="nsew", pady=2)

        CTkFrame(content, fg_color="transparent", height=5).grid(row=5, column=0, sticky="ew", pady=(2,2))

        GradientButton(content, text="🔍 Xác Minh Chữ Ký", image=self.icons.get("check"),
                    gradient_colors=[("#00b894", "#00a085")], command=self.verify_signature).grid(row=6, column=0, sticky="ew", pady=(5, 0))

    def setup_shortcuts(self):
        shortcuts = {
            "<Control-n>": self.generate_random_key,
            "<Control-i>": self.check_and_update_key_params,
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
            theme = data.get("theme", "blue")
            mode_text = "Chế Độ Sáng" if mode == "dark" else "Chế Độ Tối"
        except (FileNotFoundError, json.JSONDecodeError):
            mode, theme, mode_text = "dark", "blue", "Chế Độ Sáng"
            self.save_theme_config(mode, theme)
        set_appearance_mode(mode)
        try:
            theme_path = os.path.join(cwd, "data", "themes", f"{theme}.json")
            if os.path.exists(theme_path):
                 set_default_color_theme(theme_path)
            else:
                 print(f"Theme file not found: {theme_path}, using default.")
                 set_default_color_theme("blue")
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
        progress = CTkProgressBar(dialog, width=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()
        self.update_idletasks()
        return dialog

    def _text_to_sign_modified(self, event=None):
        self.vb1_bytes_to_sign = None

    def _text_to_verify_modified(self, event=None):
        self.vb2_bytes_to_verify = None

    def _set_entry_text(self, entry_widget, text, read_only=False):
        current_state = entry_widget.cget("state")
        entry_widget.configure(state="normal")
        entry_widget.delete("0", END)
        entry_widget.insert("0", str(text))
        if read_only:
            entry_widget.configure(state="readonly")
        elif current_state != "readonly":
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
        self.entry_k.delete("0", END) 
        self._set_entry_text(self.entry_y, "", read_only=True)

    def clear_all_data(self):
        if messagebox.askyesno("Xác Nhận", "🗑️ Bạn có muốn xóa toàn bộ dữ liệu trên tất cả các thẻ không?"):
            self.clear_key_entries()
            self._set_textbox_text(self.text_to_sign, "", disabled=False)
            self._set_textbox_text(self.text_to_verify, "", disabled=False)
            self._set_textbox_text(self.signature_output, "", disabled=True)
            self.signature_input.delete("1.0", END)
            
            self.vb1_bytes_to_sign = None
            self.vb2_bytes_to_verify = None
            self.original_forwarded_text_for_verify = None
            self.verification_status_label.configure(text="")
            
            self.hash_combo.set("SHA-256")
            self.format_combo.set("Hex")
            messagebox.showinfo("Đã Xóa", "Toàn bộ dữ liệu đã được xóa.")

    def generate_random_key(self):
        try:
            bits = int(self.key_size_combo.get())
            msg = f"Đang tạo cặp khóa ElGamal {bits}-bit ngẫu nhiên và số k...\nVui lòng chờ."
            if bits >= 1024: msg += "\nQuá trình này có thể mất một chút thời gian."
            dialog = self.show_working_dialog(msg)
            p, g, x, y = elgamal.cre_key(bits)
            k = elgamal.gen_k_for_signature(p) 
            dialog.destroy()

            self.clear_key_entries()
            self._set_entry_text(self.entry_p, p)
            self._set_entry_text(self.entry_g, g)
            self._set_entry_text(self.entry_x, x)
            self._set_entry_text(self.entry_k, k)
            self._set_entry_text(self.entry_y, y, read_only=True)
            
            messagebox.showinfo("Thành Công", "✅ Cặp khóa (p,g,x,y) và số ngẫu nhiên k đã được tạo!")
        except Exception as e:
            if 'dialog' in locals() and dialog.winfo_exists(): dialog.destroy()
            messagebox.showerror("Lỗi Tạo Khóa Ngẫu Nhiên", f"Không thể tạo khóa hoặc k: {e}")

    def check_and_update_key_params(self):
        try:
            p_str, g_str, x_str, k_str = self.entry_p.get(), self.entry_g.get(), self.entry_x.get(), self.entry_k.get()
            if not all([p_str, g_str, x_str]):
                messagebox.showerror("Thiếu Thông Tin", "Vui lòng nhập đầy đủ p, g, và x để tạo khóa.")
                return

            p = int(p_str)
            g = int(g_str)
            x = int(x_str)

            if not elgamal.check_prime(p):
                messagebox.showerror("Lỗi p", f"Số p ({p}) phải là số nguyên tố.")
                return
            if not (1 < g < p):
                messagebox.showerror("Lỗi g", f"Số g ({g}) phải nằm trong khoảng (1, {p-1}).")
                return
            if not (1 < x < p - 1):
                messagebox.showerror("Lỗi x", f"Số x ({x}) phải nằm trong khoảng (1, {p-1}).")
                return
            if k_str:
                k = int(k_str)
                if not (0 < k < p - 1 and elgamal.find_gcd(k, p - 1) == 1):
                    messagebox.showerror("Lỗi k", f"Số k ({k}) không hợp lệ. Phải (0, {p-1}) & gcd(k, {p-1})=1.")
                    return

            dialog = self.show_working_dialog("Đang tính toán khóa công khai y từ đầu vào...")
            y_calc = elgamal.pow_mod(g, x, p)
            dialog.destroy()
            self._set_entry_text(self.entry_y, str(y_calc), read_only=True)
            messagebox.showinfo("Thành Công", "Đã tạo khóa (p,g,x,y) từ đầu vào thành công.")
        except ValueError:
            messagebox.showerror("Lỗi Đầu Vào", "Các giá trị p, g, x, k phải là số nguyên.")
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
            
            if not y_s:
                if expected_y_val is not None:
                    if action_type != "verification":
                        if messagebox.askyesno("Thiếu y", f"Tính y từ (p,g,x)? y={expected_y_val}", icon=messagebox.WARNING):
                            self._set_entry_text(self.entry_y, str(expected_y_val), read_only=True)
                            y = expected_y_val
                        else: messagebox.showerror("Lỗi Khóa", "y là bắt buộc."); return None
                    else:
                         messagebox.showerror("Lỗi Khóa", "y trống. Cần y để xác minh."); return None
                elif action_type == "verification":
                    messagebox.showerror("Lỗi Khóa", "y trống và không thể tính. Cần y để xác minh."); return None
            else:
                y = int(y_s)
                if not (0 < y < p): messagebox.showerror("Lỗi y", f"Số y ({y}) phải trong (0, {p})."); return None
                if expected_y_val is not None and y != expected_y_val:
                    if messagebox.askyesno("Không Khớp y", f"y hiện tại ({y}) khác y tính từ (p,g,x) ({expected_y_val}). Cập nhật?", icon=messagebox.WARNING):
                        self._set_entry_text(self.entry_y, str(expected_y_val), read_only=True); y = expected_y_val
                    else: return None
            
            if action_type == "signing": return p, g, x
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
        
        k_str = self.entry_k.get().strip()
        k = int(k_str) if k_str else None
        if k and not (0 < k < p - 1 and elgamal.find_gcd(k, p - 1) == 1):
            messagebox.showerror("Lỗi k", f"Số k ({k}) không hợp lệ. Phải (0, {p-1}) & gcd(k, {p-1})=1.")
            return
        
        bits_str = self.key_size_combo.get()
        
        file_types = (
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        )
        
        fp = filedialog.asksaveasfilename(
            initialdir=cwd, 
            title="Lưu Khóa ElGamal",
            filetypes=file_types,
            defaultextension=".json"
        )
        
        if not fp: 
            return 
        
        try:
            with open(fp, "w", encoding="utf-8") as f:
                if fp.lower().endswith(".txt"):
                    txt_content = f"--- Khóa ElGamal ---\n"
                    txt_content += f"Độ dài khóa: {bits_str}\n\n" 
                    txt_content += f"p: {p}\n"
                    txt_content += f"g: {g}\n"
                    txt_content += f"y (khóa công khai): {y}\n"
                    txt_content += f"x (khóa bí mật): {x}\n"
                    if k: txt_content += f"k (số ngẫu nhiên): {k}\n"
                    f.write(txt_content)
                    messagebox.showinfo("Thành Công", f"Đã lưu khóa dưới dạng văn bản (TXT) vào:\n{fp}")
                else: 
                    key_data = {
                        "description": "Khóa ElGamal", 
                        "bit_length": bits_str, 
                        "p": p, 
                        "g": g, 
                        "x_private_key": x, 
                        "y_public_key": y
                    }
                    if k: key_data["k_random"] = k
                    json.dump(key_data, f, indent=4)
                    
                    if fp.lower().endswith(".json"):
                        messagebox.showinfo("Thành Công", f"Đã lưu khóa dưới dạng JSON vào:\n{fp}")
                    else:
                        messagebox.showinfo("Thành Công", f"Đã lưu khóa (sử dụng định dạng JSON) vào:\n{fp}")
                        
        except Exception as e: 
            messagebox.showerror("Lỗi Lưu Khóa", f"Không thể lưu file:\n{e}")

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
                          [('p','p'), ('g','g'), ('x','x_private_key'), ('y','y_public_key'), ('bit_length','bit_length'), ('k','k_random')]}
                else:
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
                            elif key_part == "k (số ngẫu nhiên)": kd['k'] = int(value_part)
                            elif key_part == "độ dài khóa": kd['bit_length'] = value_part
            
            self.clear_key_entries()
            self._set_entry_text(self.entry_p, kd.get("p", ""))
            self._set_entry_text(self.entry_g, kd.get("g", ""))
            self._set_entry_text(self.entry_x, kd.get("x", ""))
            self._set_entry_text(self.entry_k, kd.get("k", "")) 
            self._set_entry_text(self.entry_y, kd.get("y", ""), read_only=True)
            
            bits_val = kd.get("bit_length", self.key_bit_sizes[1])
            if str(bits_val) in [str(s) for s in self.key_bit_sizes]: self.key_size_combo.set(str(bits_val))
            else: self.key_size_combo.set(str(self.key_bit_sizes[1]))
            
            messagebox.showinfo("Thanh Công", f"Đã tải khóa từ:\n{fp}")
        except Exception as e: messagebox.showerror("Lỗi Tải Khóa", f"Lỗi đọc file ({fp}) hoặc định dạng không đúng:\n{e}")

    def open_file_to_sign(self):
        filetypes = (
            ("All Files", "*.*"),
            ("Excel Files", "*.xlsx *.xls"),
            ("Word Documents", "*.docx"),
            ("PDF Files", "*.pdf"),
            ("Text Files", "*.txt")
        )
        fp = filedialog.askopenfilename(initialdir=cwd, title="Mở File Để Ký", filetypes=filetypes).strip()
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
        self.original_forwarded_text_for_verify = None
        self.verification_status_label.configure(text="")
        filetypes = (
            ("All Files", "*.*"),
            ("Excel Files", "*.xlsx *.xls"),
            ("Word Documents", "*.docx"),
            ("PDF Files", "*.pdf"),
            ("Text Files", "*.txt")
        )
        fp = filedialog.askopenfilename(initialdir=cwd, title="Mở File Để Xác Minh", filetypes=filetypes).strip()
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
            filetypes=(("Signature Files", "*.sig"), ("Text files", "*.txt"), ("All files", "*.*"))).strip()
        if not fp: return
        self.signature_input.delete("1.0", END)
        try:
            with open(fp, "r", encoding="utf-8") as f: data = f.read()
            self.signature_input.insert("1.0", data.strip())
            messagebox.showinfo("Thành Công", f"Đã tải chữ ký từ: {os.path.basename(fp)}")
        except Exception as e: messagebox.showerror("Lỗi", f"Không thể đọc file chữ ký:\n{e}")

    def sign_document(self):
        key_params = self.get_key_params_for_action(action_type="signing")
        if not key_params: messagebox.showerror("Lỗi Khóa", "Không thể ký. Kiểm tra (p,g,x)."); return
        p, g, x = key_params

        k_for_signing_str = self.entry_k.get().strip()
        k_for_signing = None
        dialog = None
        try:
            if k_for_signing_str:
                k_for_signing = int(k_for_signing_str)
                if not (0 < k_for_signing < p - 1 and elgamal.find_gcd(k_for_signing, p - 1) == 1):
                    messagebox.showerror("Lỗi k", f"k ({k_for_signing}) không hợp lệ. Phải (0, {p-1}) & gcd(k, {p-1})=1.")
                    return
            else:
                dialog_k_gen = self.show_working_dialog("Đang tạo số ngẫu nhiên k...")
                k_for_signing = elgamal.gen_k_for_signature(p)
                self._set_entry_text(self.entry_k, str(k_for_signing))
                dialog_k_gen.destroy()
            
            mode_hash = self.hash_combo.get()
            format_type = self.format_combo.get()
            
            current_doc_bytes_to_sign = None
            if self.vb1_bytes_to_sign is not None:
                current_doc_bytes_to_sign = self.vb1_bytes_to_sign
            else:
                text_to_sign_str = self.text_to_sign.get("1.0", END).strip()
                if not text_to_sign_str: messagebox.showwarning("Thiếu Dữ Liệu", "Nội dung ký trống!"); return
                current_doc_bytes_to_sign = text_to_sign_str.encode('utf-8')
            
            if current_doc_bytes_to_sign is None: messagebox.showerror("Lỗi", "Không có dữ liệu để ký."); return

            dialog = self.show_working_dialog("Đang tạo chữ ký...")
            r_val, s_val = elgamal.create_sign(current_doc_bytes_to_sign, mode_hash, p, g, x, k_for_signing)
            
            generated_signature_str = elgamal.encode_signature(r_val, s_val, format_type)
            self._set_textbox_text(self.signature_output, generated_signature_str)
            
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

        if not vb_display and not ck and self.vb1_bytes_to_sign is None:
            messagebox.showwarning("Lỗi Chuyển Tiếp", "Không có dữ liệu để chuyển tiếp!")
            return

        self._set_textbox_text(self.text_to_verify, vb_display if vb_display else "", disabled=False)
        self.signature_input.delete("1.0", END)
        if ck: self.signature_input.insert("1.0", ck)
        
        if self.vb1_bytes_to_sign is not None:
            self.vb2_bytes_to_verify = self.vb1_bytes_to_sign
        elif vb_display:
            self.vb2_bytes_to_verify = vb_display.encode('utf-8')
        else:
            self.vb2_bytes_to_verify = None

        self.original_forwarded_text_for_verify = vb_display
        self._check_verification_text_changed()

        messagebox.showinfo("Thành Công", "✅ Dữ liệu (văn bản, chữ ký) đã được chuyển sang thẻ Xác Minh!")

    def save_signature(self):
        self.signature_output.configure(state="normal")
        data = self.signature_output.get("1.0", END).strip()
        self.signature_output.configure(state="disabled")
        if not data:
            messagebox.showwarning("Lỗi Lưu", "Chưa có chữ ký để lưu!")
            return
        
        filetypes_list = (
            ("Signature File", "*.sig"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        )

        fp = filedialog.asksaveasfilename(
            initialdir=cwd,
            title="Lưu File Chữ Ký",
            filetypes=filetypes_list,
            defaultextension=".sig"
        )
        if fp:
            try:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(data)
                messagebox.showinfo("Thành Công", f"Đã lưu chữ ký!\n{fp}")
            except Exception as e:
                messagebox.showerror("Lỗi Lưu File", f"Không thể lưu:\n{e}")

    def verify_signature(self):
        key_params = self.get_key_params_for_action(action_type="verification")
        if not key_params:
            messagebox.showerror("Lỗi Khóa", "Không thể xác minh. Vui lòng kiểm tra các tham số khóa công khai (p, g, y).")
            return
        p_val, g_val, y_val = key_params

        hash_algo = self.hash_combo.get()
        format_type = self.format_combo.get()
        
        signature_str = self.signature_input.get("1.0", END).strip()
        if not signature_str:
            messagebox.showwarning("Thiếu Chữ Ký", "Vui lòng nhập hoặc tải chữ ký cần xác minh.")
            return
        
        doc_bytes = None
        if self.vb2_bytes_to_verify is not None:
            doc_bytes = self.vb2_bytes_to_verify
        else:
            text_to_verify_str = self.text_to_verify.get("1.0", END).strip()
            if not text_to_verify_str:
                messagebox.showwarning("Thiếu Dữ Liệu", "Không có nội dung tài liệu để xác minh.")
                return
            doc_bytes = text_to_verify_str.encode('utf-8')
        
        if doc_bytes is None:
            messagebox.showerror("Lỗi Dữ Liệu", "Không tìm thấy dữ liệu tài liệu để tiến hành xác minh.")
            return

        dialog = self.show_working_dialog("Đang xác minh chữ ký...")
        try:
            status = elgamal.verify_sign(
                data_bytes=doc_bytes,
                hash_mode=hash_algo,
                signature_str=signature_str,
                format_type=format_type,
                p=p_val, g=g_val, y=y_val
            )
            
            if dialog and dialog.winfo_exists():
                dialog.destroy()

            if status == elgamal.VerificationStatus.VALID:
                messagebox.showinfo("Thành Công", "✅ Chữ ký hợp lệ!\nChữ ký đã được xác minh và hoàn toàn khớp với tài liệu.")
            elif status == elgamal.VerificationStatus.CRYPTO_MISMATCH:
                messagebox.showerror("Thất Bại", "❌ Chữ ký không hợp lệ!\nNội dung tài liệu không khớp với chữ ký. Dữ liệu có thể đã bị thay đổi.")
            else:
                messagebox.showerror("Lỗi Không Xác Định", f"Quá trình xác minh trả về trạng thái không rõ: {status}")

        except elgamal.SignatureDecodeError as e:
            if dialog and dialog.winfo_exists():
                dialog.destroy()
            messagebox.showerror("Lỗi Dữ Liệu Chữ Ký", str(e)) 

        except Exception as e:
            if dialog and dialog.winfo_exists():
                dialog.destroy()
            messagebox.showerror("Lỗi Xử Lý", f"Đã xảy ra lỗi trong quá trình xác minh: {e}")
            
    def thoat(self):
        if messagebox.askyesno("Thông Báo", "Bạn có muốn thoát không?"):
            self.quit()

    def _check_verification_text_changed(self, event=None):
        if self.original_forwarded_text_for_verify is None:
            return 

        current_text = self.text_to_verify.get("1.0", END).strip()
        original_text = self.original_forwarded_text_for_verify.strip()

        if current_text == original_text:
            self.verification_status_label.configure(
                text="✅ Nội dung khớp với văn bản gốc đã chuyển.",
                text_color=("#27ae60", "#2ecc71")
            )
        else:
            self.verification_status_label.configure(
                text="⚠️ CẢNH BÁO: Nội dung đã bị thay đổi so với văn bản gốc!",
                text_color=("#d35400", "#e67e22")
        )

if __name__ == "__main__":
    app = BeautifulElGamalApp()
    try:
        icon_path = os.path.join(cwd, "data", "images", "icon.ico")
        if os.path.exists(icon_path): app.iconbitmap(icon_path)
        else: print(f"Không tìm thấy file icon.ico tại: {icon_path}")
    except Exception as e: print(f"Không thể tải icon.ico: {e}")
    app.mainloop()