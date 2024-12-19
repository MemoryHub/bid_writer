import fitz
from .base_stamper import BaseStamper
from .stamp_utils import StampUtils

class ElectronicStamper(BaseStamper):
    """电子章处理器"""
    
    def apply_stamp(self, pdf_doc: fitz.Document, stamp_file: str) -> None:
        stamp_size_pt = StampUtils.mm_to_points(self.config.stamp_size_mm)
        margin_right_pt = StampUtils.mm_to_points(self.config.margin_right_mm)
        margin_bottom_pt = StampUtils.mm_to_points(self.config.margin_bottom_mm)
        
        for page in pdf_doc:
            page_rect = page.rect
            
            # 计算印章位置
            x = page_rect.width - margin_right_pt - stamp_size_pt
            y = page_rect.height - margin_bottom_pt - stamp_size_pt
            
            # 创建印章区域
            rect = fitz.Rect(x, y, x + stamp_size_pt, y + stamp_size_pt)
            
            # 插入印章
            page.insert_image(rect, filename=stamp_file) 