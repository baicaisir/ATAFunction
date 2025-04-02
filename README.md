# ATAFunction 游戏自动化测试框架

基于Python+Airtest+pytest+allure的游戏自动化测试框架，遵循PO模式的最佳实践，将UI元素、页面操作和测试逻辑分离，使得测试用例更加清晰、易于维护。

## 框架特点

1. **设备管理**：支持设备配置，默认使用本地安卓设备
2. **操作封装**：封装基础操作如点击、滑动、图片存在检查等
3. **应用层封装**：封装应用级别操作如启动、关闭应用等
4. **断言封装**：提供控件存在、控件不存在断言，断言失败自动截图
5. **资源管理**：按页面分类管理控件、图片资源，便于维护
6. **日志系统**：复用airtest封装好的日志模块
7. **自动化报告**：使用allure报告，目录按照时间区分避免覆盖

## 目录结构

```
├── common/                 # 公共模块
│   ├── base/              # 基础操作封装
│   │   └── base_page.py   # 基础页面类
│   └── utils/             # 工具类
│       ├── assertion.py   # 断言封装
│       └── resource_manager.py # 资源管理
├── config/                # 配置文件
│   ├── config.py          # 全局配置
│   └── pytest.ini         # pytest配置
├── page/                  # 页面对象
│   └── weapon/            # 武器页面
│       └── weapon_page.py # 武器页面类
├── reports/               # 测试报告
├── resources/             # 资源文件
│   └── images/            # 图片资源
├── test_cases/            # 测试用例
│   └── test_homepage.py   # 首页测试用例
└── conftest.py            # pytest钩子函数
```

## 使用方法

### 环境准备

1. 安装Python 3.7+
2. 安装依赖包：
   ```
   pip install airtest pytest pytest-allure allure-pytest
   ```
3. 安装Allure命令行工具

### 运行测试

```bash
pytest test_cases/ -v
```

### 查看报告

测试执行完成后，会自动打开Allure报告。也可以手动打开：

```bash
allure open reports/[时间戳]/allure-report
```

## 测试用例编写

1. 在`resources/images/`下按页面创建目录，存放页面截图
2. 在`page/`下创建页面类，继承`BasePage`
3. 在`test_cases/`下创建测试用例，使用页面类进行操作

## 示例

```python
# 测试用例示例
def test_start_button_exists(self, setup_teardown):
    # 获取页面对象
    weapon_page = setup_teardown
    
    # 断言开始按钮存在
    weapon_page.assert_start_button_exists()
```