# Bid Writer (投标工程师助手)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Bid Writer 是一个面向投标工程师的自动化工具集，旨在简化投标文件的准备过程，提高工作效率。

## 功能特性
- 一键电子公章，可选择自动在每页都添加一个单子公章和骑缝章
- 骑缝章支持自定义印章尺寸、数量、每个几页添加
- 支持电子公章自定义印章尺寸、位置
- 支持同时添加电子公章和骑缝章 
- 支持上传word
- 插入图片到特定页??


### 电子公章管理 (Digital Seal Management)
- 支持将电子公章添加到 PDF 文档
- 精确控制公章大小（支持实际物理尺寸，如 4cm 直径）
- 灵活设置公章位置（支持基于右下角的精确定位）
- 保持公章透明度

+ ### 骑缝章功能 (Cross-page Seal)
+ - 支持在PDF文档上添加跨页骑缝章
+ - 支持同时添加电子公章和骑缝章
+ - 支持自定义骑缝章数量和分布
+ 
+ #### 骑缝章配置参数
+ | 参数 | 类型 | 默认值 | 说明 |
+ |------|------|--------|------|
+ | stamp_size_mm | float | 40.0 | 印章尺寸（直径），单位：毫米 |
+ | seal_count | int | 3 | 每组骑缝章的数量 |
+ | pages_per_seal | int | None | 每组骑缝章跨越的页数，None表示使用总页数 |
+ 
+ #### 使用示例
+ ```python
+ from stamp import StampProcessor, StampConfig, StampType
+ 
+ # 创建配置
+ config = StampConfig(
+     stamp_size_mm=40,        # 印章尺寸40mm
+     margin_right_mm=60,      # 电子章距右边距60mm
+     margin_bottom_mm=60,     # 电子章距下边距60mm
+     seal_count=3,            # 每组3个骑缝章
+     pages_per_seal=10        # 每10页一组骑缝章
+ )
+ 
+ # 创建处理器
+ processor = StampProcessor(config)
+ 
+ # 添加骑缝章
+ processor.process(
+     pdf_file="input.pdf",
+     stamp_file="stamp.png",
+     output_file="output.pdf",
+     stamp_type=StampType.SEAL  # 仅添加骑缝章
+ )
+ ```
+ 
+ #### 印章类型选择
+ | 类型 | 说明 |
+ |------|------|
+ | StampType.BOTH | 同时添加电子章和骑缝章 |
+ | StampType.STAMP | 仅添加电子章 |
+ | StampType.SEAL | 仅添加骑缝章 |
+ 
+ #### 注意事项
+ 1. 印章图片建议使用透明背景的PNG格式
+ 2. 建议印章图片分辨率不低于300DPI
+ 3. 骑缝章处理可能会增加输出文件大小
+ 4. 建议在使用前进行测试，确保效果符合预期

## 环境要求

- Python 3.8 或更高版本
- PyMuPDF (fitz)
- Pillow (用于骑缝章图片处理)

## 安装

1. 克隆仓库