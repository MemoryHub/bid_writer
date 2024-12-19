from abc import ABC, abstractmethod
import fitz
from .stamp_config import StampConfig

class BaseStamper(ABC):
    """印章处理器基类"""
    
    def __init__(self, config: StampConfig):
        self.config = config
    
    @abstractmethod
    def apply_stamp(self, pdf_doc: fitz.Document, stamp_file: str) -> None:
        """
        应用印章到PDF文档
        :param pdf_doc: PDF文档对象
        :param stamp_file: 印章图片文件路径
        """
        pass 