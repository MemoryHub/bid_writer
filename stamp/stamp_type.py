from enum import Enum

class StampType(Enum):
    """
    印章类型枚举类
    
    定义了三种印章处理类型：
    - BOTH: 同时使用电子章和骑缝章
    - STAMP: 仅使用电子章
    - SEAL: 仅使用骑缝章
    
    使用枚举确保类型选择的安全性和代码的可维护性
    """
    BOTH = "both"     # 同时使用电子章和骑缝章
    STAMP = "stamp"   # 仅使用电子章
    SEAL = "seal"     # 仅使用骑缝章