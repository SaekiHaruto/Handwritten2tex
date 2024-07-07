import tkinter as tk
from tkinter import ttk, messagebox
from whiteboard import Whiteboard
from tex_converter import handwritten2tex, tex2img
import os
from PIL import Image, ImageTk
import threading
import time


class LoadingAnimation:
    def __init__(self, master, text="Converting"):
        self.master = master
        self.text = text
        self.label = ttk.Label(self.master, text=self.text, font=("Arial", 14))
        self.label.pack(pady=20)
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self.animate, daemon=True).start()

    def stop(self):
        self.is_running = False
        self.label.destroy()

    def animate(self):
        dots = 0
        while self.is_running:
            dots = (dots + 1) % 4
            self.label.config(text=f"{self.text}{'.' * dots}")
            time.sleep(0.5)


class MathFormulaConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Math Formula Converter")

        # フルスクリーン設定
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_fullscreen)

        self.current_tex = ""  # TeXコードを保持する変数

        # メインフレーム
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1段目: ホワイトボード (画面の70%を占める)
        whiteboard_frame = ttk.Frame(main_frame)
        whiteboard_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        self.whiteboard = Whiteboard(whiteboard_frame)
        self.whiteboard.canvas.pack(fill=tk.BOTH, expand=True)

        # 2段目: ボタン類 (画面の10%を占める)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Clear", command=self.whiteboard.clear_canvas).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Undo", command=self.whiteboard.undo).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="to tex", command=self.convert_to_tex).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Copy", command=self.copy_tex).pack(side=tk.RIGHT, padx=10)

        # 3段目: 画像表示エリア (画面の20%を占める)
        self.img_frame = ttk.Frame(main_frame)
        self.img_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        self.img_label = ttk.Label(self.img_frame)
        self.img_label.pack(fill=tk.BOTH, expand=True)

        # デフォルト画像の表示
        self.display_default_image()

        # ローディングアニメーション
        self.loading_animation = None

    def exit_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", False)

    def display_default_image(self):
        default_img_path = "input/default.png"
        if os.path.exists(default_img_path):
            self.display_image(default_img_path)
        else:
            self.img_label.config(text="Default image not found")

    def display_image(self, img_path):
        img = Image.open(img_path)
        img = self.resize_image(img)
        photo = ImageTk.PhotoImage(img)
        self.img_label.config(image=photo)
        self.img_label.image = photo

    def resize_image(self, img):
        # 画面の幅に合わせて画像をリサイズ
        width = self.master.winfo_width()
        height = int(width / 4)  # 幅の1/4の高さにする
        return img.resize((width, height), Image.LANCZOS)

    def convert_to_tex(self):
        # ローディングアニメーションの開始
        self.loading_animation = LoadingAnimation(self.img_frame)
        self.loading_animation.start()

        # 別スレッドで変換処理を実行
        threading.Thread(target=self._convert_to_tex_thread, daemon=True).start()

    def _convert_to_tex_thread(self):
        self.whiteboard.save_canvas("input/input.png")
        self.current_tex = handwritten2tex("input/input.png")
        tex2img(self.current_tex)

        # メインスレッドで結果を表示
        self.master.after(0, self._show_conversion_result)

    def _show_conversion_result(self):
        # ローディングアニメーションの停止
        if self.loading_animation:
            self.loading_animation.stop()
            self.loading_animation = None

        self.display_image("output/output.png")

    def copy_tex(self):
        if self.current_tex:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.current_tex)
            messagebox.showinfo("コピー成功", "TeXコードがクリップボードにコピーされました。")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathFormulaConverter(root)
    root.mainloop()