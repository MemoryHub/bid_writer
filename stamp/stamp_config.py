from dataclasses import dataclass

@dataclass
class StampConfig:
    """
    印章配置数据类
    
    使用@dataclass装饰器自动生成初始化方法、repr等基本方法
    
    属性:
        stamp_size_mm (float): 印章尺寸（直径），单位毫米，默认40mm
        margin_right_mm (float): 电子章距右边距，单位毫米，默认60mm
        margin_bottom_mm (float): 电子章距下边距，单位毫米，默认60mm
        seal_count (int): 骑缝章数量，默认3个
        pages_per_seal (int): 每个骑缝章跨越的页数，默认None（使用总页数）
    """
    stamp_size_mm: float = 40.0        # 印章尺寸（直径），单位毫米
    margin_right_mm: float = 60.0      # 电子章距右边距，单位毫米
    margin_bottom_mm: float = 60.0     # 电子章距下边距，单位毫米
    seal_count: int = 1                # 骑缝章数量
    pages_per_seal: int = 12         # 每个骑缝章跨越的页数

    def __post_init__(self):
        """
        数据验证方法
        在对象创建后自动调用，验证配置参数的有效性
        
        验证规则:
        1. 印章尺寸必须大于0
        2. 边距不能为负数
        3. 骑缝章数量必须大于0
        4. 如果指定了跨页数，必须大于0
        
        Raises:
            ValueError: 当任何参数不满足要求时抛出
        """
        if self.stamp_size_mm <= 0:
            raise ValueError("印章尺寸必须大于0")
        if self.margin_right_mm < 0:
            raise ValueError("右边距不能为负数")
        if self.margin_bottom_mm < 0:
            raise ValueError("下边距不能为负数")
        if self.seal_count <= 0:
            raise ValueError("骑缝章数量必须大于0")
        if self.pages_per_seal is not None and self.pages_per_seal <= 0:
            raise ValueError("每个骑缝章跨越的页数必须大于0") 