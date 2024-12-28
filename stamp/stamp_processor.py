import logging
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
    
    def process(self, input_file: str, stamp_file: str, output_file: str, stamp_type: StampType) -> None:
        """
        处理文件添加印章
        :param input_file: 输入文件路径（支持PDF或Word文档）
        :param stamp_file: 印章图片文件路径
        :param output_file: 输出PDF文件路径
        :param stamp_type: 印章类型
        """
        if not isinstance(stamp_type, StampType):
            raise ValueError("stamp_type必须是StampType枚举类型")
        # 检查输出文件路径是否为空
        # 检查输出文件路径是否为空
        if not output_file:
            raise ValueError("输出文件路径不能为空")
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        # 检查印章文件是否存在
        if not os.path.exists(stamp_file):
            raise FileNotFoundError(f"印章文件不存在: {stamp_file}")
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # 处理Word文档
        temp_pdf = None  
        if input_file.lower().endswith(('.doc', '.docx')):
            from convert.file_converter import FileConverter
            # 创建临时PDF文件路径
            temp_pdf = os.path.join(
                os.path.dirname(output_file),
                f"{os.path.basename(os.path.splitext(input_file)[0])}.pdf"
            )
    
            # 转换为PDF
            pdf_file = FileConverter.word_to_pdf(
                input_path=input_file,
                output_path=temp_pdf,
                overwrite=True
            )
        else:
            pdf_file = input_file
            
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
            # 清理临时文件
            if temp_output and os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                except Exception as e:
                    print(f"警告：清理临时输出文件失败: {str(e)}")
                    
            if temp_pdf and os.path.exists(temp_pdf):
                try:
                    os.remove(temp_pdf)
                except Exception as e:
                    print(f"警告：清理临时PDF文件失败: {str(e)}")