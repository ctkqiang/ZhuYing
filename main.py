# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Tuple, Optional
from tkinter import messagebox


class 竹影:
    def __init__(self) -> None:
        super(竹影, self).__init__()

        self.name: str = "竹影"
        self.version: str = "1.0.0"
        self.author: str = "钟智强"
        self.author_email: str = "johnmelodymel@qq.com"
        self.author_url: str = "https://ctkqiang.xin"
        self.description: str = "竹影"

        self.root: tk.Tk = tk.Tk()
        self.filename_entry: Optional[ttk.Entry] = None

        self.menubar: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # 文件菜单
        filemenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开文件", command=self.select_file)
        filemenu.add_separator()
        filemenu.add_command(label="退出程序", command=self.root.quit)

        # 编辑菜单
        editmenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="编辑", menu=editmenu)

        editmenu.add_command(
            label="清除内容",
            command=lambda: (
                self.filename_entry.delete(0, tk.END) if self.filename_entry else None
            ),
        )

        # 关于菜单
        aboutmenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="关于", menu=aboutmenu)
        aboutmenu.add_command(label=f"关于{self.name}", command=self.show_about)

        self.root.title(self.name)
        self.root.geometry("1000x600")

    def show_about(self) -> None:
        messagebox.showinfo(
            "关于",
            f"{self.name} v{self.version}\n\n"
            f"开发者: {self.author}\n"
            f"邮箱: {self.author_email}\n"
            f"网站: {self.author_url}",
        )

    def select_file(self) -> None:
        filetypes: Tuple[Tuple[str, str], ...] = (
            ("视频文件", "*.mp4 *.avi *.mov *.mkv"),
            ("所有文件", "*.*"),
        )

        filename: str = filedialog.askopenfilename(
            title="选择视频文件", filetypes=filetypes
        )

        if filename and self.filename_entry:
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, filename)
        else:
            print("未选择任何文件.")

    def main_window(self) -> None:
        main_frame: ttk.Frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        filename_frame: ttk.Frame = ttk.Frame(main_frame)
        filename_frame.pack(fill=tk.X, pady=(0, 10))
        filename_label: ttk.Label = ttk.Label(filename_frame, text="文件名:")
        filename_label.pack(side=tk.LEFT)

        self.filename_entry = ttk.Entry(filename_frame)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        select_btn: ttk.Button = ttk.Button(
            filename_frame, text="选择文件", command=self.select_file
        )
        select_btn.pack(side=tk.LEFT, padx=(5, 0))

        middle_frame: ttk.Frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        video_frame: ttk.LabelFrame = ttk.LabelFrame(middle_frame, text="视频")
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        transcribe_frame: ttk.LabelFrame = ttk.LabelFrame(middle_frame, text="转录")
        transcribe_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        transcribe_text: tk.Text = tk.Text(transcribe_frame, height=10)
        transcribe_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        output_frame: ttk.LabelFrame = ttk.LabelFrame(main_frame, text="输出")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        output_text: tk.Text = tk.Text(output_frame, height=8)
        output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame: ttk.Frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        export_btn: ttk.Button = ttk.Button(button_frame, text="导出")
        export_btn.pack(side=tk.LEFT, padx=(0, 5))

        reset_btn: ttk.Button = ttk.Button(button_frame, text="重置")
        reset_btn.pack(side=tk.LEFT)

        return self.root.mainloop()


if __name__ == "__main__":
    app: 竹影 = 竹影()
    app.main_window()
