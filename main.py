from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock, mainthread
from kivy.utils import platform
import requests
import os
import time

# 替换成你的花生壳上传地址！！！
UPLOAD_URL = "http://11110068lsmp0.vicp.fun/upload"
INTERVAL = 30  # 拍照间隔（秒）

class RemoteMonitorApp(App):
    def build(self):
        self.status_label = Label(text="监控启动中...\n请允许权限", font_size=20)
        self.photo_path = None
        self.init_permissions()
        Clock.schedule_once(self.start_monitor, 2)
        return self.status_label

    def init_permissions(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            from android.storage import app_storage_path
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])
            self.photo_path = os.path.join(app_storage_path(), "monitor_photo.jpg")

    def start_monitor(self, dt):
        self.update_status(f"监控运行中\n下次拍照：{INTERVAL}秒后")
        Clock.schedule_interval(self.take_and_upload_photo, INTERVAL)

    def take_and_upload_photo(self, dt):
        try:
            if platform == "android" and os.path.exists(self.photo_path):
                from android.intent import Intent, FLAG_ACTIVITY_NEW_TASK
                intent = Intent("android.media.action.IMAGE_CAPTURE")
                intent.putExtra("output", self.photo_path)
                intent.setFlags(FLAG_ACTIVITY_NEW_TASK)
                self.android_activity.startActivity(intent)
                time.sleep(2)
            self.upload_photo()
        except Exception as e:
            self.update_status(f"异常：{str(e)[:15]}")

    def upload_photo(self):
        try:
            if not os.path.exists(self.photo_path):
                self.update_status("未拍到照片")
                return
            photo_name = f"monitor_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(self.photo_path, "rb") as f:
                files = {"image": (photo_name, f, "image/jpeg")}
                response = requests.post(UPLOAD_URL, files=files, timeout=15)
            if response.status_code == 200:
                self.update_status(f"上传成功\n下次：{INTERVAL}秒后")
            else:
                self.update_status(f"上传失败：{response.status_code}")
        except Exception as e:
            self.update_status(f"上传异常：{str(e)[:15]}")

    @mainthread
    def update_status(self, text):
        self.status_label.text = text

if __name__ == "__main__":
    RemoteMonitorApp().run()