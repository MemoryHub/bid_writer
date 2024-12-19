import fitz  # PyMuPDF

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

# 示例用法
if __name__ == "__main__":
    pdf_file = "resources/test.pdf"       # 输入 PDF 文件路径
    stamp_file = "resources/stamp.png"        # 公章图片路径
    output_file = "resources/contract_with_stamp.pdf"  # 输出 PDF 文件路径
    
    # 设置公章到右下角的边距（单位：毫米）
    margin_right_mm = 80    # 距离右边界20毫米
    margin_bottom_mm = 80   # 距离下边界20毫米
    
    # 公章直径为40毫米（4厘米）
    stamp_size_mm = 40

    add_stamp_to_pdf(
        pdf_file, 
        stamp_file, 
        output_file, 
        margin_right_mm=margin_right_mm,
        margin_bottom_mm=margin_bottom_mm,
        stamp_size_mm=stamp_size_mm
    )
