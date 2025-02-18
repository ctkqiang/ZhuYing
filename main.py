# -*- coding: UTF-8 -*-

import cv2
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Tuple, Optional
from tkinter import messagebox
from PIL import Image, ImageTk


class 竹影:
    def __init__(self) -> None:
        super(竹影, self).__init__()
        # Remove pygame.mixer.init()

        # 设置应用程序基本信息
        self.name: str = "竹影"
        self.version: str = "1.0.0"
        self.author: str = "钟智强"
        self.author_email: str = "johnmelodymel@qq.com"
        self.author_url: str = "https://ctkqiang.xin"
        self.description: str = "竹影"

        # 初始化主窗口和组件
        self.root: tk.Tk = tk.Tk()
        self.filename_entry: Optional[ttk.Entry] = None

        # 设置窗口标题和图标
        self.root.title(f"{self.name} v{self.version} - 视频转录工具")
        self.root.iconbitmap("assets/icon.ico")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # 设置菜单栏
        self.menubar: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # 设置文件菜单
        filemenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开文件", command=self.select_file)
        filemenu.add_separator()  # 添加分隔线
        filemenu.add_command(label="退出程序", command=self.root.quit)

        # 设置编辑菜单
        editmenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="编辑", menu=editmenu)
        editmenu.add_command(
            label="清除内容",
            command=lambda: (
                self.filename_entry.delete(0, tk.END) if self.filename_entry else None
            ),
        )

        # 设置关于菜单
        aboutmenu: tk.Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="帮助", menu=aboutmenu)
        aboutmenu.add_command(label="使用说明", command=self.show_help)
        aboutmenu.add_separator()
        aboutmenu.add_command(label="检查更新", command=self.check_update)
        aboutmenu.add_separator()
        aboutmenu.add_command(label=f"关于{self.name}", command=self.show_about)

    def show_help(self) -> None:
        # 显示使用说明
        messagebox.showinfo(
            "使用说明",
            '1. 点击"选择文件"按钮选择视频文件\n',
            "2. 等待视频加载完成\n",
            '3. 点击"转录"开始处理\n',
            "4. 处理完成后可以导出结果",
        )

    def check_update(self) -> None:
        # 检查更新
        messagebox.showinfo("检查更新", f"当前版本: v{self.version}\n" "已是最新版本")

        # 配置窗口属性
        self.root.title(self.name)
        self.root.geometry("1000x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self) -> None:
        if hasattr(self, "cap"):
            self.cap.release()
        # 退出前清理音频
        pygame.mixer.quit()
        self.root.quit()

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
            self.current_video = filename
            self.show_video_thumbnail(filename)
        else:
            messagebox.showwarning("警告", "未选择任何文件")

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
            filename_frame,
            text="选择文件",
            command=self.select_file,
            width=15,
        )
        select_btn.pack(side=tk.LEFT, padx=(5, 0), pady=5)

        middle_frame: ttk.Frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 创建视频显示区域
        video_frame: ttk.LabelFrame = ttk.LabelFrame(middle_frame, text="视频")
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 添加视频标签用于显示视频
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # 添加视频控制按钮
        video_controls = ttk.Frame(video_frame)
        video_controls.pack(fill=tk.X, pady=5)

        self.play_btn = ttk.Button(
            video_controls, text="播放", command=self.toggle_play, width=15
        )
        self.play_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = ttk.Button(
            video_controls, text="停止", command=self.stop_video, width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

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

        export_btn: ttk.Button = ttk.Button(button_frame, text="导出", width=15)
        export_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        reset_btn: ttk.Button = ttk.Button(button_frame, text="重置", width=15)
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)

        return self.root.mainloop()

    def play_video(self, video_path: str) -> None:
        self.cap = cv2.VideoCapture(video_path)

        def update_frame():
            while True and hasattr(self, "is_playing") and self.is_playing:
                ret, frame = self.cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_rgb = cv2.resize(frame_rgb, (270, 480))
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                    self.video_label.configure(image=photo)
                    self.video_label.image = photo
                    self.root.after(30)
                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.video_thread = threading.Thread(target=update_frame, daemon=True)
        self.video_thread.start()

    def toggle_play(self) -> None:
        if hasattr(self, "is_playing") and self.is_playing:
            self.is_playing = False
            self.play_btn.configure(text="播放")
            if hasattr(self, "cap"):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video position
        else:
            self.is_playing = True
            self.play_btn.configure(text="暂停")
            if hasattr(self, "current_video"):
                self.play_video(self.current_video)

    def stop_video(self) -> None:
        try:
            self.is_playing = False
            if hasattr(self, "cap") and self.cap is not None:
                self.cap.release()
                self.cap = None
            if hasattr(self, "current_video"):
                self.show_video_thumbnail(self.current_video)
            self.play_btn.configure(text="播放")
        except Exception as e:
            print(f"Error stopping video: {e}")

    def on_closing(self) -> None:
        try:
            if hasattr(self, "cap") and self.cap is not None:
                self.cap.release()
                self.cap = None
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.root.quit()

    def show_video_thumbnail(self, video_path: str) -> None:
        # 获取视频第一帧作为缩略图
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()

        if ret:
            # 转换并调整图像大小为垂直格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (270, 480))  # 调整为更小的固定尺寸
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

            # 显示缩略图
            self.video_label.configure(image=photo)
            self.video_label.image = photo
        cap.release()

    def toggle_play(self) -> None:
        if hasattr(self, "is_playing") and self.is_playing:
            self.is_playing = False
            self.play_btn.configure(text="播放")
        else:
            self.is_playing = True
            self.play_btn.configure(text="暂停")

            if hasattr(self, "current_video"):
                self.play_video(self.current_video)

    def stop_video(self) -> None:
        # 停止视频播放并显示缩略图
        if hasattr(self, "cap"):
            self.is_playing = False
            self.cap.release()

            if hasattr(self, "current_video"):
                self.show_video_thumbnail(self.current_video)

            self.play_btn.configure(text="播放")


if __name__ == "__main__":
    app: 竹影 = 竹影()
    app.main_window()
