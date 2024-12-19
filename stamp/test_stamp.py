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
        
    def test_all_stamp_types(self, 
                            input_file: str = "resources/test_word.docx",
                            stamp_file: str = "resources/stamp.png",
                            output_dir: str = "resources") -> None:
        """
        测试所有印章类型的应用
        
        Args:
            input_file (str): 输入PDF文件路径,默认为'resources/test.pdf'
            stamp_file (str): 印章图片文件路径,默认为'resources/stamp.png'
            output_dir (str): 输出目录路径,默认为'resources'
            
        测试内容包括：
        1. 同时添加电子章和骑缝章
        2. 只添加电子章
        3. 只添加骑缝章
        
        每种情况都会生成独立的输出文件
        """
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
            
            print("所有测试完成！")
            
        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
    
    def _test_stamp_type(self,
                        input_file: str,
                        stamp_file: str,
                        output_file: str,
                        stamp_type: StampType,
                        description: str) -> None:
        """
        测试特定类型的印章处理
        
        Args:
            input_file (str): 输入PDF文件路径
            stamp_file (str): 印章图片文件路径
            output_file (str): 输出PDF文件路径
            stamp_type (StampType): 印章类型
            description (str): 测试描述
            
        处理步骤：
        1. 打印开始测试信息
        2. 调用处理器进行印章处理
        3. 打印完成信息
        """
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
    """
    主函数，用于运行印章处理测试
    
    执行步骤：
    1. 创建测试器实例
    2. 运行所有印章类型的测试
    3. 捕获并处理可能的异常
    """
    try:
        tester = StampTester()
        tester.test_all_stamp_types()
    except Exception as e:
        print(f"测试执行失败: {str(e)}")

if __name__ == "__main__":
    main() 