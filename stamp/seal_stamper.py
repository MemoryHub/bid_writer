import fitz
from PIL import Image
import io
from .base_stamper import BaseStamper
from .stamp_utils import StampUtils

class SealStamper(BaseStamper):
    """骑缝章处理器"""

    def apply_stamp(self, pdf_doc: fitz.Document, stamp_file: str) -> None:
        # 将印章尺寸从毫米转换为PDF点数
        seal_size_pt = StampUtils.mm_to_points(self.config.stamp_size_mm)
        # 获取PDF文档的总页数
        total_pages = len(pdf_doc)

        # 确定每个骑缝章处理的页数
        pages_per_seal = (self.config.pages_per_seal
                          if self.config.pages_per_seal is not None and self.config.pages_per_seal <= total_pages
                          else total_pages)

        # 计算需要多少组骑缝章
        seal_groups = (total_pages + pages_per_seal - 1) // pages_per_seal

        # 打开印章图片文件
        with Image.open(stamp_file) as img:
            # 确保图像模式为RGBA以支持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 调整印章图像大小
            img = img.resize((int(seal_size_pt * 2), int(seal_size_pt * 2)), Image.Resampling.LANCZOS)

            # 处理每组骑缝章
            for group in range(seal_groups):
                # 计算当前组的起始页和结束页
                start_page = group * pages_per_seal
                end_page = min(start_page + pages_per_seal, total_pages)
                pages_in_group = end_page - start_page

                # 计算每页的骑缝章宽度
                slice_width = int(seal_size_pt / pages_in_group)

                # 为每个骑缝章组添加指定数量的骑缝章
                for seal_index in range(self.config.seal_count):
                    # 计算骑缝章在页面上的垂直位置
                    y_position = (seal_size_pt * 1.5) * (seal_index + 1)

                    # 在每页上应用骑缝章
                    for page_index in range(start_page, end_page):
                        page = pdf_doc[page_index]
                        page_rect = page.rect

                        # 计算当前页在组中的相对索引
                        relative_index = page_index - start_page
                        # 计算图像切片的左右边界
                        left = int(relative_index * img.width / pages_in_group)
                        right = int((relative_index + 1) * img.width / pages_in_group)

                        # 裁剪图像以适应当前页
                        slice_img = img.crop((left, 0, right, img.height))

                        # 将裁剪后的图像保存到字节流中
                        img_bytes = io.BytesIO()
                        slice_img.save(img_bytes, format='PNG', optimize=True, quality=95)
                        img_bytes.seek(0)

                        # 计算图像在页面上的位置
                        x = page_rect.width - slice_width
                        y = y_position - (seal_size_pt / 2)

                        # 定义图像插入的矩形区域
                        rect = fitz.Rect(x, y, x + slice_width, y + seal_size_pt)

                        # 在页面上插入图像
                        page.insert_image(rect, stream=img_bytes.getvalue())