import os
from docx2pdf import convert
from typing import Optional

class FileConverter:
    """文件格式转换器类"""
    
    @staticmethod
    def word_to_pdf(
        input_path: str, 
        output_path: Optional[str] = None,
        overwrite: bool = False
    ) -> str:
        """
        将Word文档转换为PDF格式
        
        Args:
            input_path: Word文档的输入路径
            output_path: PDF文件的输出路径（可选）
            overwrite: 如果输出文件已存在，是否覆盖
            
        Returns:
            str: 转换后的PDF文件路径
            
        Raises:
            FileNotFoundError: 当输入文件不存在时
            ValueError: 当输入文件不是.doc或.docx格式时
            FileExistsError: 当输出文件已存在且overwrite=False时
        """
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
            
        # 检查文件格式
        if not input_path.lower().endswith(('.doc', '.docx')):
            raise ValueError("输入文件必须是.doc或.docx格式")
            
        # 如果未指定输出路径，使用输入文件路径，仅改变扩展名
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + '.pdf'
            
        # 检查输出文件是否已存在
        if os.path.exists(output_path) and not overwrite:
            raise FileExistsError(f"输出文件已存在: {output_path}")
            
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
        # 执行转换
        convert(input_path, output_path)
        
        return output_path
