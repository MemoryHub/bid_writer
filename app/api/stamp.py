from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
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

        # 设定临时文件夹路径
        resources_dir = "resources"  # 确保这个目录在项目中存在
        os.makedirs(resources_dir, exist_ok=True)

        # 使用临时目录
        input_file_path = os.path.join(resources_dir, f"temp_{input_file.filename}")
        stamp_file_path = os.path.join(resources_dir, f"temp_{stamp_file.filename}")

        # 处理文件上传
        with open(input_file_path, "wb") as f:
            f.write(await input_file.read())

        with open(stamp_file_path, "wb") as f:
            f.write(await stamp_file.read())

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(resources_dir, f"{os.path.splitext(input_file.filename)[0]}_stamped_{timestamp}.pdf")

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

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """下载文件"""
    file_path = os.path.join("resources", file_name)  # 确保路径正确
    print(f"Attempting to download file from: {file_path}")  # Debugging line
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件未找到")
    return FileResponse(file_path, media_type='application/pdf', filename=file_name)
