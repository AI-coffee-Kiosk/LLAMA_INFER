import random
import json
import os

# 주문 데이터 저장 디렉토리 설정
output_dir = "order_scenarios"
os.makedirs(output_dir, exist_ok=True)

# 메뉴, 사이즈, 옵션 및 액션 목록 설정
menu = ["아메리카노", "라떼", "카푸치노", "카페모카", "바닐라라떼", "에스프레소", "카라멜마끼아또",
        "허브티", "홍차", "초콜릿라떼", "레몬에이드", "복숭아아이스티", "딸기스무디", "망고스무디", "키위주스", "토마토주스"]
sizes = ["미디움", "라지"]
temperatures = ["핫", "아이스"]
actions = ["add_item", "modify_order", "cancel_order", "recommend_closest_item"]
# 주문 항목 생성 함수
def create_order_item(drink=None, size=None, temperature=None, quantity=None, add_ons=None, extra_shots=0):
    return {
        "drink": drink or random.choice(menu),
        "size": size or random.choice(sizes),
        "temperature": temperature or random.choice(temperatures),
        "quantity": quantity or random.randint(1, 10),
        "add_ons": add_ons or [],
        "extra_shots": extra_shots
    }

# 추천 문구 생성 함수
def generate_recommendation():
    recommendation = random.choice(menu)
    return recommendation, f"{recommendation}를 추천합니다."

# 시나리오 생성 함수
def generate_scenario(num_actions):
    conversation_history = []
    accumulated_items = []
    cumulative_input = ""

    # 첫 번째 액션은 create_order로 설정
    item = create_order_item()
    accumulated_items.append(item)
    quantity_text = f"{item['quantity']}잔" if item["quantity"] > 1 else "한 잔"
    t = f"{item['temperature']} {item['drink']} {quantity_text} 줘"
    response = f"{item['drink']} {item['quantity']}잔 주문되었습니다.\n지금까지 주문하신 내용은 다음과 같습니다:\n- {item['temperature']} {item['drink']} {item['size']} {item['quantity']}잔"
    json_output = {"action": "create_order", "order_items": accumulated_items.copy()}
    cumulative_input += f"Customer's 1 Input: {t} "
    conversation_history.append({
        "instruction": "Process the customer’s order based on the latest input in the current conversation history, considering previous items ordered in the session, and generate the appropriate natural language response and JSON output.",
        "input": cumulative_input.strip(),
        "output": f"**Natural Language Response**: \"{response}\"\n\n**JSON Output**:\n```json\n{json.dumps(json_output, ensure_ascii=False, indent=2)}\n```\n"
    })

    # 추가 액션 실행
    for i in range(2, num_actions):
        action = random.choice(actions)

        if action == "add_item":
            quantity = random.randint(1, 10)
            item = create_order_item(quantity=quantity)
            accumulated_items.append(item)
            quantity_text = f"{quantity}잔" if quantity > 1 else "한 잔"
            t = f"{item['temperature']} {item['drink']} {quantity_text} 추가해줘"
            response = f"{item['drink']} {item['quantity']}잔 추가 주문되었습니다.\n지금까지 주문하신 내용은 다음과 같습니다:\n" + \
                       "\n".join([f"- {x['temperature']} {x['drink']} {x['size']} {x['quantity']}잔" for x in
                                  accumulated_items])
            json_output = {"action": action, "order_items": accumulated_items.copy()}

        elif action == "modify_order" and accumulated_items:
            modified_item = random.choice(accumulated_items)
            new_quantity = random.randint(1, 10)
            modified_item["quantity"] = new_quantity
            quantity_text = f"{new_quantity}잔" if new_quantity > 1 else "한 잔"
            t = f"{modified_item['drink']} 수량을 {quantity_text}으로 변경해줘"
            response = f"{modified_item['drink']} 수량을 {modified_item['quantity']}잔으로 변경했습니다.\n" + \
                       "\n".join([f"- {x['temperature']} {x['drink']} {x['size']} {x['quantity']}잔" for x in
                                  accumulated_items])
            json_output = {"action": action, "order_items": accumulated_items.copy()}

        elif action == "cancel_order" and accumulated_items:
            canceled_item = random.choice(accumulated_items)
            accumulated_items = [x for x in accumulated_items if x != canceled_item]  # 항목을 제거
            t = f"{canceled_item['drink']} 주문 취소해줘"
            response = f"{canceled_item['drink']} 주문이 취소되었습니다.\n지금까지 주문하신 내용은 다음과 같습니다:\n" + \
                       "\n".join([f"- {x['temperature']} {x['drink']} {x['size']} {x['quantity']}잔" for x in
                                  accumulated_items])
            json_output = {"action": action, "order_items": accumulated_items.copy()}

        elif action == "recommend_closest_item":
            recommendation, recommendation_text = generate_recommendation()
            response = recommendation_text
            json_output = {"action": action, "order_items": accumulated_items.copy()}
            t = "음료 추천해줘"

        cumulative_input += f"Customer's {i} Input: {t} "
        conversation_history.append({
            "instruction": "Process the customer’s order based on the latest input in the current conversation history, considering previous items ordered in the session, and generate the appropriate natural language response and JSON output.",
            "input": cumulative_input.strip(),
            "output": f"**Natural Language Response**: \"{response}\"\n\n**JSON Output**:\n```json\n{json.dumps(json_output, ensure_ascii=False, indent=2)}\n```\n"
        })

    # 마지막 액션으로 complete_order 추가 (모든 주문 항목 포함)
    response = "주문이 완료되었습니다. 결제는 카드리더기를 사용해주세요. 감사합니다."
    json_output = {"action": "complete_order", "order_items": accumulated_items.copy()}
    cumulative_input += f"Customer's {num_actions} Input: 주문 완료할게요 "
    conversation_history.append({
        "instruction": "Process the customer’s order based on the latest input in the current conversation history, considering previous items ordered in the session, and generate the appropriate natural language response and JSON output.",
        "input": cumulative_input.strip(),
        "output": f"**Natural Language Response**: \"{response}\"\n\n**JSON Output**:\n```json\n{json.dumps(json_output, ensure_ascii=False, indent=2)}\n```\n"
    })

    return conversation_history

# 시나리오 100개 생성 및 단일 JSON 파일에 저장
num_scenarios = 1000
all_scenarios = []
for scenario_num in range(1, num_scenarios + 1):
    num_actions = random.randint(3, 5)  # 중간 액션 수는 랜덤, 끝은 complete_order로 고정
    scenario_data = generate_scenario(num_actions)
    all_scenarios.append(scenario_data)

# 모든 시나리오를 단일 JSON 파일에 저장
filename = os.path.join(output_dir, "all_scenarios2.json")
with open(filename, "w", encoding="utf-8") as file:
    json.dump(all_scenarios, file, ensure_ascii=False, indent=2)
print(f"All scenarios saved to {filename}")
