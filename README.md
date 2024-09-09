# Bilibili Cover Downloader

## 项目简介
这是一个批量下载 B 站视频封面的工具，提供了简单友好的图形化界面。
你只需输入 B 站用户名、密码、UP 主视频主页链接，以及本地保存的路径
即可自动帮你下载高清原始的B站封面文件
![image](https://github.com/user-attachments/assets/d660a5d4-e00a-4d6b-970d-22d10d577492)



## 安装步骤

1. **克隆项目
git clone https://github.com/yourusername/bilibili-cover-downloader.git
cd bilibili-cover-downloader
   
2. **安装依赖**
使用 pip 安装依赖：pip install -r requirements.txt

3. **安装ChromeDriver**
ChromeDriver是谷歌浏览器模拟真人浏览的自动测试驱动
请前往[下载ChromeDriver](https://chromedriver.chromium.org/downloads)
确保版本和你的Chrome浏览器一致，并将该文件放置到谷歌浏览器的文件夹内，操作如下：
（图片）

3. **运行程序**
执行以下命令启动：python main.py

## 版权和使用说明
- 输入 B 站用户名和密码。
- 输入目标 B 站 UP 主的视频主页链接。
- 选择保存路径。
- 点击“开始下载”按钮，程序会自动获取所有视频封面并保存到指定文件夹。
