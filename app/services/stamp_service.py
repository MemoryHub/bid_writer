from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete  # Import delete for async queries
from sqlalchemy.future import select  # Import select for async queries
from app.models.stamp_image import StampImage
from datetime import datetime

async def upload_stamp_images(db: AsyncSession, user_id: int, image_paths: list):
    """批量上传印章图片"""
    stamp_images = []
    for path in image_paths:
        stamp_image = StampImage(
            user_id=user_id,
            image_path=path,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        stamp_images.append(stamp_image)
    
    db.add_all(stamp_images)
    await db.commit()

    # Refresh each stamp image individually
    for stamp_image in stamp_images:
        await db.refresh(stamp_image)

    return stamp_images

async def delete_stamp_images(db: AsyncSession, image_ids: list):
    """批量删除印章图片"""
    await db.execute(delete(StampImage).where(StampImage.id.in_(image_ids)))  # Use delete for async queries
    await db.commit()

async def get_all_stamp_images(db: AsyncSession, user_id: int):
    """获取用户所有印章图片"""
    result = await db.execute(select(StampImage).filter(StampImage.user_id == user_id))  # Use select for async queries
    return result.scalars().all()  # Use scalars() to get the results 