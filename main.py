import tkinter as tk
from PIL import ImageGrab
import time

class ScreenshotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect = None  # 用来绘制框（矩形的边框）

        # 创建一个全屏的遮罩窗口
        self.overlay = tk.Toplevel(self.root)
        self.overlay.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.overlay.attributes("-alpha", 0.5)  # 设置透明度 0.5（50% 透明度）
        self.overlay.config(bg="black")  # 黑色背景
        self.overlay.attributes("-topmost", True)  # 使遮罩窗口始终在最上层
        self.overlay.bind("<ButtonPress-1>", self.on_mouse_press)
        self.overlay.bind("<B1-Motion>", self.on_mouse_drag)
        self.overlay.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.canvas = tk.Canvas(self.overlay, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()

    def on_mouse_press(self, event):
        # 鼠标按下时记录起始位置
        self.start_x = event.x
        self.start_y = event.y

        # 如果框已经存在，删除它
        if self.rect:
            self.canvas.delete(self.rect)

    def on_mouse_drag(self, event):
        # 鼠标拖动时更新框的大小
        if self.start_x and self.start_y:
            self.end_x = event.x
            self.end_y = event.y
            # 删除旧的框并绘制新的框
            if self.rect:
                self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", width=2)

    def on_mouse_release(self, event):
        # 鼠标释放时完成框选并截图
        self.end_x = event.x
        self.end_y = event.y
        self.capture_screenshot()

    def capture_screenshot(self):
        # 在截图前先关闭遮罩窗口
        self.overlay.withdraw()

        # 计算框选区域的坐标，确保左上和右下坐标正确
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            # 获取遮罩窗口的左上角坐标
            overlay_x = self.overlay.winfo_rootx()
            overlay_y = self.overlay.winfo_rooty()

            # 将框选区域的相对坐标转换为屏幕绝对坐标
            left = overlay_x + min(self.start_x, self.end_x)
            top = overlay_y + min(self.start_y, self.end_y)
            right = overlay_x + max(self.start_x, self.end_x)
            bottom = overlay_y + max(self.start_y, self.end_y)

            # 截图
            region = (left, top, right, bottom)
            screenshot = ImageGrab.grab(bbox=region)
            screenshot.show()
            screenshot.save("screenshot.png")
            print("截图已保存为 screenshot.png")

        # 完成截图后退出程序
        self.root.quit()  # 退出主循环

    def run(self):
        print("请用鼠标框选截图区域，按下鼠标左键开始，拖动框选，释放鼠标左键结束。")

        self.overlay.deiconify()  # 显示遮罩窗口
        self.overlay.mainloop()  # 启动事件循环

if __name__ == "__main__":
    app = ScreenshotApp()
    app.run()
