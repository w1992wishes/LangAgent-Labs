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

# 加载环境变量
load_dotenv()


def check_env():
    """检查环境配置"""
    print("=" * 60)
    print("🔍 检查环境配置")
    print("=" * 60)

    # 检查必需的环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL")

    issues = []

    # 检查 API Key
    if not api_key:
        issues.append("❌ OPENAI_API_KEY 未设置")
    elif api_key.startswith("your-") or api_key == "sk-xxxxxxxxxxxxxx":
        issues.append("❌ OPENAI_API_KEY 使用了默认值，请替换为真实的 API Key")
    else:
        print(f"✅ OPENAI_API_KEY: {api_key[:10]}...{api_key[-4:]}")

    # 检查 API Base
    if not api_base:
        print("⚠️  OPENAI_API_BASE 未设置，将使用默认值")
    else:
        print(f"✅ OPENAI_API_BASE: {api_base}")

    # 检查 Model
    if not model:
        print("⚠️  OPENAI_MODEL 未设置，将使用默认值")
    else:
        print(f"✅ OPENAI_MODEL: {model}")

    print("-" * 60)

    # 检查 .env 文件是否存在
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        print(f"✅ .env 文件存在")
    else:
        issues.append(f"❌ .env 文件不存在")
        print(f"💡 提示: 请复制 .env.example 到 .env 并配置")

    print("=" * 60)

    if issues:
        print("\n❌ 发现以下问题:")
        for issue in issues:
            print(f"   {issue}")
        print("\n请修复这些问题后再运行服务。")
        print("\n快速修复:")
        print("1. 打开 .env 文件")
        print("2. 将 OPENAI_API_KEY 替换为你的真实 API Key")
        print("3. 保存后重新运行\n")
        return False
    else:
        print("\n✅ 环境配置检查通过！\n")
        return True


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
