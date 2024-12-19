import fitz
import os
from PIL import Image
import io
from typing import Union, Tuple, Optional
from .stamp_utils import StampUtils

class ImageInserter:
    """图片插入器，用于将图片插入到PDF的指定页面"""

    @staticmethod
    def insert_image(
        pdf_file: str,
        image_file: str,
        output_file: str,
        page_number: int,
        position: Tuple[float, float] = None,
        size_mm: Union[float, Tuple[float, float]] = None,
        margin_right_mm: float = None,
        margin_bottom_mm: float = None
    ) -> None:
        """
        将图片插入到PDF指定页面的指定位置

        Args:
            pdf_file (str): 输入PDF文件路径
            image_file (str): 要插入的图片文件路径
            output_file (str): 输出PDF文件路径
            page_number (int): 要插入的页码（从0开始）
            position (tuple, optional): 插入位置的坐标(x,y)，单位为毫米，以左上角为原点
            size_mm (float or tuple, optional): 图片尺寸，单位为毫米
                                              可以是单个数值（等比缩放）或(宽,高)元组
            margin_right_mm (float, optional): 距右边距，单位为毫米，与position互斥
            margin_bottom_mm (float, optional): 距下边距，单位为毫米，与position互斥
        """
        # 参数检查
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_file}")
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"图片文件不存在: {image_file}")
        if position and (margin_right_mm is not None or margin_bottom_mm is not None):
            raise ValueError("position参数与margin参数不能同时使用")

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        try:
            # 打开PDF文件
            pdf_doc = fitz.open(pdf_file)
            
            # 检查页码是否有效
            if not 0 <= page_number < len(pdf_doc):
                raise ValueError(f"无效的页码: {page_number}，文档共{len(pdf_doc)}页")

            # 获取目标页面
            page = pdf_doc[page_number]
            
            # 打开并处理图片
            with Image.open(image_file) as img:
                # 如果图片不是RGBA模式，转换为RGBA
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 计算图片尺寸
                if size_mm:
                    if isinstance(size_mm, (int, float)):
                        # 等比缩放
                        width_pt = StampUtils.mm_to_points(size_mm)
                        scale = width_pt / img.width
                        height_pt = img.height * scale
                    else:
                        # 指定宽高
                        width_pt = StampUtils.mm_to_points(size_mm[0])
                        height_pt = StampUtils.mm_to_points(size_mm[1])
                else:
                    # 使用原始尺寸
                    width_pt = img.width
                    height_pt = img.height

                # 计算插入位置
                if position:
                    # 使用指定位置
                    x = StampUtils.mm_to_points(position[0])
                    y = StampUtils.mm_to_points(position[1])
                else:
                    # 使用边距定位
                    if margin_right_mm is None:
                        x = 0  # 默认左对齐
                    else:
                        x = page.rect.width - width_pt - StampUtils.mm_to_points(margin_right_mm)
                    
                    if margin_bottom_mm is None:
                        y = 0  # 默认顶部对齐
                    else:
                        y = page.rect.height - height_pt - StampUtils.mm_to_points(margin_bottom_mm)

                # 定义插入区域
                rect = fitz.Rect(x, y, x + width_pt, y + height_pt)

                # 将图片保存到字节流
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                # 将图片插入到PDF
                page.insert_image(rect, stream=img_bytes.getvalue())

            # 保存修改后的PDF
            pdf_doc.save(output_file, garbage=4, deflate=True)
            print(f"已成功将图片插入到第{page_number + 1}页，生成文件：{output_file}")

        except Exception as e:
            raise Exception(f"插入图片时出错: {str(e)}")

        finally:
            if 'pdf_doc' in locals():
                pdf_doc.close() 