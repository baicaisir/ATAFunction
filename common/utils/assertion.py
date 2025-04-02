import allure
import os
import time
from airtest.core.api import *
from config.config import REPORT_DIR
from common.utils.resource_manager import ResourceManager

class Assertion:
    """
    断言封装类，提供控件存在、控件不存在断言
    断言失败自动截图
    """
    
    def __init__(self):
        # 设置截图保存路径
        self.screenshot_dir = os.path.join(REPORT_DIR, time.strftime('%Y%m%d_%H%M%S'), 'assertion_screenshots')
        ResourceManager.ensure_dir_exists(self.screenshot_dir)
    
    def _wait_for_condition(self, condition_func, timeout=10, check_interval=0.5, error_handler=None):
        """
        等待条件满足
        :param condition_func: 条件函数，返回True表示条件满足
        :param timeout: 超时时间（秒）
        :param check_interval: 检查间隔（秒）
        :param error_handler: 错误处理函数，用于处理condition_func执行过程中的异常
        :return: 如果条件满足返回True，否则返回False
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result = condition_func()
                if result:
                    return True
            except Exception as e:
                if error_handler:
                    error_handler(e)
            
            # 短暂等待后重试
            time.sleep(check_interval)
        
        return False
    
    def assert_image_exists(self, page_name, image_name, timeout=10, message=None):
        """
        断言图片存在
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param message: 断言失败提示信息
        """
        image_path = ResourceManager.get_image_path(page_name, image_name)
        
        if message is None:
            message = f"断言失败: 图片 {image_name} 在 {page_name} 页面不存在"
        
        try:
            # 定义检查图片是否存在的条件函数
            def check_image_exists():
                pos = exists(Template(image_path))
                if pos:
                    allure.attach(f"断言成功: 图片 {image_name} 在 {page_name} 页面存在", name="断言信息",
                                  attachment_type=allure.attachment_type.TEXT)
                    return True
                return False
            
            # 定义错误处理函数
            def handle_error(e):
                allure.attach(f"检查元素异常: {e}", name="断言信息",
                              attachment_type=allure.attachment_type.TEXT)
            
            # 等待条件满足
            result = self._wait_for_condition(check_image_exists, timeout, 0.5, handle_error)
            if not result:
                # 超时后仍未找到图片，抛出断言错误
                raise AssertionError(message)
            
        except AssertionError as e:
            # 断言失败，截图并添加到报告
            screenshot_path = self._take_screenshot(f"assert_exists_failed_{page_name}_{image_name}")
            allure.attach.file(screenshot_path, name="断言失败截图", attachment_type=allure.attachment_type.PNG)
            allure.attach(message, name="断言信息", attachment_type=allure.attachment_type.TEXT)
            raise e
    
    def assert_image_not_exists(self, page_name, image_name, timeout=3, message=None):
        """
        断言图片不存在
        :param page_name: 页面名称
        :param image_name: 图片名称
        :param timeout: 超时时间（秒）
        :param message: 断言失败提示信息
        """
        image_path = ResourceManager.get_image_path(page_name, image_name)
        
        if message is None:
            message = f"断言失败: 图片 {image_name} 在 {page_name} 页面存在"
        
        try:
            # 定义检查图片是否存在的条件函数
            def check_image_not_exists():
                pos = exists(Template(image_path, threshold=0.7))
                if pos is False:
                    allure.attach(f"断言成功: 图片 {image_name} 在 {page_name} 页面不存在", name="断言信息", 
                                  attachment_type=allure.attachment_type.TEXT)
                    return True
                return False
            
            # 等待条件满足
            result = self._wait_for_condition(check_image_not_exists, timeout, 0.5)
            if not result:
                # 超时后仍找到图片，抛出断言错误
                raise AssertionError(message)
                
        except AssertionError as e:
            # 断言失败，截图并添加到报告
            screenshot_path = self._take_screenshot(f"assert_not_exists_failed_{page_name}_{image_name}")
            allure.attach.file(screenshot_path, name="断言失败截图", attachment_type=allure.attachment_type.PNG)
            allure.attach(message, name="断言信息", attachment_type=allure.attachment_type.TEXT)
            raise e
    
    def _take_screenshot(self, name=None):
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