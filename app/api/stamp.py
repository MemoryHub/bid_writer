from fastapi import APIRouter, HTTPException, UploadFile, File
from stamp.stamp_processor import StampProcessor
from stamp.stamp_config import StampConfig
from stamp.stamp_type import StampType
import os
import tempfile
from datetime import datetime

router = APIRouter(prefix="/stamp", tags=["stamp"])

@router.post("/smart-stamp")
async def process_stamp(
    input_file: UploadFile = File(...),
    stamp_file: UploadFile = File(...),
    stamp_type: StampType = StampType.BOTH
):
    """处理印章"""
    try:
        # 创建印章处理器
        config = StampConfig(
            stamp_size_mm=40,
            margin_right_mm=60,
            margin_bottom_mm=60,
            seal_count=1
        )
        processor = StampProcessor(config)

        # 使用临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file_path = os.path.join(temp_dir, f"temp_{input_file.filename}")
            stamp_file_path = os.path.join(temp_dir, f"temp_{stamp_file.filename}")

            # 处理文件上传
            with open(input_file_path, "wb") as f:
                f.write(await input_file.read())

            with open(stamp_file_path, "wb") as f:
                f.write(await stamp_file.read())

            # 生成输出文件名，并确保它包含输出目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(temp_dir, f"{os.path.splitext(input_file.filename)[0]}_stamped_{timestamp}.pdf")

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
