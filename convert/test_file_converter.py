from file_converter import FileConverter

def main():
    try:
        # 转换单个文件
        input_file = "resources/1.docx"
        output_file = "resources/1.pdf"
            
        pdf_path = FileConverter.word_to_pdf(
            input_path=input_file,
            output_path=output_file,
            overwrite=True
        )
        print(f"转换成功！PDF文件保存在: {pdf_path}")
        
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main() 