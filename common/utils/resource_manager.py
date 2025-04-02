import os
from config.config import ROOT_DIR, RESOURCE_DIR, IMAGE_DIR

class ResourceManager:
    """
    资源管理类，按页面分类管理控件、图片资源
    """
    
    @staticmethod
    def get_image_path(page_name, image_name):
        """
        获取图片资源的绝对路径
        :param page_name: 页面名称，如'homepage', 'weapon'
        :param image_name: 图片名称，如'start_button.png'
        :return: 图片的绝对路径
        """
        # 确保图片名称有.png后缀
        if not image_name.endswith('.png'):
            image_name = f"{image_name}.png"
        
        # 构建图片路径
        image_path = os.path.join(IMAGE_DIR, page_name, image_name)
        
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片资源不存在: {image_path}")
        
        return image_path
    
    @staticmethod
    def get_resource_path(resource_type, page_name, resource_name):
        """
        获取资源的绝对路径
        :param resource_type: 资源类型，如'images', 'elements'
        :param page_name: 页面名称
        :param resource_name: 资源名称
        :return: 资源的绝对路径
        """
        resource_path = os.path.join(RESOURCE_DIR, resource_type, page_name, resource_name)
        
        # 检查资源是否存在
        if not os.path.exists(resource_path):
            raise FileNotFoundError(f"资源不存在: {resource_path}")
        
        return resource_path
    
    @staticmethod
    def ensure_dir_exists(dir_path):
        """
        确保目录存在，如果不存在则创建
        :param dir_path: 目录路径
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path