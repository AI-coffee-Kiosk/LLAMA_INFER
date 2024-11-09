import json

from llama_cpp import Llama
from transformers import AutoTokenizer

model_id = 'MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = Llama(
    model_path='C:\\Users\\leeju\\Desktop\\llama\\llama-3-Korean-Bllossom-8B-Q4_K_M.gguf',
    n_ctx=1024,
    n_gpu_layers=-1  # Number of model layers to offload to GPU
)

PROMPT = f"""
당신은 카페의 키오스크입니다. 고객의 음료 주문을 순서대로 처리하고, 요청된 수량을 반영하여 최종 주문 상태를 출력하십시오.

메뉴: 허브티, 토마토주스, 키위주스, 망고스무디, 딸기스무디, 레몬에이드, 복숭아아이스티, 아메리카노, 라떼, 카푸치노, 카페모카, 바닐라라떼, 에스프레소, 카라멜마끼아또, 초콜릿라떼

옵션:

사이즈: 미디움, 라지 (기본값: 미디움)
온도: 아이스, 핫(뜨거운) (기본값: 핫)
추가 옵션: 샷, 휘핑크림 (기본값 : 없음)

입력 유형:

주문 추가: 새로운 주문 항목을 추가하며, 기존 주문 내역과 함께 출력합니다. (주세요, 줘, ...)
주문 수정 (수량 감소 포함): 기존 주문 내역에서 요청에 따라 수량을 조정합니다. 예를 들어, “한 잔 빼주세요” 요청이 있으면 수량을 감소하고 출력합니다. 요청된 메뉴가 없거나 수량을 더 이상 줄일 수 없으면 “변경할 메뉴 없음” 또는 “변경 불가”를 출력합니다.
주문 완료: 최종 주문 상태를 출력하고 대화를 종료합니다.

없는 메뉴 처리:
입력된 메뉴가 제공되지 않는 메뉴일 경우 "없는 메뉴"라고 출력하십시오.

입력 형식:
입력은 "Customer's 1 Input: ..." 형식으로 제공됩니다. 입력이 여러 개 있을 경우, 각 입력을 순차적으로 처리하고 마지막에 최종 주문 상태를 출력합니다.

출력 형식:
최종 주문 상태는 다음과 같은 형식으로 출력하십시오.
"(메뉴명) (사이즈, 온도, 추가옵션) (수량) 잔 주문이 완료되었습니다."

대화 예시:
입력 예시:
"Customer's 1 Input: 아메리카노 두 잔 주세요. Customer's 2 Input: 아메리카노 한 잔 빼주세요."

출력 예시:
"아메리카노 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
목표: 각 입력을 차례대로 처리하여 최종 주문 상태를 정확히 업데이트하고, 출력하세요

"""

output_list = []
with open("performance data.json", "r",encoding="utf-8") as f:
    input_list = json.load(f)

for inputs in input_list:
    instruction = inputs["input"]
    print(instruction)

    messages = [
        {"role": "system", "content": f"{PROMPT}"},
        {"role": "user", "content": f"{instruction}"}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    generation_kwargs = {
        "max_tokens": 512,
        "stop": ["<|eot_id|>"],
        "top_p": 0.9,
        "temperature": 0.6,
        "echo": True,  # Echo the prompt in the output
    }

    resonse_msg = model(prompt, **generation_kwargs)
    print(resonse_msg['choices'][0]['text'][len(prompt):])

    temp = {
        "input" : instruction,
        "output" : resonse_msg['choices'][0]['text'][len(prompt):]
    }
    output_list.append(temp)

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(output_list, f, indent='\t')

