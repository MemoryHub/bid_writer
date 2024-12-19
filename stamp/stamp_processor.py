import fitz
import os
from .stamp_type import StampType
from .stamp_config import StampConfig
from .electronic_stamper import ElectronicStamper
from .seal_stamper import SealStamper

class StampProcessor:
    """印章处理器主类"""
    
    def __init__(self, config: StampConfig = None):
        self.config = config or StampConfig()
        self.electronic_stamper = ElectronicStamper(self.config)
        self.seal_stamper = SealStamper(self.config)
    
    def process(self, pdf_file: str, stamp_file: str, output_file: str, stamp_type: StampType) -> None:
        """
        处理PDF文件添加印章
        :param pdf_file: 输入PDF文件路径
        :param stamp_file: 印章图片文件路径
        :param output_file: 输出PDF文件路径
        :param stamp_type: 印章类型
        """
        if not isinstance(stamp_type, StampType):
            raise ValueError("stamp_type必须是StampType枚举类型")
            
        temp_output = None  # 临时输出文件路径初始化为None
        
        try:
            pdf_doc = fitz.open(pdf_file)  # 打开输入的PDF文件
            
            # 如果印章类型是骑缝章或同时包含电子章和骑缝章
            if stamp_type in [StampType.BOTH, StampType.SEAL]:
                if stamp_type == StampType.BOTH:
                    # 如果是同时包含电子章和骑缝章，先处理骑缝章并保存临时文件
                    temp_output = output_file.replace('.pdf', '_temp.pdf')  # 生成临时文件名
                    self.seal_stamper.apply_stamp(pdf_doc, stamp_file)  # 应用骑缝章
                    pdf_doc.save(temp_output, garbage=4, deflate=True)  # 保存到临时文件
                    pdf_doc.close()  # 关闭当前PDF文档
                    # 重新打开临时文件以继续处理电子章
                    pdf_doc = fitz.open(temp_output)  # 打开临时文件
                else:
                    # 如果仅处理骑缝章，直接应用骑缝章
                    self.seal_stamper.apply_stamp(pdf_doc, stamp_file)  # 仅应用骑缝章
            
            # 如果印章类型是电子章或同时包含电子章和骑缝章
            if stamp_type in [StampType.BOTH, StampType.STAMP]:
                # 应用电子章
                self.electronic_stamper.apply_stamp(pdf_doc, stamp_file)  # 应用电子章
            
            # 保存最终的PDF文件
            pdf_doc.save(output_file, garbage=4, deflate=True)  # 保存最终输出文件
            pdf_doc.close()  # 关闭PDF文档
            print(f"已成功添加印章，生成文件：{output_file}")
            
        except Exception as e:
            raise Exception(f"处理文件时出错: {str(e)}")
        
        finally:
            if temp_output and os.path.exists(temp_output):
                os.remove(temp_output) 