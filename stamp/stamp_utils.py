class StampUtils:
    """
    印章工具类
    提供印章处理过程中需要的通用工具方法
    """
    
    @staticmethod
    def mm_to_points(mm: float) -> float:
        """
        将毫米转换为PDF点数
        
        PDF中使用点（point）作为基本单位
        转换公式：
        1 英寸 = 25.4 毫米
        1 英寸 = 72 点
        因此 1 毫米 = 72/25.4 点
        
        Args:
            mm (float): 毫米值
            
        Returns:
            float: 对应的点数
            
        示例:
            >>> StampUtils.mm_to_points(25.4)
            72.0
        """
        return mm * 72 / 25.4