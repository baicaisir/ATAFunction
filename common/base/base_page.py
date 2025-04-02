from airtest.core.api import *
from airtest.core.settings import Settings
from airtest.report.report import simple_report
import os
import time
from config.config import DEFAULT_TIMEOUT, ROOT_DIR, REPORT_DIR
from common.utils.resource_manager import ResourceManager

class BasePage:
    """
    基础页面类，封装基本的操作方法
    """
    
    def __init__(self):
        # 设置默认超时时间
        Settings.FIND_TIMEOUT = DEFAULT_TIMEOUT
        # 设置截图保存路径
        self.screenshot_dir = os.path.join(REPORT_DIR, time.strftime('%Y%m%d_%H%M%S'))
        ResourceManager.ensure_dir_exists(self.screenshot_dir)
    
    def click_image(self, page_name, image_name, timeout=DEFAULT_TIMEOUT, threshold=0.7, rgb=False):
        """
        点击图片
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param threshold: 图像识别相似度阈值，范围0-1，值越大要求匹配度越高
        :param rgb: 是否使用RGB模式进行识别，默认为False使用灰度图识别
        :return: 点击结果
        """
        image_path = ResourceManager.get_image_path(page_name, image_name)
        try:
            return touch(Template(image_path, threshold=threshold, rgb=rgb), timeout=timeout)
        except Exception as e:
            self.take_screenshot(f"click_failed_{image_name}")
            raise e
    
    def swipe_operation(self, start_pos, end_pos, duration=0.5):
        """
        滑动操作
        :param start_pos: 起始位置，如(100, 100)
        :param end_pos: 结束位置，如(100, 500)
        :param duration: 滑动持续时间（秒）
        :return: 滑动结果
        """
        try:
            return swipe(start_pos, end_pos, duration=duration)
        except Exception as e:
            self.take_screenshot("swipe_failed")
            raise e
    
    def image_exists(self, page_name, image_name, timeout=DEFAULT_TIMEOUT, threshold=0.7, rgb=False):
        """
        检查图片是否存在
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param threshold: 图像识别相似度阈值，范围0-1，值越大要求匹配度越高
        :param rgb: 是否使用RGB模式进行识别，默认为False使用灰度图识别
        :return: 图片是否存在
        """
        image_path = ResourceManager.get_image_path(page_name, image_name)
        try:
            # 使用wait函数进行超时判断，如果找到图片则返回位置，否则抛出异常
            pos = wait(Template(image_path, threshold=threshold, rgb=rgb), timeout=timeout)
            return pos is not False
        except Exception:
            return False
    
    def wait_image(self, page_name, image_name, timeout=DEFAULT_TIMEOUT, threshold=0.7, rgb=False):
        """
        等待图片出现
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param threshold: 图像识别相似度阈值，范围0-1，值越大要求匹配度越高
        :param rgb: 是否使用RGB模式进行识别，默认为False使用灰度图识别
        :return: 图片位置
        """
        image_path = ResourceManager.get_image_path(page_name, image_name)
        print("识别文件路径：",image_path)
        try:
            return wait(Template(image_path, threshold=threshold, rgb=rgb), timeout=timeout)
        except Exception as e:
            self.take_screenshot(f"wait_failed_{image_name}")
            raise e
    
    def take_screenshot(self, name=None):
        """
        截图
        :param name: 截图名称，默认为当前时间戳
        :return: 截图路径
        """
        if name is None:
            name = f"screenshot_{int(time.time())}"
        
        screenshot_path = os.path.join(self.screenshot_dir, f"{name}.png")
        snapshot(screenshot_path)
        return screenshot_path
    
    def image_not_exists(self, page_name, image_name, timeout=DEFAULT_TIMEOUT, threshold=0.7, rgb=False):
        """
        检查图片是否不存在
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param threshold: 图像识别相似度阈值，范围0-1，值越大要求匹配度越高
        :param rgb: 是否使用RGB模式进行识别，默认为False使用灰度图识别
        :return: 图片是否不存在
        """
        return not self.image_exists(page_name, image_name, timeout, threshold, rgb)