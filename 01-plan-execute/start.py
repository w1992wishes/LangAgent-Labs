"""
启动脚本

快速启动 Plan-Execute Agent API 服务
"""
import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 添加 src 目录到 Python 路径
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.insert(0, src_path)

import uvicorn
from dotenv import load_dotenv
from check_env import check_env

# 加载环境变量
load_dotenv()


if __name__ == "__main__":
    # 先检查环境
    if not check_env():
        sys.exit(1)

    print("=" * 60)
    print("🚀 启动 Plan-Execute Agent API")
    print("=" * 60)
    print()

    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
