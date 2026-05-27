#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载MapleMono字体
"""

import os
import requests
import zipfile
import io

def download_maple_mono():
    """下载MapleMono字体"""
    # MapleMono字体GitHub仓库
    # 使用最新的release
    url = "https://github.com/subframe7536/maple-font/releases/download/v7.4/MapleMono-NF-CN.zip"

    print(f"正在下载MapleMono字体...")
    print(f"URL: {url}")

    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        print(f"文件大小: {total_size / 1024 / 1024:.2f} MB")

        # 下载文件
        downloaded = 0
        content = b''
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                content += chunk
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r下载进度: {percent:.1f}%", end='', flush=True)

        print("\n下载完成!")

        # 解压字体
        print("正在解压字体...")
        font_dir = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
        os.makedirs(font_dir, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
            # 列出压缩包中的文件
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('.ttf'):
                    # 提取文件名
                    font_name = os.path.basename(file_info.filename)
                    if font_name:  # 跳过目录
                        # 解压文件
                        with zip_ref.open(file_info) as source:
                            font_path = os.path.join(font_dir, font_name)
                            with open(font_path, 'wb') as target:
                                target.write(source.read())
                            print(f"已安装: {font_name}")

        print("字体安装完成!")
        return True

    except Exception as e:
        print(f"下载失败: {e}")
        return False

if __name__ == "__main__":
    download_maple_mono()