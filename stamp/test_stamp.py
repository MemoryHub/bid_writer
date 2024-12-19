import os
import sys
from pathlib import Path

# 获取项目根目录
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from stamp.stamp_processor import StampProcessor
from stamp.stamp_config import StampConfig
from stamp.stamp_type import StampType
from stamp.image_inserter import ImageInserter

class StampTester:
    """
    印章处理测试类
    用于测试电子印章和骑缝章的各种应用场景
    """
    
    def __init__(self):
        """
        初始化测试类
        创建默认的配置和处理器实例
        """
        # 创建默认配置
        self.config = StampConfig(
            stamp_size_mm=40,      # 印章尺寸40mm
            margin_right_mm=80,    # 距右边距80mm
            margin_bottom_mm=80,   # 距下边距80mm
            seal_count=1           # 每组1个骑缝章
        )
        
        # 创建印章处理器
        self.processor = StampProcessor(self.config)
        
    def test_all_features(self,
                         input_file: str = "resources/lp.pdf",
                         stamp_file: str = "resources/stamp.png",
                         image_file: str = "resources/stamp.png",
                         output_dir: str = "resources") -> None:
        """
        测试所有功能
        
        Args:
            input_file (str): 输入文件路径
            stamp_file (str): 印章图片路径
            image_file (str): 测试用图片路径
            output_dir (str): 输出目录路径
        """
        try:
            # 测试印章功能
            self.test_all_stamp_types(input_file, stamp_file, output_dir)
            
            # 测试图片插入功能
            self.test_image_insertion(
                pdf_file=f"{output_dir}/contract_with_both_stamps.pdf",
                image_file=image_file,
                output_dir=output_dir
            )
            
        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
    
    def test_image_insertion(self,
                           pdf_file: str,
                           image_file: str,
                           output_dir: str) -> None:
        """
        测试图片插入功能
        
        Args:
            pdf_file (str): 输入PDF文件路径
            image_file (str): 要插入的图片文件路径
            output_dir (str): 输出目录路径
        """
        try:
            print("\n开始测试: 图片插入功能")
            
            # 测试使用坐标定位插入图片
            output_file = f"{output_dir}/output_with_image_position.pdf"
            ImageInserter.insert_image(
                pdf_file=pdf_file,
                image_file=image_file,
                output_file=output_file,
                page_number=0,  # 插入到第1页
                position=(50, 50),  # 距左50mm，距上50mm
                size_mm=30  # 图片宽度30mm，等比缩放
            )
            print(f"完成坐标定位插入测试: {output_file}")
            
            # 测试使用边距定位插入图片
            output_file = f"{output_dir}/output_with_image_margin.pdf"
            ImageInserter.insert_image(
                pdf_file=pdf_file,
                image_file=image_file,
                output_file=output_file,
                page_number=1,  # 插入到第2页
                margin_right_mm=30,  # 距右30mm
                margin_bottom_mm=30,  # 距下30mm
                size_mm=(40, 30)  # 图片宽40mm，高30mm
            )
            print(f"完成边距定位插入测试: {output_file}")
            
            print("图片插入测试完成！")
            
        except Exception as e:
            print(f"图片插入测试失败: {str(e)}")
            raise
    
    def test_all_stamp_types(self, 
                            input_file: str,
                            stamp_file: str,
                            output_dir: str) -> None:
        """测试所有印章类型"""
        try:
            # 测试同时添加电子章和骑缝章
            self._test_stamp_type(
                input_file=input_file,
                stamp_file=stamp_file,
                output_file=f"{output_dir}/contract_with_both_stamps.pdf",
                stamp_type=StampType.BOTH,
                description="同时添加电子章和骑缝章"
            )
            
            # 测试只添加电子章
            self._test_stamp_type(
                input_file=input_file,
                stamp_file=stamp_file,
                output_file=f"{output_dir}/contract_with_stamp.pdf",
                stamp_type=StampType.STAMP,
                description="添加电子章"
            )
            
            # 测试只添加骑缝章
            self._test_stamp_type(
                input_file=input_file,
                stamp_file=stamp_file,
                output_file=f"{output_dir}/contract_with_seals.pdf",
                stamp_type=StampType.SEAL,
                description="添加骑缝章"
            )
            
            print("所有印章测试完成！")
            
        except Exception as e:
            print(f"印章测试过程中发生错误: {str(e)}")
            raise

    def _test_stamp_type(self,
                        input_file: str,
                        stamp_file: str,
                        output_file: str,
                        stamp_type: StampType,
                        description: str) -> None:
        """测试特定类型的印章处理"""
        print(f"\n开始测试: {description}")
        try:
            self.processor.process(
                input_file=input_file,
                stamp_file=stamp_file,
                output_file=output_file,
                stamp_type=stamp_type
            )
            print(f"测试完成: {description}")
            print(f"输出文件: {output_file}")
        except Exception as e:
            print(f"测试失败: {description}")
            print(f"错误信息: {str(e)}")
            raise

def main():
    """主函数"""
    try:
        tester = StampTester()
        tester.test_all_features()
    except Exception as e:
        print(f"测试执行失败: {str(e)}")

if __name__ == "__main__":
    main() 