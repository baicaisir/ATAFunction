from common.base.base_page import BasePage
from common.utils.assertion import Assertion
from config.config import DEVICE_CONFIG, LONG_TIMEOUT
from airtest.core.api import *
import time

class WeaponPage(BasePage):
    """
    武器页面类，封装武器页面的操作
    """
    
    def __init__(self):
        super().__init__()
        self.assertion = Assertion()
        self.page_name = "weapon"  # 页面名称，用于资源管理
    
    def start_app(self):
        """
        启动应用
        """
        package_name = DEVICE_CONFIG['package_name']
        activity_name = DEVICE_CONFIG['activity_name']
        full_activity = f"{package_name}{activity_name}"
        
        try:
            # 启动应用
            start_app(package_name)
            self.take_screenshot("app_started")
            return True
        except Exception as e:
            self.take_screenshot("start_app_failed")
            raise Exception(f"启动应用失败: {e}")
    
    def stop_app(self):
        """
        关闭应用
        """
        package_name = DEVICE_CONFIG['package_name']
        
        try:
            # 关闭应用
            stop_app(package_name)
            return True
        except Exception as e:
            self.take_screenshot("stop_app_failed")
            raise Exception(f"关闭应用失败: {e}")
    
    def wait_for_home_page(self, timeout=LONG_TIMEOUT):
        """
        等待进入主页
        :param timeout: 超时时间（秒）
        :return: 是否成功进入主页
        """
        try:
            # 等待开始按钮出现，表示已进入主页
            print("查看查找是否正确")
            return self.wait_image(self.page_name, "start_button", timeout=timeout)
        except Exception as e:
            self.take_screenshot("wait_home_page_failed")
            raise Exception(f"等待进入主页失败: {e}")
    
    def click_start_button(self):
        """
        点击开始按钮
        :return: 点击结果
        """
        try:
            return self.click_image(self.page_name, "start_button")
        except Exception as e:
            self.take_screenshot("click_start_button_failed")
            raise Exception(f"点击开始按钮失败: {e}")
    
    def assert_start_button_exists(self, timeout=LONG_TIMEOUT):
        """
        断言开始按钮存在
        :param timeout: 超时时间（秒）
        """
        self.assertion.assert_image_exists(self.page_name, "start_button", timeout=timeout)
    
    def assert_start_button_not_exists(self):
        """
        断言开始按钮不存在
        """
        self.assertion.assert_image_not_exists(self.page_name, "start_button")