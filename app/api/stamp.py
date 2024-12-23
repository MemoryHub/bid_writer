from fastapi import APIRouter, HTTPException, UploadFile, File
from stamp.stamp_processor import StampProcessor
from stamp.stamp_config import StampConfig
from stamp.stamp_type import StampType
import os

router = APIRouter(prefix="/stamp", tags=["stamp"])

@router.post("/smart-stamp")
async def process_stamp(
    input_file: UploadFile = File(...),
    stamp_file: UploadFile = File(...),
    output_file: str = "output.pdf",
    stamp_type: StampType = StampType.BOTH
):
    """处理印章"""
    try:
        # 创建印章处理器
        config = StampConfig(
            stamp_size_mm=40,  # 示例配置
            margin_right_mm=60,
            margin_bottom_mm=60,
            seal_count=1
        )
        processor = StampProcessor(config)

        # 将上传的文件保存到临时位置
        input_file_path = f"temp_{input_file.filename}"
        stamp_file_path = f"temp_{stamp_file.filename}"

        with open(input_file_path, "wb") as f:
            f.write(await input_file.read())

        with open(stamp_file_path, "wb") as f:
            f.write(await stamp_file.read())

        # 调用处理方法
        processor.process(
            input_file=input_file_path,
            stamp_file=stamp_file_path,
            output_file=output_file,
            stamp_type=stamp_type
        )

        return {"message": "印章处理成功", "output_file": output_file}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
        if os.path.exists(stamp_file_path):
            os.remove(stamp_file_path)
