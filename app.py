from flask import Flask, render_template, request, jsonify
import os
import bardapi

# Bard API key 설정
os.environ['_BARD_API_KEY'] = "XwgyrM8N1vkwESsSa5RQIK-bUDSJkbNfpT2GD25LaWTydkW8zCJ-WQPpoo9_sWf_6XBYEw."

bard = bardapi.core.Bard()

app = Flask(__name__)

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text # 한글로 13페이지 넘어가면 오류나옴? 글자수의 문제인듯

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        user_question = data['question']
        text = load_text('bard.txt')
        combined_text = "질문: 사립유치원과 관련하여"+user_question +"? 라는 질문에 대해 짧게 답변해줘. '네, 알겠습니다. 사립유치원과 관련하여 추가경정예산이란 무엇인지 150자 이내로 설명해 드리겠습니다.' 이런 설명 제외하고 답변부터 바로 출력해 2. 답변은 참고텍스트를 기준으로 해줘 헌법처럼 3. 사립유치원과 관련 없는 질문에는 관련없는 질문이라 대답못하겠다고 답변해줘. 4. 답변할 때 '네 알겠습니다.', '네, 한국어로 답변해드리겠습니다.' ,'150자로 설명해드리겠습니다.' 이런 말들은 하지 말고 바로 답변해. 5. 앞에 쓴 1,2,3,4의 요청사항은 답변할 때 설명하지말고 바로 답변해. 참고 텍스트="+ text
        response = bard.get_answer(combined_text)
        # 'choices' 키가 존재하고 그 안에 내용이 있는지 확인
        if 'choices' in response and len(response['choices']) > 0:
            answer = response['choices'][0]['content']
        else:
            answer = "The key 'choices' is not in the response or there are no choices."
        return jsonify({'answer': answer})

    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
