import pytest
import allure
from page.weapon.weapon_page import WeaponPage

@allure.epic("武器大师游戏测试")
@allure.feature("首页模块")
class TestHomepage:
    """
    首页模块测试用例
    """
    
    @pytest.fixture(scope="function")
    def setup_teardown(self):
        """
        测试前置和后置条件
        前置：打开游戏，等待进入主页
        后置：退出游戏
        """
        # 前置条件
        weapon_page = WeaponPage()
        weapon_page.start_app()
        weapon_page.wait_for_home_page()
        
        # 返回页面对象给测试用例使用
        yield weapon_page
        
        # 后置条件
        # weapon_page.stop_app()
    
    @allure.story("首页UI测试")
    @allure.title("验证首页开始按钮存在")
    @allure.severity(allure.severity_level.BLOCKER)  # P0级别
    @pytest.mark.smoke  # 冒烟测试标记
    @pytest.mark.homepage  # 首页模块标记
    def test_start_button_exists(self, setup_teardown):
        """
        测试用例：验证首页开始按钮存在
        步骤：
        1. 断言开始按钮存在
        预期结果：
        1. 开始按钮存在
        """
        # 获取页面对象
        weapon_page = setup_teardown
        
        # 添加测试步骤
        with allure.step("验证开始按钮存在"):
            # 断言开始按钮存在，超时时间30秒
            weapon_page.assert_start_button_exists()
            
        # 添加测试结果
        allure.attach("测试通过：首页开始按钮存在", name="测试结果", attachment_type=allure.attachment_type.TEXT)