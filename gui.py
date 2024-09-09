import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from bili_scraper import get_all_pages
from cover_downloader import download_covers
from cover_downloader import get_cover_url
from selenium import webdriver

class BiliCoverApp:
    def __init__(self):
        # 初始化带主题的窗口
        self.window = ttk.Window(themename="cosmo")
        self.window.title("BiliCoverDownloader")
        self.window.geometry("1000x700")
        
        # 窗口大小自适应
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=1)
        self.window.columnconfigure(1, weight=1)

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        ## B站用户名和密码输入框
        self.username_label = ttk.Label(self.window, text="B站用户名:", font=("Helvetica", 10))
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self.window, bootstyle="success")
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = ttk.Label(self.window, text="B站密码:", font=("Helvetica", 10))
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self.window, show="*", bootstyle="success")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # 添加提示文案
        self.info_label = ttk.Label(self.window, text="提示: 需要登录B站账户进行人工模拟访问，本应用仅在本地使用，不会上传或搜集您的账户信息。",
                                    font=("Helvetica", 8), foreground="gray")
        self.info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # B站URL输入框
        self.url_label = ttk.Label(self.window, text="B站投稿URL:", font=("Helvetica", 10))
        self.url_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ttk.Entry(self.window, width=40, bootstyle="success")
        self.url_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # 保存路径选择
        self.save_dir_label = ttk.Label(self.window, text="保存路径:", font=("Helvetica", 10))
        self.save_dir_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.save_dir_entry = ttk.Entry(self.window, width=40, bootstyle="success")
        self.save_dir_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.browse_button = ttk.Button(self.window, text="浏览", command=self.browse_directory, bootstyle="primary")
        self.browse_button.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

        # 启动按钮
        self.start_button = ttk.Button(self.window, text="开始", command=self.start_process, bootstyle="success")
        self.start_button.grid(row=5, column=1, pady=20, sticky="ew")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.save_dir_entry.insert(0, directory)
    
    def start_process(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        url = self.url_entry.get()+"?tid=0&keyword=&order=pubdate"
        save_dir = self.save_dir_entry.get()
        
        if not username or not password or not url or not save_dir:
            messagebox.showerror("错误", "请填写所有信息。")
            return

        try:
            driver = webdriver.Chrome()
            video_ids = get_all_pages(driver, url, username, password)
            for video_id in video_ids:
                cover_url = get_cover_url(driver, video_id)
                if cover_url:
                    download_covers(cover_url, video_id, save_dir)
            else:
                print(f"跳过视频ID {video_id}，因为未找到封面链接或页面无法访问。")
            driver.quit() # 关闭驱动
            messagebox.showinfo("成功", "封面下载完成！")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def run(self):
        self.window.mainloop()