from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.response import ResponseModel
import os
from app.core.config import settings  # 导入配置

router = APIRouter(prefix="/upload", tags=["upload"])

# 定义文件保存路径
UPLOAD_DIRECTORY = settings.UPLOAD_DIRECTORY

# 确保上传目录存在
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'docx', 'doc', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/multiple-files", response_model=ResponseModel)
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """
    上传多个文件
    """
    file_paths = []
    
    for file in files:
        # 限制文件大小为 500MB
        if file.size > 500 * 1024 * 1024:  # 500MB
            raise HTTPException(status_code=400, detail="文件大小超过限制（500MB）")

        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="不允许的文件类型")

        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(file_location)

    # 构建返回的完整路径，确保包含 /resources
    full_paths = [f"{settings.BASE_URL}/{settings.UPLOAD_DIRECTORY}/{os.path.basename(path)}" for path in file_paths]

    return ResponseModel(code=200, message="文件上传成功", data=full_paths)
