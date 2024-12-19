import fitz
from PIL import Image
import io
from .base_stamper import BaseStamper
from .stamp_utils import StampUtils

class SealStamper(BaseStamper):
    """骑缝章处理器"""
    
    # 两个骑缝章之间的垂直间距（毫米）
    SEAL_VERTICAL_SPACING_MM = 10
    # 距离顶部的起始位置（毫米）
    TOP_MARGIN_MM = 20

    def apply_stamp(self, pdf_doc: fitz.Document, stamp_file: str) -> None:
        # 将印章尺寸从毫米转换为PDF点数
        seal_size_pt = StampUtils.mm_to_points(self.config.stamp_size_mm)
        # 获取PDF文档的总页数
        total_pages = len(pdf_doc)

        if total_pages < 2:
            return  # 单页文档不需要骑缝章

        # 确定每个骑缝章处理的页数
        pages_per_seal = (self.config.pages_per_seal
                         if self.config.pages_per_seal is not None and self.config.pages_per_seal <= total_pages
                         else total_pages)

        # 计算需要多少组骑缝章（考虑重叠页面）
        if pages_per_seal > 1:
            # 计算实际需要的组数，向上取整确保覆盖所有页面
            seal_groups = (total_pages + pages_per_seal - 2) // (pages_per_seal - 1)
        else:
            seal_groups = 1

        # 打开印章图片文件
        with Image.open(stamp_file) as img:
            # 确保图像模式为RGBA以支持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 调整印章图像大小
            img = img.resize((int(seal_size_pt * 2), int(seal_size_pt * 2)), Image.Resampling.LANCZOS)

            # 计算骑缝章垂直间距
            seal_spacing_pt = StampUtils.mm_to_points(self.SEAL_VERTICAL_SPACING_MM)
            top_margin_pt = StampUtils.mm_to_points(self.TOP_MARGIN_MM)

            # 处理每组骑缝章
            for group in range(seal_groups):
                # 计算当前组的起始页和结束页
                # 每组的最后一页会成为下一组的第一页
                start_page = group * (pages_per_seal - 1)
                end_page = min(start_page + pages_per_seal, total_pages)
                pages_in_group = end_page - start_page

                # 如果是最后一组且页数不足，调整页数
                if group == seal_groups - 1:
                    pages_in_group = total_pages - start_page

                # 计算每页的骑缝章宽度
                slice_width = int(seal_size_pt / pages_in_group)

                # 为每个骑缝章组添加指定数量的骑缝章
                for seal_index in range(self.config.seal_count):
                    # 计算基础垂直位置
                    base_y_position = (seal_size_pt * 1.5) * (seal_index + 1)
                    
                    # 根据组号增加垂直偏移，确保新组的骑缝章在上一组下方
                    raw_y_position = base_y_position + (group * (seal_size_pt + seal_spacing_pt))

                    # 获取第一页的高度作为参考
                    page_height = pdf_doc[0].rect.height
                    
                    # 如果位置超出页面底部，重新从顶部开始计算
                    if raw_y_position + seal_size_pt > page_height:
                        # 计算需要回到顶部的次数
                        cycles = int(raw_y_position / (page_height - seal_size_pt - top_margin_pt))
                        # 计算实际的Y位置
                        y_position = top_margin_pt + (raw_y_position - cycles * (page_height - seal_size_pt - top_margin_pt))
                    else:
                        y_position = raw_y_position

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