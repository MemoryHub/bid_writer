from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from stamp.stamp_processor import StampProcessor
from stamp.stamp_config import StampConfig
from stamp.stamp_type import StampType
import os
from datetime import datetime, timedelta
import threading
from app.core.security import current_active_user
from app.services.stamp_service import upload_stamp_images, delete_stamp_images, get_all_stamp_images
from app.core.security import current_active_user
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session  # 使用异步会话
from app.core.config import settings  # 导入配置
from app.models.response import ResponseModel  # Import the response model

router = APIRouter(prefix="/stamp", tags=["stamp"])

# 临时文件存储路径
resources_dir = "resources"  # 确保这个目录在项目中存在
os.makedirs(resources_dir, exist_ok=True)

# 清理过期临时文件的函数
def clean_temp_files():
    now = datetime.now()
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        # 检查文件是否是临时文件
        if filename.startswith("temp_"):
            # 获取文件的创建时间
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            # 如果文件创建时间超过半小时，则删除
            if now - file_creation_time > timedelta(minutes=30):
                try:
                    os.remove(file_path)
                    print(f"Deleted expired temporary file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {str(e)}")

# 启动清理线程
def start_cleaning_thread():
    threading.Timer(60, start_cleaning_thread).start()  # 每60秒调用一次
    clean_temp_files()

# 启动清理线程
start_cleaning_thread()

@router.post("/smart-stamp", response_model=ResponseModel)
async def smart_stamp(
    input_file: UploadFile = File(...),
    stamp_file: UploadFile = File(...),
    stamp_type: StampType = StampType.BOTH,
    user=Depends(current_active_user)  # 确保用户已登录
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
        input_file_path = os.path.join(resources_dir, f"temp_{input_file.filename}")
        stamp_file_path = os.path.join(resources_dir, f"temp_{stamp_file.filename}")

        # 处理文件上传
        with open(input_file_path, "wb") as f:
            f.write(await input_file.read())

        with open(stamp_file_path, "wb") as f:
            f.write(await stamp_file.read())

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(resources_dir, f"temp_{os.path.splitext(input_file.filename)[0]}_stamped_{timestamp}.pdf")

        # 调用处理方法
        processor.process(
            input_file=input_file_path,
            stamp_file=stamp_file_path,
            output_file=output_file,
            stamp_type=stamp_type
        )

        return ResponseModel(code=200, message="印章处理成功", data={"output_file": output_file})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{file_name}")
async def download_file(file_name: str, user=Depends(current_active_user)):  # 确保用户已登录
    """下载文件"""
    file_path = os.path.join(resources_dir, file_name)  # 确保路径正确
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件未找到")
    return FileResponse(file_path, media_type='application/pdf', filename=file_name)

@router.post("/upload-images", response_model=ResponseModel)
async def upload_images(images: List[UploadFile] = File(...), user=Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    """批量上传印章图片"""
    
    current_images = await get_all_stamp_images(db, user.id)
    if len(current_images) + len(images) > 30:
        raise HTTPException(status_code=400, detail="总共只能上传最多30张图片")

    uploaded_paths = []
    for image in images:
        if image.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise HTTPException(status_code=400, detail="只支持 PNG 和 JPEG 格式的图片")

        file_path = os.path.join(resources_dir, image.filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        uploaded_paths.append(file_path)

    await upload_stamp_images(db, user.id, uploaded_paths)

    full_paths = [f"{settings.BASE_URL}/{os.path.basename(path)}" for path in uploaded_paths]

    return ResponseModel(code=200, message="上传成功", data=full_paths)

@router.post("/delete-images", response_model=ResponseModel)
async def delete_images(image_ids: List[int], user=Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    """批量删除印章图片"""
    await delete_stamp_images(db, image_ids)
    return ResponseModel(code=200, message="删除成功", data=image_ids)

@router.get("/list-images", response_model=ResponseModel)
async def list_images(user=Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    """获取所有印章图片链接"""
    images = await get_all_stamp_images(db, user.id)
    image_paths = [f"{settings.BASE_URL}/{image.image_path}" for image in images]
    return ResponseModel(code=200, message="获取成功", data=image_paths)
