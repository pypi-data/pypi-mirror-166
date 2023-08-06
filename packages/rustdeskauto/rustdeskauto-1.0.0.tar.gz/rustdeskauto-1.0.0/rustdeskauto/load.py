# -*- coding: utf-8 -*-
# '''打开软件，自动链接'''
# '''使用方法：python3 main.py'''
# 将主程序与rustdesk放在同一目录下
# 初始化类会自动打开软件
# api:
# 改变标题：change_title(hwnd, title):
# 自动远程：input_account('id', '密码',title)
# 获取该远程信息:file_info('id'):
# 提交数据: submit_data()/提交数据会自动获取远程信息并且提交,该函数必须在第一次远程之后使用/






import time
import pyautogui
import pywinauto
import requests
import win32gui
import os




# 远程类
class Remote:
    # 初始化
    # 阻塞运行
    def __init__(self, gongsi, shouhou):
        # 远程开始时间结束时间
        self.account = None
        self.start_time = 0
        self.end_time = 0
        self.gongsi = gongsi
        self.shouhou = shouhou
        # 脚本运行间隔
        # pyautogui.PAUSE = 0.5
        # 静默启动软件
        self.app = pywinauto.Application(backend='uia')
        # 通过句柄绑定
        # 判断同级目录是否存在RustDesk.exe
        if os.path.exists("RustDesk.exe"):
            self.app.start('RustDesk')
        if os.path.exists("bent.exe"):
            self.app.start('bent')
        #       获取最顶层窗口
        self.main_window = self.app.top_window()
        self.main_window.wait('visible')
        # 最小化窗口
        self.main_window.minimize()

        self.hwnd = win32gui.FindWindow('H-SMILE-FRAME', None)
        # 开启保护模式
        pyautogui.FAILSAFE = True
        # 改变窗口标题
        self.change_title(self.hwnd, '奔腾电脑远程售后')

    # 改变窗口标题
    def change_title(self, hwnd, title):
        time.sleep(0.1)
        win32gui.SetWindowText(hwnd, title)

    # 获取该远程信息
    # @param title account账号
    # @return 返回远程信息
    # @param account 账号
    # @param password 密码
    # @param name 远程机器备注
    def file_info(self, title):
        #     读取当前用户目录下AppData\Roaming\RustDesk\config\peers的文件内容
        file_path = os.path.expanduser('~') + "\AppData\Roaming\RustDesk\config\peers" + "\\" + title + '.toml'
        #     如果文件存在，则读取文件内容
        if os.path.exists(file_path):
            # utf-8编码读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                # 获取文件内容
                content = f.read()
                # 查找指定字符串
                alias = self.find_str(content, "alias = '")
                username = self.find_str(content, "username = '")
                hostname = self.find_str(content, "hostname = '")
            return {'name': alias, 'username': username, 'hostname': hostname}
        else:
            return None

    # 查找指定字符串
    def find_str(self, content, str):
        start = content.find(str)
        if start == -1:
            return ''
        end = content.find("'", start + len(str))
        # 获取指定字符串
        alias = content[start + len(str):end]
        return alias

    # 上传数据
    def upload_data(self,data):
        #     发送get请求
        url = 'https://4bd6b408-e7ec-438f-83d2-8cba6cc6b874.bspapp.com/add/add?name=' + data['name'] + '&username=' + \
              data['username'] + '&hostname=' + data['hostname'] + '&time=' + str(data['time']) + '&start_time=' + str(
            data['start_time']) + '&end_time=' + str(data['end_time']) + '&my_hostname=' + data['my_hostname']+'&gongsi='+data['gongsi']+'&shouhou='+data['shouhou']
        requests.get(url)

    # 提交数据
    def submit_data(self):
        try:
            data = self.file_info(self.account)
            if data is not None:
                data['start_time'] = int(self.start_time)
                data['end_time'] = int(time.time())
                data['time'] = int(data['end_time'] - data['start_time'])
                # 获取结束时间
                hostname = os.popen('hostname').read()
                data['my_hostname'] = hostname[:-1]
                data['gongsi'] = self.gongsi
                data['shouhou'] = self.shouhou
                print(data)
                # 上传数据
                self.upload_data(data)
        except:
            print('提交数据失败')
            return False

    # 结束
    def end_remote(self):
        # 如果窗口存在，则关闭窗口
        if self.main_window.exists():
            self.main_window.close()
            self.app.kill()

    # 自动远程
    def input_account(self, account, password, title):
        # 窗口重新获取焦点
        hwnd = win32gui.FindWindow('H-SMILE-FRAME', None)
        win32gui.SetForegroundWindow(hwnd)

        # 按两次tap
        pyautogui.press('tab')
        win32gui.SetForegroundWindow(hwnd)
        pyautogui.press('tab')
        win32gui.SetForegroundWindow(hwnd)
        pyautogui.typewrite(account)
        win32gui.SetForegroundWindow(hwnd)
        # 回车
        pyautogui.press('enter')
        # 等带输入框出现
        while True:
            # 获取account窗口
            account_hwnd = win32gui.FindWindow('H-SMILE-FRAME', account)
            if account_hwnd != 0:
                # 等带编辑框组件加载完成
                self.main_window.minimize()
                while True:
                    # 如果该控件存在
                    if self.app.connect(handle=account_hwnd).top_window().child_window(title="取消", control_type="Button").exists():
                        # 设置该窗口的title
                        self.change_title(account_hwnd, title)
                        time.sleep(0.3)
                        win32gui.SetForegroundWindow(account_hwnd)
                        pyautogui.typewrite(password)
                        win32gui.SetForegroundWindow(account_hwnd)
                        pyautogui.press('enter')
                        pyautogui.press('enter')
                        # 最小化窗口
                        self.main_window.minimize()
                        if self.start_time == 0:
                            self.account = account
                            self.start_time = time.time()
                        # 点击确认
                        return 1
                        break
                    else:
                #         判断是否超过1分钟
                        if time.time() - self.start_time > 60:

                            return 2
                            break

                break

# if __name__ == '__main__':
    # Remote = Remote('123')
    # # Remote.input_account('1078258647', 'iwvwhi','asdfa')
    # print(Remote.file_info('1078258647'))
