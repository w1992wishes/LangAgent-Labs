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
        "message": "请分析一下人工智能的发展趋势，包括当前的技术水平和未来的应用前景，拆两个步骤就行"
    }

    print(f"\n📤 发送请求: {data['message']}")

    try:
        response = requests.post(url, json=data, stream=True, timeout=300)

        print(f"\n✅ 连接成功，开始接收流式数据:\n")

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    data_str = line[5:].strip()
                    if data_str:
                        try:
                            event = json.loads(data_str)
                            event_type = event.get('event', 'unknown')
                            print(f"📨 事件: {event_type}")

                            if event_type == 'node_update':
                                node = event.get('node', '')
                                print(f"   节点: {node}")

                            elif event_type == 'final':
                                result = event.get('data', {})
                                print(f"   最终回答: {result.get('response', '')}...")
                                break

                            elif event_type == 'error':
                                error = event.get('data', {}).get('error', 'Unknown error')
                                print(f"   ❌ 错误: {error}")
                                break

                        except json.JSONDecodeError:
                            pass

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
