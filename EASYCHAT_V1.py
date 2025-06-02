import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import json
import threading
from datetime import datetime
import os
import configparser
import time
from collections import deque
from PIL import Image, ImageTk, ImageDraw
import base64
from io import BytesIO

class EasyChat:
    def __init__(self, root):
        self.root = root
        self.setup_variables()
        self.setup_language_texts()
        self.load_config()
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        self.setup_bindings()
        self.request_timestamps = deque(maxlen=10)
        
        # 添加语言变化监听
        self.language.trace_add("write", self.on_language_change)

    def setup_variables(self):
        """初始化变量"""
        self.api_key = tk.StringVar()
        self.api_url = tk.StringVar(value="https://api.openai.com/v1/chat/completions")
        self.model_name = tk.StringVar(value="gpt-3.5-turbo")
        self.language = tk.StringVar(value="中文")
        self.chat_font_size = tk.IntVar(value=11)  # 对话框字体大小
        self.input_font_size = tk.IntVar(value=11)  # 输入框字体大小
        self.conversation_history = []
        self.is_sending = False
        self.last_request_time = 0
        
    def setup_language_texts(self):
        """设置语言文本映射"""
        self.texts = {
            "中文": {
                "window_title": "EasyChat - AI智能对话助手",
                "settings": "设置",
                "api_settings": "API 设置",
                "api_key": "API 密钥:",
                "api_url": "API 地址:",
                "model_name": "模型名称:",
                "ui_settings": "界面设置",
                "language": "界面语言:",
                "send": "发送消息",
                "clear": "清空",
                "export": "导出",
                "copy": "复制",
                "cut": "剪切",
                "paste": "粘贴",
                "select_all": "全选",
                "test_connection": "测试连接",
                "save": "保存",
                "cancel": "取消",
                "user": "用户",
                "assistant": "助手",
                "system": "系统",
                "ready": "就绪",
                "sending": "正在发送消息...",
                "send_success": "消息发送成功",
                "send_fail": "发送失败",
                "copied": "消息已复制到剪贴板",
                "no_api_key": "请先在设置中配置API密钥",
                "confirm_clear": "确定要清空所有对话记录吗？",
                "cleared": "对话已清空",
                "no_conversation": "没有对话记录可导出",
                "export_title": "导出对话记录",
                "export_success": "对话记录已导出到: ",
                "export_fail": "导出失败: ",
                "settings_saved": "设置已保存",
                "restart_required": "需要重启应用以应用语言更改",
                "connection_success": "API连接测试成功！",
                "connection_fail": "连接失败: ",
                "connection_error": "连接测试失败: ",
                "rate_limit": "请求频率超限，请等待{seconds}秒后重试。",
                "wait_time": "请求过于频繁，请等待 {seconds} 秒...",
                "not_connected": "未连接",
                "connected": "已连接",
                "connection_lost": "连接失败",
                "text_file": "文本文件",
                "all_files": "所有文件",
                "conversation_header": "EasyChat 对话记录",
                "select_avatar": "选择头像",
                "avatar": "用户头像",
                "avatar_updated": "头像更新成功",
                "avatar_error": "头像更新失败",
                "error": "错误",
                "font_settings": "字体设置",
                "chat_font_size": "对话框字体大小:",
                "input_font_size": "输入框字体大小:",
                "font_size_changed": "字体大小已更改",
                "api_error_status": "API请求失败 (状态码: {status_code})",
                "api_error_details": "详细信息：{message}",
                "request_timeout": "请求超时，请检查网络连接",
                "connection_failed": "连接失败，请检查网络或API地址",
                "error_occurred": "发生错误: {error}",
            },
            "English": {
                "window_title": "EasyChat - AI Conversation Assistant",
                "settings": "Settings",
                "api_settings": "API Settings",
                "api_key": "API Key:",
                "api_url": "API URL:",
                "model_name": "Model Name:",
                "ui_settings": "UI Settings",
                "language": "Interface Language:",
                "send": "Send",
                "clear": "Clear",
                "export": "Export",
                "copy": "Copy",
                "cut": "Cut",
                "paste": "Paste",
                "select_all": "Select All",
                "test_connection": "Test Connection",
                "save": "Save",
                "cancel": "Cancel",
                "user": "User",
                "assistant": "Assistant",
                "system": "System",
                "ready": "Ready",
                "sending": "Sending message...",
                "send_success": "Message sent successfully",
                "send_fail": "Send failed",
                "copied": "Message copied to clipboard",
                "no_api_key": "Please configure API key in settings first",
                "confirm_clear": "Are you sure you want to clear all conversations?",
                "cleared": "Conversation cleared",
                "no_conversation": "No conversation to export",
                "export_title": "Export Conversation",
                "export_success": "Conversation exported to: ",
                "export_fail": "Export failed: ",
                "settings_saved": "Settings saved",
                "restart_required": "Restart required to apply language changes",
                "connection_success": "API connection test successful!",
                "connection_fail": "Connection failed: ",
                "connection_error": "Connection test failed: ",
                "rate_limit": "Rate limit exceeded, please wait {seconds} seconds.",
                "wait_time": "Too many requests, please wait {seconds} seconds...",
                "not_connected": "Not Connected",
                "connected": "Connected",
                "connection_lost": "Connection Lost",
                "text_file": "Text File",
                "all_files": "All Files",
                "conversation_header": "EasyChat Conversation Log",
                "select_avatar": "Select Avatar",
                "avatar": "User Avatar",
                "avatar_updated": "Avatar updated successfully",
                "avatar_error": "Failed to update avatar",
                "error": "Error",
                "font_settings": "Font Settings",
                "chat_font_size": "Chat Font Size:",
                "input_font_size": "Input Font Size:",
                "font_size_changed": "Font size changed",
                "api_error_status": "API request failed (Status code: {status_code})",
                "api_error_details": "Details: {message}",
                "request_timeout": "Request timeout, please check your network connection",
                "connection_failed": "Connection failed, please check your network or API URL",
                "error_occurred": "Error occurred: {error}",
            }
        }

    def get_text(self, key):
        """获取当前语言的文本"""
        return self.texts[self.language.get()][key]

    def on_language_change(self, *args):
        """当语言变化时更新界面文本"""
        try:
            # 更新窗口标题
            self.root.title(self.get_text("window_title"))
            
            # 更新工具栏按钮
            if hasattr(self, 'toolbar_frame'):
                for widget in self.toolbar_frame.winfo_children():
                    if isinstance(widget, ttk.Frame):  # tools_frame
                        for btn in widget.winfo_children():
                            if isinstance(btn, ttk.Button):
                                if "⚙" in btn['text']:
                                    btn.configure(text="⚙ " + self.get_text("settings"))
                                elif "📁" in btn['text']:
                                    btn.configure(text="📁 " + self.get_text("export"))
                                elif "🗑" in btn['text']:
                                    btn.configure(text="🗑 " + self.get_text("clear"))
            
            # 更新发送按钮
            if hasattr(self, 'send_button'):
                self.send_button.configure(text=self.get_text("send"))
            
            # 更新状态栏
            if hasattr(self, 'status_label'):
                current_status = self.status_label['text']
                if current_status == "就绪" or current_status == "Ready":
                    self.status_label.configure(text=self.get_text("ready"))
                elif "发送成功" in current_status or "sent successfully" in current_status:
                    self.status_label.configure(text=self.get_text("send_success"))
                elif "发送失败" in current_status or "Send failed" in current_status:
                    self.status_label.configure(text=self.get_text("send_fail"))
            
            # 更新连接状态
            if hasattr(self, 'connection_status'):
                current_conn = self.connection_status['text']
                if "未连接" in current_conn or "Not Connected" in current_conn:
                    self.connection_status.configure(text="● " + self.get_text("not_connected"))
                elif "已连接" in current_conn or "Connected" in current_conn:
                    self.connection_status.configure(text="● " + self.get_text("connected"))
                elif "连接失败" in current_conn or "Connection Lost" in current_conn:
                    self.connection_status.configure(text="● " + self.get_text("connection_lost"))
            
            # 保存当前语言设置
            self.save_config()
            
        except Exception as e:
            print(f"Language update error: {str(e)}")

    def setup_window(self):
        """设置主窗口"""
        self.root.title(self.get_text("window_title"))
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 设置窗口图标和样式
        self.root.configure(bg='#f8f9fa')
        
        # 居中显示窗口
        self.center_window()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_config(self):
        """加载配置文件"""
        self.config = configparser.ConfigParser()
        self.config_file = "easychat_config.ini"
        
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
            if 'API' in self.config:
                self.api_key.set(self.config.get('API', 'key', fallback=''))
                self.api_url.set(self.config.get('API', 'url', fallback='https://api.openai.com/v1/chat/completions'))
                self.model_name.set(self.config.get('API', 'model', fallback='gpt-3.5-turbo'))
            if 'Settings' in self.config:
                self.language.set(self.config.get('Settings', 'language', fallback='中文'))
                self.chat_font_size.set(self.config.getint('Settings', 'chat_font_size', fallback=11))
                self.input_font_size.set(self.config.getint('Settings', 'input_font_size', fallback=11))
                
    def save_config(self):
        """保存配置文件"""
        if 'API' not in self.config:
            self.config.add_section('API')
        if 'Settings' not in self.config:
            self.config.add_section('Settings')
            
        self.config.set('API', 'key', self.api_key.get())
        self.config.set('API', 'url', self.api_url.get())
        self.config.set('API', 'model', self.model_name.get())
        self.config.set('Settings', 'language', self.language.get())
        self.config.set('Settings', 'chat_font_size', str(self.chat_font_size.get()))
        self.config.set('Settings', 'input_font_size', str(self.input_font_size.get()))
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
            
    def create_widgets(self):
        """创建界面组件"""
        # 创建样式
        self.setup_styles()
        
        # 主框架
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        
        # 顶部工具栏
        self.create_toolbar()
        
        # 聊天区域
        self.create_chat_area()
        
        # 输入区域
        self.create_input_area()
        
        # 状态栏
        self.create_status_bar()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 配置主题色彩
        style.configure('Main.TFrame', background='#f0f0f0')  # 更改为微信的灰色背景
        style.configure('Toolbar.TFrame', background='#ffffff', relief='flat')
        style.configure('Chat.TFrame', background='#f0f0f0')
        style.configure('Input.TFrame', background='#f0f0f0')  # 改为与对话框相同的背景色
        
        # 发送按钮样式 - 渐变灰色设计
        style.configure('Send.TButton', 
                       padding=(15, 8),
                       relief='flat',  # 去掉边框
                       borderwidth=0,  # 去掉边框
                       focuscolor='none',
                       width=10,
                       font=('Microsoft YaHei UI', 10, 'bold'),  # 保持粗体
                       background='#e6e6e6',  # 浅灰色背景
                       foreground='#333333')  # 深灰色文字
        style.map('Send.TButton',
                 background=[('active', '#d9d9d9'),  # 鼠标悬停时的颜色
                            ('pressed', '#cccccc')],  # 按下时的颜色
                 foreground=[('active', '#1a1a1a'),
                            ('pressed', '#000000')],
                 relief=[('pressed', 'flat')])  # 保持无边框
                 
        style.configure('Clear.TButton',
                       padding=(15, 8),
                       relief='raised',
                       borderwidth=1,
                       focuscolor='none')
        style.map('Clear.TButton',
                 background=[('active', '#f8f9fa')],
                 relief=[('pressed', 'sunken')])

    def create_toolbar(self):
        """创建顶部工具栏"""
        self.toolbar_frame = ttk.Frame(self.main_frame, style='Toolbar.TFrame', padding="10")
        
        # 左侧Logo
        title_label = ttk.Label(
            self.toolbar_frame, 
            text="EasyChat", 
            font=('Microsoft YaHei UI', 16, 'bold'),
            background='#ffffff',
            foreground='#2c3e50'
        )
        title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # 中间区域（用于模型选择和进度条）
        middle_frame = ttk.Frame(self.toolbar_frame, style='Toolbar.TFrame')
        middle_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 模型选择下拉框
        models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        model_combo = ttk.Combobox(
            middle_frame,
            textvariable=self.model_name,
            values=models,
            state="readonly",
            width=15
        )
        model_combo.pack(side=tk.LEFT, padx=(20, 10))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            middle_frame,
            mode='indeterminate',
            length=100,
            orient=tk.HORIZONTAL
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 20))
        self.progress_bar.pack_forget()  # 初始时隐藏
        
        # 工具按钮框架
        tools_frame = ttk.Frame(self.toolbar_frame, style='Toolbar.TFrame')
        tools_frame.pack(side=tk.RIGHT)
        
        # 设置按钮
        settings_btn = ttk.Button(
            tools_frame, 
            text="⚙ " + self.get_text("settings"), 
            command=self.open_settings,
            style='Clear.TButton'
        )
        settings_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 导出对话按钮
        export_btn = ttk.Button(
            tools_frame, 
            text="📁 " + self.get_text("export"), 
            command=self.export_conversation,
            style='Clear.TButton'
        )
        export_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 清空对话按钮
        clear_btn = ttk.Button(
            tools_frame, 
            text="🗑 " + self.get_text("clear"), 
            command=self.clear_conversation,
            style='Clear.TButton'
        )
        clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_chat_area(self):
        """创建聊天显示区域"""
        self.chat_frame = ttk.Frame(self.main_frame, style='Chat.TFrame', padding="10")
        
        # 创建画布和滚动条
        self.chat_canvas = tk.Canvas(
            self.chat_frame,
            bg='#f0f0f0',
            highlightthickness=0,
            relief='flat'
        )
        self.scrollbar = ttk.Scrollbar(
            self.chat_frame,
            orient="vertical",
            command=self.chat_canvas.yview
        )
        
        # 创建消息容器框架
        self.message_frame = ttk.Frame(
            self.chat_canvas,
            style='Chat.TFrame'
        )
        
        # 配置画布滚动
        self.chat_canvas.configure(yscrollcommand=self.on_scroll_change)
        self.chat_canvas.create_window((0, 0), window=self.message_frame, anchor="nw")
        
        # 布局
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件
        self.message_frame.bind('<Configure>', self.on_frame_configure)
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # 初始化最小滚动位置
        self.min_scroll = 0.0

    def on_scroll_change(self, *args):
        """处理滚动条位置变化"""
        # 确保不会滚动超过顶部
        if float(args[0]) < self.min_scroll:
            self.chat_canvas.yview_moveto(self.min_scroll)
        else:
            self.scrollbar.set(*args)

    def on_mousewheel(self, event):
        """鼠标滚轮事件"""
        if len(self.message_frame.winfo_children()) > 0:
            # 计算新的滚动位置
            delta = -1 * (event.delta / 120)
            current_pos = self.chat_canvas.yview()[0]
            new_pos = current_pos + (delta * 0.05)  # 0.05是滚动步长
            
            # 限制最小滚动位置
            if new_pos >= self.min_scroll:
                self.chat_canvas.yview_scroll(int(delta), "units")

    def on_frame_configure(self, event=None):
        """当消息框架大小改变时，更新画布滚动区域"""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        
        # 计算最小滚动位置（防止滚动超过第一条消息）
        if len(self.message_frame.winfo_children()) > 0:
            canvas_height = self.chat_canvas.winfo_height()
            frame_height = self.message_frame.winfo_height()
            if frame_height > canvas_height:
                self.min_scroll = 0.0
            else:
                self.min_scroll = 0.0
        else:
            self.min_scroll = 0.0

    def on_canvas_configure(self, event):
        """当画布大小改变时，调整消息框架宽度"""
        width = event.width - 4  # 减去一点空间给滚动条
        self.chat_canvas.itemconfig(self.chat_canvas.find_withtag("all")[0], width=width)

    def create_input_area(self):
        """创建输入区域"""
        self.input_frame = ttk.Frame(self.main_frame, style='Input.TFrame', padding=(10, 0, 10, 10))  # 修改padding，顶部不留空
        
        # 创建一个内部框架来容纳输入框和按钮，设置白色背景
        input_content_frame = ttk.Frame(self.input_frame, style='Input.TFrame')  # 使用灰色背景
        input_content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 输入文本框和按钮使用grid布局
        input_content_frame.grid_columnconfigure(0, weight=1)  # 输入框可以水平缩放
        input_content_frame.grid_columnconfigure(1, weight=0)  # 按钮保持固定宽度
        
        # 创建白色背景的容器来包装输入框
        text_container = ttk.Frame(input_content_frame, style='Toolbar.TFrame')  # 白色背景
        text_container.grid(row=0, column=0, sticky="nsew")
        
        # 输入文本框
        self.input_text = tk.Text(
            text_container,  # 放在白色容器中
            height=4,
            wrap=tk.WORD,
            font=('Microsoft YaHei UI', 10),
            bg='#ffffff',
            fg='#2c3e50',
            relief='groove',
            borderwidth=1,
            highlightthickness=1,
            highlightbackground='#e9ecef',
            highlightcolor='#ced4da',
            insertbackground='#007bff'
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)  # 使用pack布局填充容器
        
        # 创建右键菜单
        self.create_context_menu(self.input_text)
        
        # 创建白色背景的容器来包装发送按钮
        button_container = ttk.Frame(input_content_frame, style='Toolbar.TFrame')  # 白色背景
        button_container.grid(row=0, column=1, sticky="ns", padx=(10, 0))  # 保持10像素的间距
        
        # 发送按钮
        self.send_button = ttk.Button(
            button_container,  # 放在白色容器中
            text=self.get_text("send"),
            command=self.send_message,
            style='Send.TButton'
        )
        self.send_button.pack(fill=tk.BOTH, expand=True)  # 使用pack布局填充容器

    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ttk.Frame(self.main_frame, style='Toolbar.TFrame', padding="5")
        
        # 使用grid布局来确保状态栏元素的正确位置
        self.status_frame.grid_columnconfigure(0, weight=1)  # 状态文本可以占据剩余空间
        self.status_frame.grid_columnconfigure(1, weight=0)  # 连接状态固定宽度
        
        self.status_label = ttk.Label(
            self.status_frame,
            text=self.get_text("ready"),
            font=('Microsoft YaHei UI', 9),
            background='#ffffff',
            foreground='#6c757d'
        )
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # 连接状态指示器
        self.connection_status = ttk.Label(
            self.status_frame,
            text="● " + self.get_text("not_connected"),
            font=('Microsoft YaHei UI', 9),
            background='#ffffff',
            foreground='#dc3545'
        )
        self.connection_status.grid(row=0, column=1, sticky="e", padx=(10, 0))

    def setup_layout(self):
        """设置布局"""
        # 主框架使用grid而不是pack，这样可以更好地控制布局
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 工具栏固定高度，不参与缩放
        self.toolbar_frame.grid(row=0, column=0, sticky="ew", padx=1, pady=(0, 1))
        
        # 聊天区域可以自由缩放
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=1, pady=(0, 1))
        
        # 输入区域固定高度，但可以水平缩放
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=1, pady=(0, 1))
        
        # 状态栏固定高度
        self.status_frame.grid(row=3, column=0, sticky="ew", padx=1)

        # 配置main_frame的行权重
        self.main_frame.grid_rowconfigure(1, weight=1)  # 只有聊天区域可以垂直缩放
        self.main_frame.grid_rowconfigure(0, weight=0)  # 工具栏不缩放
        self.main_frame.grid_rowconfigure(2, weight=0)  # 输入区域不缩放
        self.main_frame.grid_rowconfigure(3, weight=0)  # 状态栏不缩放
        self.main_frame.grid_columnconfigure(0, weight=1)  # 所有列都可以水平缩放
        
    def setup_bindings(self):
        """设置事件绑定"""
        # Ctrl+Enter 发送消息
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        # Enter 换行
        self.input_text.bind('<Return>', lambda e: None)
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def send_message(self):
        """发送消息"""
        if self.is_sending:
            return
            
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
            
        if not self.api_key.get():
            messagebox.showerror(self.get_text("error"), self.get_text("no_api_key"))
            self.open_settings()
            return
            
        # 清空输入框
        self.input_text.delete("1.0", tk.END)
        
        # 显示用户消息
        self.add_message("user", message)
        
        # 开始发送
        self.is_sending = True
        self.send_button.configure(state='disabled', text=self.get_text("sending"))
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 20))  # 显示进度条
        self.progress_bar.start()
        self.status_label.configure(text=self.get_text("sending"))
        
        # 在新线程中调用API
        threading.Thread(target=self.call_api, args=(message,), daemon=True).start()
        
    def call_api(self, message):
        """调用AI API"""
        try:
            # 检查请求频率
            current_time = time.time()
            self.request_timestamps.append(current_time)
            
            # 如果在1分钟内的请求数超过3个，则等待
            if len(self.request_timestamps) >= 3:
                time_diff = current_time - self.request_timestamps[0]
                if time_diff < 60:  # 小于60秒
                    wait_time = 60 - time_diff
                    self.root.after(0, lambda: self.status_label.configure(text=self.get_text("wait_time") + str(int(wait_time))))
                    time.sleep(wait_time)

            # 准备请求数据
            self.conversation_history.append({"role": "user", "content": message})
            
            headers = {
                "Authorization": f"Bearer {self.api_key.get()}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model_name.get(),
                "messages": self.conversation_history,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 发送请求
            response = requests.post(
                self.api_url.get(),
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                self.root.after(0, self.on_api_success, assistant_message)
            elif response.status_code == 429:
                error_response = response.json()
                retry_after = int(response.headers.get('Retry-After', 60))
                error_msg = self.get_text("rate_limit").format(seconds=retry_after)
                if 'error' in error_response:
                    error_msg += f"\n{self.get_text('api_error_details').format(message=error_response['error'].get('message', ''))}"
                self.root.after(0, self.on_api_error, error_msg)
            else:
                try:
                    error_response = response.json()
                    error_msg = self.get_text("api_error_status").format(status_code=response.status_code)
                    if 'error' in error_response:
                        error_msg += f"\n{self.get_text('api_error_details').format(message=error_response['error'].get('message', ''))}"
                except:
                    error_msg = self.get_text("api_error_status").format(status_code=response.status_code)
                self.root.after(0, self.on_api_error, error_msg)
                
        except requests.exceptions.Timeout:
            self.root.after(0, self.on_api_error, self.get_text("request_timeout"))
        except requests.exceptions.ConnectionError:
            self.root.after(0, self.on_api_error, self.get_text("connection_failed"))
        except Exception as e:
            self.root.after(0, self.on_api_error, self.get_text("error_occurred").format(error=str(e)))
            
    def on_api_success(self, message):
        """API调用成功"""
        self.add_message("assistant", message)
        self.finish_sending(self.get_text("send_success"))
        self.connection_status.configure(text="● " + self.get_text("connected"), foreground='#28a745')
        
    def on_api_error(self, error_msg):
        """API调用失败"""
        self.add_message("system", f"{self.get_text('error')}: {error_msg}")
        self.finish_sending(self.get_text("send_fail"))
        self.connection_status.configure(text="● " + self.get_text("connection_fail") + self.get_text("connection_lost"), foreground='#dc3545')
        
    def finish_sending(self, status_text):
        """完成发送"""
        self.is_sending = False
        self.send_button.configure(state='normal', text=self.get_text("send"))
        self.progress_bar.stop()
        self.progress_bar.pack_forget()  # 隐藏进度条
        self.status_label.configure(text=status_text)
        
    def add_message(self, sender, message):
        """添加消息到聊天显示区"""
        # 创建消息框架
        msg_container = ttk.Frame(self.message_frame, style='Chat.TFrame')
        msg_container.pack(fill=tk.X, padx=10, pady=5)
        
        # 添加时间戳（如果是新的一组消息）
        timestamp = datetime.now().strftime("%H:%M:%S")
        if not hasattr(self, 'last_message_time') or \
           self.last_message_time is None or \
           (datetime.now() - self.last_message_time).seconds > 300:
            time_label = ttk.Label(
                self.message_frame,
                text=timestamp,
                font=('Microsoft YaHei UI', 8),
                foreground='#999999',
                background='#f0f0f0'
            )
            time_label.pack(pady=(5, 0))
            self.last_message_time = datetime.now()
        
        # 根据发送者决定消息框的样式和位置
        is_user = sender.lower() == "user"
        if is_user:
            msg_container.pack(anchor="e")  # 靠右对齐
            bubble_color = "#95ec69"  # 微信绿色
        else:
            msg_container.pack(anchor="w")  # 靠左对齐
            bubble_color = "#ffffff"  # 白色
        
        # 创建消息气泡
        bubble_frame = tk.Frame(
            msg_container,
            bg=bubble_color,
            relief="flat",
            borderwidth=1
        )
        bubble_frame.pack(side=tk.RIGHT if is_user else tk.LEFT)
        
        # 消息文本
        msg_text = tk.Text(
            bubble_frame,
            wrap=tk.WORD,
            font=('Microsoft YaHei UI', self.chat_font_size.get()),  # 使用配置的字体大小
            bg=bubble_color,
            relief="flat",
            height=1,
            width=1,
            padx=10,
            pady=5
        )
        msg_text.pack(expand=True, fill=tk.BOTH)
        msg_text.insert("1.0", message)
        
        # 计算文本高度
        msg_text.update_idletasks()
        lines = int(msg_text.index('end-1c').split('.')[0])
        text_width = min(len(message) * 10 + 20, 400)  # 限制最大宽度
        msg_text.configure(
            width=text_width // 7,  # 估算字符宽度
            height=lines,
            state='disabled'  # 设置为只读
        )
        
        # 滚动到底部
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def clear_conversation(self):
        """清空对话"""
        if messagebox.askyesno(self.get_text("clear"), self.get_text("confirm_clear")):
            # 清空消息框架
            for widget in self.message_frame.winfo_children():
                widget.destroy()
            self.conversation_history.clear()
            self.last_message_time = None
            self.status_label.configure(text=self.get_text("cleared"))
            
    def export_conversation(self):
        """导出对话记录"""
        if not self.conversation_history:
            messagebox.showinfo(self.get_text("export"), self.get_text("no_conversation"))
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[(self.get_text("text_file"), "*.txt"), (self.get_text("all_files"), "*.*")],
            title=self.get_text("export_title")
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.get_text("conversation_header") + "\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for msg in self.conversation_history:
                        role = self.get_text("user") if msg["role"] == "user" else self.get_text("assistant")
                        f.write(f"{role}: {msg['content']}\n\n")
                        
                messagebox.showinfo(self.get_text("export"), self.get_text("export_success") + filename)
                self.status_label.configure(text=self.get_text("export_success") + filename)
            except Exception as e:
                messagebox.showerror(self.get_text("export"), self.get_text("export_fail") + str(e))
                
    def open_settings(self):
        """打开设置窗口"""
        # 保存当前设置值
        original_settings = {
            'api_key': self.api_key.get(),
            'api_url': self.api_url.get(),
            'model_name': self.model_name.get(),
            'language': self.language.get(),
            'chat_font_size': self.chat_font_size.get(),
            'input_font_size': self.input_font_size.get()
        }

        settings_window = tk.Toplevel(self.root)
        settings_window.title(self.get_text("settings"))
        settings_window.geometry("500x600")  # 增加窗口高度
        settings_window.resizable(False, False)
        settings_window.configure(bg='#f8f9fa')
        
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (250)
        y = (settings_window.winfo_screenheight() // 2) - (300)
        settings_window.geometry(f'500x600+{x}+{y}')
        
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # API设置
        api_frame = ttk.LabelFrame(main_frame, text=self.get_text("api_settings"), padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text=self.get_text("api_key")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key, width=50, show="*")
        api_key_entry.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        ttk.Label(api_frame, text=self.get_text("api_url")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        api_url_entry = ttk.Entry(api_frame, textvariable=self.api_url, width=50)
        api_url_entry.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        ttk.Label(api_frame, text=self.get_text("model_name")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        model_entry = ttk.Entry(api_frame, textvariable=self.model_name, width=50)
        model_entry.grid(row=5, column=0, columnspan=2, sticky=tk.EW)
        
        api_frame.columnconfigure(0, weight=1)

        # 界面设置
        ui_frame = ttk.LabelFrame(main_frame, text=self.get_text("ui_settings"), padding="10")
        ui_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(ui_frame, text=self.get_text("language")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        language_combo = ttk.Combobox(ui_frame, textvariable=self.language, values=["中文", "English"], state="readonly")
        language_combo.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        ui_frame.columnconfigure(0, weight=1)

        # 字体设置
        font_frame = ttk.LabelFrame(main_frame, text=self.get_text("font_settings"), padding="10")
        font_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 对话框字体大小
        ttk.Label(font_frame, text=self.get_text("chat_font_size")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        chat_font_spinbox = ttk.Spinbox(
            font_frame,
            from_=8,
            to=20,
            width=5,
            textvariable=self.chat_font_size
        )
        chat_font_spinbox.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        # 输入框字体大小
        ttk.Label(font_frame, text=self.get_text("input_font_size")).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        input_font_spinbox = ttk.Spinbox(
            font_frame,
            from_=8,
            to=20,
            width=5,
            textvariable=self.input_font_size
        )
        input_font_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        font_frame.columnconfigure(0, weight=1)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        test_btn = ttk.Button(button_frame, text=self.get_text("test_connection"), command=self.test_connection)
        test_btn.pack(side=tk.LEFT)
        
        save_btn = ttk.Button(button_frame, text=self.get_text("save"), 
                             command=lambda: self.save_settings(settings_window))
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 修改取消按钮的功能
        def cancel_settings():
            # 恢复原始设置值
            self.api_key.set(original_settings['api_key'])
            self.api_url.set(original_settings['api_url'])
            self.model_name.set(original_settings['model_name'])
            self.language.set(original_settings['language'])
            self.chat_font_size.set(original_settings['chat_font_size'])
            self.input_font_size.set(original_settings['input_font_size'])
            settings_window.destroy()
            
        cancel_btn = ttk.Button(button_frame, text=self.get_text("cancel"), 
                               command=cancel_settings)
        cancel_btn.pack(side=tk.RIGHT)
        
    def test_connection(self):
        """测试API连接"""
        if not self.api_key.get():
            messagebox.showerror(self.get_text("settings"), self.get_text("no_api_key"))
            return
            
        def test_api():
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key.get()}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.model_name.get(),
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10
                }
                
                response = requests.post(
                    self.api_url.get(),
                    headers=headers,
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.root.after(0, lambda: messagebox.showinfo(self.get_text("test_connection"), 
                                                                 self.get_text("connection_success")))
                    self.root.after(0, lambda: self.connection_status.configure(
                        text="● " + self.get_text("connected"), 
                        foreground='#28a745'))
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        self.get_text("test_connection"), 
                        self.get_text("connection_fail") + str(response.status_code)))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    self.get_text("test_connection"), 
                    self.get_text("connection_error") + str(e)))
                
        threading.Thread(target=test_api, daemon=True).start()
        
    def save_settings(self, window):
        """保存设置"""
        old_language = self.config.get('Settings', 'language', fallback='中文')
        old_chat_font_size = self.config.getint('Settings', 'chat_font_size', fallback=11)
        old_input_font_size = self.config.getint('Settings', 'input_font_size', fallback=11)
        
        self.save_config()
        
        # 如果字体大小改变，应用新的字体设置
        if (old_chat_font_size != self.chat_font_size.get() or 
            old_input_font_size != self.input_font_size.get()):
            self.apply_font_settings()
            messagebox.showinfo(self.get_text("settings"), 
                              self.get_text("font_size_changed"))
        
        # 如果语言改变，提示需要重启
        if self.language.get() != old_language:
            messagebox.showinfo(self.get_text("settings"), 
                              self.get_text("settings_saved") + "\n" + 
                              self.get_text("restart_required"))
        else:
            messagebox.showinfo(self.get_text("settings"), 
                              self.get_text("settings_saved"))
        
        window.destroy()

    def apply_font_settings(self):
        """应用字体设置"""
        # 更新对话框中所有消息的字体大小
        for widget in self.message_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):  # 消息气泡
                        for text_widget in child.winfo_children():
                            if isinstance(text_widget, tk.Text):
                                text_widget.configure(font=('Microsoft YaHei UI', self.chat_font_size.get()))
        
        # 更新输入框字体大小
        self.input_text.configure(font=('Microsoft YaHei UI', self.input_font_size.get()))

    def on_closing(self):
        """窗口关闭事件"""
        self.save_config()
        self.root.destroy()

    def create_context_menu(self, widget):
        """创建右键菜单"""
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label=self.get_text("copy"), command=lambda: widget.event_generate("<<Copy>>"))
        menu.add_command(label=self.get_text("cut"), command=lambda: widget.event_generate("<<Cut>>"))
        menu.add_command(label=self.get_text("paste"), command=lambda: widget.event_generate("<<Paste>>"))
        menu.add_separator()
        menu.add_command(label=self.get_text("select_all"), command=lambda: widget.tag_add("sel", "1.0", "end"))
        
        def show_menu(event):
            if widget.cget('state') == 'disabled':
                menu.entryconfig(self.get_text("cut"), state="disabled")
                menu.entryconfig(self.get_text("paste"), state="disabled")
            else:
                menu.entryconfig(self.get_text("cut"), state="normal")
                menu.entryconfig(self.get_text("paste"), state="normal")
            menu.tk_popup(event.x_root, event.y_root)
            
        widget.bind("<Button-3>", show_menu)

def main():
    """主函数"""
    root = tk.Tk()
    app = EasyChat(root)
    root.mainloop()

if __name__ == "__main__":
    main()
