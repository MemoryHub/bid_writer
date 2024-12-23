from sqlalchemy import Column, Integer, String
from app.db.database import Base

class StampImage(Base):
    __tablename__ = "stamp_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 去掉外键约束
    image_path = Column(String, nullable=False)
    created_at = Column(String, nullable=False)  # 可以使用 DateTime 类型
    updated_at = Column(String, nullable=False)  # 可以使用 DateTime 类型 