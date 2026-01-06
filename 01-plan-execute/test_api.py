"""
API 测试脚本

测试 Plan-Execute Agent 的功能
"""
import requests
import json


def test_non_stream():
    """测试非流式接口"""
    print("=" * 60)
    print("测试非流式接口")
    print("=" * 60)

    url = "http://localhost:8000/api/chat"
    data = {
        "message": "请分析一下人工智能的发展趋势，包括当前的技术水平和未来的应用前景，拆两个步骤就行"
    }

    print(f"\n📤 发送请求: {data['message'][:50]}...")

    try:
        response = requests.post(url, json=data, timeout=600)
        response.raise_for_status()

        result = response.json()
        print(f"\n✅ 状态码: {response.status_code}")
        print(f"\n📋 执行计划:")
        for step in result['plan']:
            print(f"  {step['step_id']}. {step['description']} - {step['status']}")

        print(f"\n📝 步骤结果:")
        for i, step_result in enumerate(result['steps_results']):
            print(f"  步骤 {i+1}: {step_result}...")

        print(f"\n💡 最终回答:")
        print(f"  {result['response']}...")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 错误: {e}")


def test_stream():
    """测试流式接口"""
    print("\n" + "=" * 60)
    print("测试流式接口")
    print("=" * 60)

    url = "http://localhost:8000/api/chat/stream"
    data = {
        "message": "你好，请简单介绍一下你自己"
    }

    print(f"\n📤 发送请求: {data['message']}")

    try:
        response = requests.post(
            url,
            json=data,
            stream=True,
            timeout=300
        )

        print(f"\n✅ 连接成功，开始接收流式数据:\n")
        print("=" * 60)

        # SSE 解析：组合多行为一个事件
        current_event = None
        current_data = []

        for line in response.iter_lines(decode_unicode=True):
            if line:
                # 解析 SSE 格式
                if line.startswith('event:'):
                    current_event = line[6:].strip()
                elif line.startswith('data:'):
                    data_str = line[5:].strip()
                    if data_str:
                        current_data.append(data_str)
                elif line == '':  # 空行表示事件结束
                    if current_event and current_data:
                        # 组合数据
                        combined_data = '\n'.join(current_data)

                        try:
                            if current_event in ['start', 'progress']:
                                # 简单字符串数据
                                if current_event == 'start':
                                    print(f"\n🚀 {combined_data}\n")
                                elif current_event == 'progress':
                                    print(f"⏳ {combined_data}")

                            elif current_event == 'final':
                                # JSON 数据
                                event_data = json.loads(combined_data)
                                print("\n" + "=" * 60)
                                print(f"🎯 最终结果（结构化数据）:")
                                print("=" * 60)

                                # 显示计划
                                plan = event_data.get('plan', [])
                                print(f"\n📋 执行计划（{len(plan)}个步骤）:")
                                for step in plan:
                                    print(f"  {step.get('step_id', '-')}. {step.get('description', '')}")

                                # 显示最终回答
                                print(f"\n💡 最终回答:")
                                print(f"{event_data.get('response', '')}\n")
                                break

                            elif current_event == 'error':
                                print(f"\n❌ 错误: {combined_data}\n")
                                break

                        except json.JSONDecodeError as e:
                            print(f"[解析错误] {e}")
                        finally:
                            # 重置
                            current_event = None
                            current_data = []

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 错误: {e}")


def test_root():
    """测试根路径"""
    print("=" * 60)
    print("测试根路径")
    print("=" * 60)

    try:
        response = requests.get("http://localhost:8000/")
        response.raise_for_status()
        print(f"\n✅ API 运行中")
        print(f"📄 信息: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except requests.exceptions.RequestException:
        print(f"\n❌ API 未运行，请先启动服务")
        return False

    return True


if __name__ == "__main__":
    print("\n🧪 Plan-Execute Agent API 测试\n")

    # 先测试服务是否运行
    if test_root():
        # 测试非流式接口
        #test_non_stream()

        # 测试流式接口
        test_stream()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
