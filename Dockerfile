# Dockerfile
FROM docker.arvancloud.ir/python:3.13-slim

# ایجاد کاربر vscode با UID/GID 1000 (استاندارد Dev Containers)
# ARG USERNAME=vscode
# ARG USER_UID=1000
# ARG USER_GID=1000

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# # نصب ابزارهای ضروری + ایجاد کاربر vscode
# RUN apt-get update && apt-get install -y \
#     curl \
#     sudo \
#     && groupadd --gid $USER_GID $USERNAME \
#     && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
#     && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی و نصب پکیج‌ها
COPY core/requirements.txt .
# چون PIP_INDEX_URL را ست کردید، pip خودش از آینه لیارا استفاده می‌کند
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# کپی کد
COPY core/ .

# تغییر مالکیت دایرکتوری به vscode (برای جلوگیری از مشکلات دسترسی)
# RUN chown -R $USERNAME:$USERNAME /app

# مهم: اجرای کانتینر با کاربر vscode
# USER $USERNAME

EXPOSE 8000