import fitz  # PyMuPDF
from PIL import Image
import io

def mm_to_points(mm):
    """将毫米转换为PDF点数
    1 英寸 = 25.4 毫米
    1 英寸 = 72 点
    因此 1 毫米 = 72/25.4 点
    """
    return mm * 72 / 25.4

def add_stamp_to_pdf(pdf_file, stamp_file, output_file, margin_right_mm=60, margin_bottom_mm=60, stamp_size_mm=40):
    """
    在 PDF 上添加电子公章
    :param pdf_file: 原始 PDF 文件路径
    :param stamp_file: 公章图片路径（建议 PNG，带透明背景）
    :param output_file: 输出的 PDF 文件路径
    :param margin_right_mm: 距离右边界的距离（毫米）
    :param margin_bottom_mm: 距离下边界的距离（毫米）
    :param stamp_size_mm: 公章直径，单位为毫米，默认40mm（4cm）
    """
    # 将毫米转换为点数
    stamp_size_pt = mm_to_points(stamp_size_mm)
    margin_right_pt = mm_to_points(margin_right_mm)
    margin_bottom_pt = mm_to_points(margin_bottom_mm)
    
    # 打开 PDF 文件
    pdf = fitz.open(pdf_file)

    # 打开公章图片
    stamp = fitz.open(stamp_file)
    
    # 遍历 PDF 的每一页
    for page in pdf:
        # 获取页面尺寸
        page_rect = page.rect
        
        # 计算公章位置（从右下角往左上偏移）
        x = page_rect.width - margin_right_pt - stamp_size_pt  # 从右边界往左偏移
        y = page_rect.height - margin_bottom_pt - stamp_size_pt  # 从下边界往上偏移
        
        # 创建一个正方形区域，宽高都是stamp_size_pt
        rect = fitz.Rect(x, y, x + stamp_size_pt, y + stamp_size_pt)
        
        # 插入图片
        page.insert_image(
            rect,  # 指定图片位置和大小的矩形
            filename=stamp_file  # 直接使用文件路径
        )

    # 保存修改后的 PDF 文件
    pdf.save(output_file)
    pdf.close()
    stamp.close()
    print(f"已成功添加公章，生成文件：{output_file}")

def add_seal_to_pdf(pdf_file, seal_file, output_file, seal_count=3, seal_size_mm=40, pages_per_seal=None):
    """
    在 PDF 文件上添加骑缝章
    :param pdf_file: 原始 PDF 文件路径
    :param seal_file: 骑缝章图片路径（建议 PNG，带透明背景）
    :param output_file: 输出的 PDF 文件路径
    :param seal_count: 每组骑缝章数量，默认为3个
    :param seal_size_mm: 骑缝章尺寸（直径），单位为毫米，默认40mm
    :param pages_per_seal: 每个骑缝章跨越的页数，默认为None（使用总页数）
    """
    # 将毫米转换为点数
    seal_size_pt = mm_to_points(seal_size_mm)
    
    # 打开 PDF 文件
    pdf = fitz.open(pdf_file)
    total_pages = len(pdf)  # PDF 总页数
    
    # 处理 pages_per_seal 参数
    if pages_per_seal is None or pages_per_seal > total_pages:
        pages_per_seal = total_pages
    
    # 计算需要多少组骑缝章（向上取整）
    seal_groups = (total_pages + pages_per_seal - 1) // pages_per_seal

    # 使用 PIL 打开并处理图章图片
    with Image.open(seal_file) as img:
        # 确保图片是 RGBA 模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 调整图片大小为指定尺寸（使用高质量的重采样方法）
        img = img.resize((int(seal_size_pt * 2), int(seal_size_pt * 2)), Image.Resampling.LANCZOS)
        
        # 处理每组骑缝章
        for group in range(seal_groups):
            # 计算当前组的起始和结束页
            start_page = group * pages_per_seal
            end_page = min(start_page + pages_per_seal, total_pages)
            pages_in_group = end_page - start_page
            
            # 计算每页显示的宽度
            slice_width = int(seal_size_pt / pages_in_group)
            
            # 在每组中添加指定数量的骑缝章
            for seal_index in range(seal_count):
                # 计算当前骑缝章的垂直位置
                y_position = (seal_size_pt * 1.5) * (seal_index + 1)  # 1.5作为间距系数
                
                # 处理当前组的每一页
                for page_index in range(start_page, end_page):
                    page = pdf[page_index]
                    page_rect = page.rect
                    
                    # 计算当前页应显示的图片切片
                    relative_index = page_index - start_page
                    left = int(relative_index * img.width / pages_in_group)
                    right = int((relative_index + 1) * img.width / pages_in_group)
                    
                    # 裁剪图片获取当前页的部分
                    slice_img = img.crop((left, 0, right, img.height))
                    
                    # 将图片转换为字节流（使用高质量压缩）
                    img_bytes = io.BytesIO()
                    slice_img.save(img_bytes, format='PNG', optimize=True, quality=95)
                    img_bytes.seek(0)
                    
                    # 计算插入位置
                    x = page_rect.width - slice_width  # 靠右边缘
                    y = y_position - (seal_size_pt / 2)  # 垂直居中
                    
                    # 创建显示区域
                    rect = fitz.Rect(x, y, x + slice_width, y + seal_size_pt)
                    
                    # 插入图片切片
                    page.insert_image(
                        rect,
                        stream=img_bytes.getvalue()
                    )

    # 保存修改后的 PDF 文件
    try:
        pdf.save(output_file, garbage=4, deflate=True)  # 使用更好的压缩选项
        print(f"已成功添加骑缝章，共 {seal_groups} 组，每组 {seal_count} 个，生成文件：{output_file}")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")
    finally:
        pdf.close()

# 示例用法
if __name__ == "__main__":
    pdf_file = "resources/test.pdf"       # 输入 PDF 文件路径
    stamp_file = "resources/stamp.png"        # 公章图片路径
    output_file = "resources/contract_with_seals.pdf"  # 输出 PDF 文件路径
    
    try:
        # 添加骑缝章
        add_seal_to_pdf(
            pdf_file=pdf_file,
            seal_file=stamp_file,
            output_file=output_file,
            seal_count=3,        # 添加3个骑缝章
            seal_size_mm=40      # 骑缝章直径40mm
        )
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
