# -*- coding: UTF-8 -*-
import os
import cv2
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Tuple, Optional
from tkinter import messagebox
from PIL import Image, ImageTk
from src.video_processing import 视频处理器
from src.database_handler import 数据库处理器


class 竹影:
    def __init__(self) -> None:
        super(竹影, self).__init__()

        # 设置应用程序基本信息
        self.名称: str = "竹影"
        self.版本: str = "1.0.0"
        self.作者: str = "钟智强"
        self.作者邮箱: str = "johnmelodymel@qq.com"
        self.作者网址: str = "https://ctkqiang.xin"
        self.描述: str = "竹影"

        # 初始化主窗口和组件
        self.根窗口: tk.Tk = tk.Tk()
        self.文件名输入框: Optional[ttk.Entry] = None

        self.视频处理器 = None

        # 设置窗口标题和图标
        self.根窗口.title(f"{self.名称} v{self.版本} - 视频转录工具")
        try:
            if os.sys.platform == "darwin":
                icon_path = "./assets/icon.png"
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    self.根窗口.iconphoto(True, img)
            else:
                icon_path = "./assets/icon.ico"
                if os.path.exists(icon_path):
                    self.根窗口.iconbitmap(icon_path)
        except Exception as e:
            print(f"无法加载图标: {e}")
        self.根窗口.geometry("1400x1000")
        self.根窗口.minsize(1200, 600)

        # 设置菜单栏
        self.菜单栏: tk.Menu = tk.Menu(self.根窗口)
        self.根窗口.config(menu=self.菜单栏)

        # 设置文件菜单
        文件菜单: tk.Menu = tk.Menu(self.菜单栏, tearoff=0)
        self.菜单栏.add_cascade(label="文件", menu=文件菜单)
        文件菜单.add_command(label="打开文件", command=self.选择文件)
        文件菜单.add_separator()  # 添加分隔线
        文件菜单.add_command(label="退出程序", command=self.根窗口.quit)

        # 设置编辑菜单
        编辑菜单: tk.Menu = tk.Menu(self.菜单栏, tearoff=0)
        self.菜单栏.add_cascade(label="编辑", menu=编辑菜单)
        编辑菜单.add_command(
            label="清除内容",
            command=lambda: (
                self.文件名输入框.delete(0, tk.END) if self.文件名输入框 else None
            ),
        )

        # 设置关于菜单
        关于菜单: tk.Menu = tk.Menu(self.菜单栏, tearoff=0)
        self.菜单栏.add_cascade(label="帮助", menu=关于菜单)
        关于菜单.add_command(label="使用说明", command=self.显示帮助)
        关于菜单.add_separator()
        关于菜单.add_command(label="检查更新", command=self.检查更新)
        关于菜单.add_separator()
        关于菜单.add_command(label=f"关于{self.名称}", command=self.显示关于)

    def 显示帮助(self) -> None:
        # 显示使用说明
        messagebox.showinfo(
            "使用说明",
            '1. 点击"选择文件"按钮选择视频文件\n',
            "2. 等待视频加载完成\n",
            '3. 点击"转录"开始处理\n',
            "4. 处理完成后可以导出结果",
        )

    def 检查更新(self) -> None:
        # 检查更新
        messagebox.showinfo("检查更新", f"当前版本: v{self.版本}\n" "已是最新版本")

        # 配置窗口属性
        self.根窗口.title(self.名称)
        self.根窗口.geometry("1000x600")
        self.根窗口.protocol("WM_DELETE_WINDOW", self.关闭时)

    def 关闭时(self) -> None:
        if hasattr(self, "视频捕获"):
            self.视频捕获.release()
        # 退出前清理音频
        self.根窗口.quit()

    def 显示关于(self) -> None:
        messagebox.showinfo(
            "关于",
            f"{self.名称} v{self.版本}\n\n"
            f"开发者: {self.作者}\n"
            f"邮箱: {self.作者邮箱}\n"
            f"网站: {self.作者网址}",
        )

    def 选择文件(self) -> None:
        文件类型: Tuple[Tuple[str, str], ...] = (
            ("视频文件", "*.mp4 *.avi *.mov *.mkv"),
            ("所有文件", "*.*"),
        )

        文件名: str = filedialog.askopenfilename(
            title="选择视频文件", filetypes=文件类型
        )

        if 文件名 and self.文件名输入框:
            self.文件名输入框.delete(0, tk.END)
            self.文件名输入框.insert(0, 文件名)
            self.当前视频 = 文件名
            self.显示视频缩略图(文件名)
            self.视频处理器 = 视频处理器(视频路径=文件名)

            现有记录 = self.数据库.获取视频记录(文件路径=文件名)
            if 现有记录:
                _, _, _, 已有转录 = 现有记录
                if 已有转录:
                    self.转录文本.delete("1.0", tk.END)
                    self.转录文本.insert(tk.END, 已有转录)
                    self.状态标签["text"] = "已加载现有转录"
        else:
            messagebox.showwarning("警告", "未选择任何文件")

    def 更新转录结果(self, 结果: str) -> None:

        self.转录文本.delete("1.0", tk.END)
        self.转录文本.insert(tk.END, 结果)

        if hasattr(self, "当前视频"):
            文件名 = os.path.basename(self.当前视频)
            现有记录 = self.数据库.获取视频记录(文件路径=self.当前视频)

            if 现有记录:
                self.数据库.更新转录文本(self.当前视频, 结果)
            else:
                self.数据库.保存视频记录(
                    文件名=文件名, 文件路径=self.当前视频, 转录文本=结果
                )

    def 关闭时(self) -> None:
        # 如果对象有"视频捕获"属性
        if hasattr(self, "视频捕获"):
            self.视频捕获.release()
            # 释放视频捕获资源
            self.视频捕获.release()

        # 如果对象有"数据库"属性
        if hasattr(self, "数据库"):
            self.根窗口.quit()
            del self.数据库

        # 关闭根窗口

    def 主窗口(self) -> None:
        主框架: ttk.Frame = ttk.Frame(self.根窗口)
        主框架.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        文件名框架: ttk.Frame = ttk.Frame(主框架)
        文件名框架.pack(fill=tk.X, pady=(0, 10))
        文件名标签: ttk.Label = ttk.Label(文件名框架, text="文件名:")
        文件名标签.pack(side=tk.LEFT)

        self.文件名输入框 = ttk.Entry(文件名框架)
        self.文件名输入框.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        选择按钮: ttk.Button = ttk.Button(
            文件名框架,
            text="选择文件",
            command=self.选择文件,
            width=15,
        )
        选择按钮.pack(side=tk.LEFT, padx=(5, 0), pady=5)

        中间框架: ttk.Frame = ttk.Frame(主框架)
        中间框架.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 创建视频显示区域
        视频框架: ttk.LabelFrame = ttk.LabelFrame(中间框架, text="视频")
        视频框架.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 添加视频标签用于显示视频
        self.视频标签 = ttk.Label(视频框架)
        self.视频标签.pack(fill=tk.BOTH, expand=True)

        # 添加视频控制按钮
        视频控制 = ttk.Frame(视频框架)
        视频控制.pack(fill=tk.X, pady=5)

        self.播放按钮 = ttk.Button(
            视频控制, text="播放", command=self.切换播放, width=15
        )
        self.播放按钮.pack(side=tk.LEFT, padx=5, pady=5)

        self.停止按钮 = ttk.Button(
            视频控制, text="停止", command=self.停止视频, width=15
        )
        self.停止按钮.pack(side=tk.LEFT, padx=5, pady=5)

        转录框架: ttk.LabelFrame = ttk.LabelFrame(中间框架, text="转录")
        转录框架.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.进度条 = ttk.Progressbar(转录框架, mode="determinate")
        self.进度条.pack(fill=tk.X, padx=5, pady=(5, 0))

        self.状态标签 = ttk.Label(转录框架, text="就绪")
        self.状态标签.pack(pady=(2, 5))

        self.转录文本: tk.Text = tk.Text(转录框架, height=10, font=(None, 20))
        self.转录文本.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add transcribe button
        转录按钮: ttk.Button = ttk.Button(
            转录框架, text="开始转录", command=self.开始转录, width=15
        )
        转录按钮.pack(side=tk.BOTTOM, pady=5)

        输出框架: ttk.LabelFrame = ttk.LabelFrame(主框架, text="输出")
        输出框架.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        输出文本: tk.Text = tk.Text(输出框架, height=8)
        输出文本.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        按钮框架: ttk.Frame = ttk.Frame(主框架)
        按钮框架.pack(fill=tk.X)

        导出按钮: ttk.Button = ttk.Button(按钮框架, text="导出", width=15)
        导出按钮.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        重置按钮: ttk.Button = ttk.Button(按钮框架, text="重置", width=15)
        重置按钮.pack(side=tk.LEFT, padx=5, pady=5)

        return self.根窗口.mainloop()

    def 播放视频(self, 视频路径: str) -> None:
        self.视频捕获 = cv2.VideoCapture(视频路径)

        def 更新帧():
            while True and hasattr(self, "正在播放") and self.正在播放:
                ret, frame = self.视频捕获.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_rgb = cv2.resize(frame_rgb, (270, 480))
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                    self.视频标签.configure(image=photo)
                    self.视频标签.image = photo
                    self.根窗口.after(30)
                else:
                    self.视频捕获.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.视频线程 = threading.Thread(target=更新帧, daemon=True)
        self.视频线程.start()

    def 切换播放(self) -> None:
        if hasattr(self, "正在播放") and self.正在播放:
            self.正在播放 = False
            self.播放按钮.configure(text="播放")
            if hasattr(self, "视频捕获"):
                self.视频捕获.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video position
        else:
            self.正在播放 = True
            self.播放按钮.configure(text="暂停")
            if hasattr(self, "当前视频"):
                self.播放视频(self.当前视频)

    def 停止视频(self) -> None:
        try:
            self.正在播放 = False
            if hasattr(self, "视频捕获") and self.视频捕获 is not None:
                self.视频捕获.release()
                self.视频捕获 = None
            if hasattr(self, "当前视频"):
                self.显示视频缩略图(self.当前视频)
            self.播放按钮.configure(text="播放")
        except Exception as e:
            print(f"Error stopping video: {e}")

    def 显示视频缩略图(self, 视频路径: str) -> None:
        # 获取视频第一帧作为缩略图
        cap = cv2.VideoCapture(视频路径)
        ret, frame = cap.read()

        if ret:
            # 转换并调整图像大小为垂直格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (270, 480))  # 调整为更小的固定尺寸
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

            # 显示缩略图
            self.视频标签.configure(image=photo)
            self.视频标签.image = photo
        cap.release()

    def 开始转录(self) -> None:
        """执行视频转录"""
        if not hasattr(self, "当前视频") or not self.当前视频:
            messagebox.showwarning("警告", "请先选择视频文件")
            return

        try:
            self.转录文本.delete("1.0", tk.END)
            self.转录文本.insert(tk.END, "正在转录中...\n")
            self.转录文本.update()

            # Reset progress bar
            self.进度条["value"] = 0
            self.状态标签["text"] = "正在准备转录..."

            def 更新进度(阶段: str, 进度: int):
                self.进度条["value"] = 进度
                self.状态标签["text"] = f"{阶段} - {进度}%"
                self.根窗口.update()

            def 执行转录任务():
                try:
                    更新进度("正在提取音频", 10)
                    音频路径 = self.视频处理器.提取音频()

                    更新进度("正在加载模型", 30)
                    更新进度("正在转录音频", 50)
                    结果 = self.视频处理器.执行转录(保留音频=False)

                    更新进度("处理完成", 100)
                    self.根窗口.after(0, self.更新转录结果, 结果)

                except Exception as e:
                    self.根窗口.after(0, self.显示错误, str(e))

            threading.Thread(target=执行转录任务, daemon=True).start()

        except Exception as e:
            messagebox.showerror("错误", f"转录失败: {str(e)}")

    def 更新转录结果(self, 结果: str) -> None:
        """更新转录结果到界面"""
        self.转录文本.delete("1.0", tk.END)
        self.转录文本.insert(tk.END, 结果)

    def 显示错误(self, 错误信息: str) -> None:
        """显示错误信息"""
        self.转录文本.delete("1.0", tk.END)
        self.转录文本.insert(tk.END, f"转录失败: {错误信息}")


if __name__ == "__main__":
    应用程序: 竹影 = 竹影()
    应用程序.主窗口()
