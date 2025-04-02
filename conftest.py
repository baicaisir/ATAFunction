import pytest
import allure
import os
import time
import subprocess
from airtest.core.api import *
from airtest.report.report import simple_report

from config.config import REPORT_DIR
from common.utils.resource_manager import ResourceManager

# 设置报告目录
report_time = time.strftime('%Y%m%d_%H%M%S')
report_dir = os.path.join(REPORT_DIR, report_time)
ResourceManager.ensure_dir_exists(report_dir)

# 设置allure结果目录
allure_results_dir = os.path.join(report_dir, 'allure-results')
ResourceManager.ensure_dir_exists(allure_results_dir)

# 设置日志目录
log_dir = os.path.join(report_dir, 'logs')
ResourceManager.ensure_dir_exists(log_dir)

# 设置截图目录
screenshot_dir = os.path.join(report_dir, 'screenshots')
ResourceManager.ensure_dir_exists(screenshot_dir)

# 设置airtest日志目录
auto_setup(__file__, logdir=log_dir, devices=[
    "Android:///",  # 使用默认Android设备
])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试执行状态钩子函数
    """
    outcome = yield
    report = outcome.get_result()

    # 获取测试用例的执行阶段
    if report.when == "call":
        # 测试用例执行阶段
        if report.failed:
            # 测试失败，添加截图
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_failed.png")
            snapshot(screenshot_path)
            allure.attach.file(screenshot_path, name="失败截图", attachment_type=allure.attachment_type.PNG)
    elif report.when == "setup":
        # 测试前置条件执行阶段
        if report.failed:
            # 前置条件失败，标记为blocked
            allure.dynamic.label('status', 'blocked')
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_setup_failed.png")
            snapshot(screenshot_path)
            allure.attach.file(screenshot_path, name="前置条件失败截图", attachment_type=allure.attachment_type.PNG)
    elif report.when == "teardown":
        # 测试后置条件执行阶段
        if report.failed:
            # 后置条件失败，添加截图
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_teardown_failed.png")
            snapshot(screenshot_path)
            allure.attach.file(screenshot_path, name="后置条件失败截图", attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    """
    生成测试报告
    """
    yield
    # 测试结束后生成报告
    try:
        # 生成airtest报告
        simple_report(__file__, logpath=log_dir, output=os.path.join(report_dir, 'airtest_report.html'))
        log("生成airtest报告成功:%s" % os.path.join(report_dir, 'airtest_report.html'))

        # 生成allure报告
        # allure_report_dir = os.path.join(report_dir, 'allure-report')
        # ResourceManager.ensure_dir_exists(allure_report_dir)

        # 使用subprocess执行allure命令生成报告
        # subprocess.run(["allure", "generate", allure_results_dir, "-o", allure_report_dir, "--clean"], check=True, shell=True)

        # 打开allure报告
        # subprocess.Popen(["allure", "open", allure_report_dir], shell=True)
    except Exception as e:
        print(f"生成报告失败: {e}")
        raise e
