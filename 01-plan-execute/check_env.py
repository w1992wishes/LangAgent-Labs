"""
环境配置检查工具

运行前检查环境变量是否正确配置
"""
import os
from dotenv import load_dotenv

def check_env():
    """检查环境配置"""
    print("=" * 60)
    print("🔍 检查环境配置")
    print("=" * 60)

    # 加载 .env 文件
    load_dotenv()

    # 检查必需的环境变量
    api_key = os.getenv("DASHSCOPE_API_KEY")
    api_base = os.getenv("DASHSCOPE_API_BASE")
    model = os.getenv("DASHSCOPE_MODEL")

    issues = []

    # 检查 API Key
    if not api_key:
        issues.append("❌ DASHSCOPE_API_KEY 未设置")
    elif api_key.startswith("your-") or api_key == "sk-xxxxxxxxxxxxxx":
        issues.append("❌ DASHSCOPE_API_KEY 使用了默认值，请替换为真实的 API Key")
    else:
        print(f"✅ DASHSCOPE_API_KEY: {api_key[:10]}...{api_key[-4:]}")

    # 检查 API Base
    if not api_base:
        issues.append("⚠️  DASHSCOPE_API_BASE 未设置，将使用默认值")
    else:
        print(f"✅ DASHSCOPE_API_BASE: {api_base}")

    # 检查 Model
    if not model:
        issues.append("⚠️  DASHSCOPE_MODEL 未设置，将使用默认值")
    else:
        print(f"✅ DASHSCOPE_MODEL: {model}")

    print("-" * 60)

    # 检查 .env 文件是否存在
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        print(f"✅ .env 文件存在: {env_path}")
    else:
        issues.append(f"❌ .env 文件不存在: {env_path}")
        print(f"💡 提示: 请复制 .env.example 到 .env 并配置")

    print("=" * 60)

    if issues:
        print("\n❌ 发现以下问题:")
        for issue in issues:
            print(f"   {issue}")
        print("\n请修复这些问题后再运行服务。\n")
        return False
    else:
        print("\n✅ 环境配置检查通过！\n")
        return True


if __name__ == "__main__":
    if check_env():
        print("🚀 可以启动服务了！运行: python start.py")
    else:
        print("⚠️  请先修复环境配置问题")
