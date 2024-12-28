# 使用官方的 Python 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main non-free contrib" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    libreoffice \
    openjdk-11-jre-headless \
    fonts-wqy-zenhei fonts-wqy-microhei xfonts-intl-chinese xfonts-intl-chinese-big xfonts-100dpi xfonts-75dpi \
    ttf-mscorefonts-installer \
    && rm -rf /var/lib/apt/lists/*


# 复制 requirements.txt 并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 安装 Python 项目依赖
RUN pip install --no-cache-dir --upgrade pip

# 暴露应用端口
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
