import os

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 资源目录
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
IMAGE_DIR = os.path.join(RESOURCE_DIR, 'images')

# 报告目录
REPORT_DIR = os.path.join(ROOT_DIR, 'reports')

# 设备配置
DEVICE_CONFIG = {
    'platform': 'Android',
    'device_id': None,  # None表示使用默认设备
    'package_name': 'com.game.android.weaponmaster',  # 游戏包名
    'activity_name': '.MainActivity'  # 主活动名
}

# 超时设置
DEFAULT_TIMEOUT = 10  # 默认超时时间（秒）
LONG_TIMEOUT = 30     # 长超时时间（秒）