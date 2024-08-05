from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import datetime

# 请求问题接口
def question_request_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=head)

    if response.status_code == 200:
        print("Request was successful")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")

    return response.text


# 获取问题内容
def get_question(html):
    # 解析html
    soup = BeautifulSoup(html, "html.parser")

    data = [] # 存 id+问题+选项
    for item in soup.find_all('li', class_="wpProQuiz_listItem"): # 10个list
        question = {}
        question_id = item["data-question-meta"]
        match = re.search(r'"question_pro_id":(\d+),"question_post_id":(\d+)', question_id)

        if match:
            # 提取的值
            question_pro_id = int(match.group(1))
            question_post_id = int(match.group(2))

            # 将值添加到字典中
            question = {
                "question_pro_id": question_pro_id,
                "question_post_id": question_post_id
            }
        
        p = item.find('div', class_='wpProQuiz_question_text')
        # 问题
        if p:
            question_text = p.get_text().strip()
            question["QS_text"] = question_text
        data.append(question)

    list = soup.find_all('script', {'type' : "text/javascript"})
    # 定义要提取的键
    keys_to_extract = [
        'course_id', 'lesson_id', 'quiz', 'quizId', 'quiz_nonce'
    ]

    # 正则表达式模式
    pattern = r'\b({})\b\s*:\s*(.*?)(?:,|\n)'.format('|'.join(keys_to_extract))

    # 提取数据
    matches = re.findall(pattern, str(list[-2]))

    # 打印提取结果
    extracted_data = {}
    for key, value in matches:
        # 处理json值的情况
        if key == 'json':
            json_str = value.strip().rstrip(',').strip()
            extracted_data[key] = json_str
        else:
            extracted_data[key] = value.strip().rstrip(',').strip()

    data.append(extracted_data)
    
    return data


# 请求答案接口
def answer_request_url(quizId, quiz, course_id, quiz_nonce, response, url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    payload = {
        "action": "ld_adv_quiz_pro_ajax",
        "func": "checkAnswers",
        "data[quizId]": quizId,
        "data[quiz]": quiz,
        "data[course_id]": course_id,
        "data[quiz_nonce]": quiz_nonce,
        "data[responses]": response,
        "quiz": quiz,
        "course_id": course_id,
        "quiz_nonce": quiz_nonce
    }
    response = requests.post(url, headers=head, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)   
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")

    return data


# 获取答案
def get_answer(id_list, data):
    answer = {}
    for id in id_list:
        answer_message = data.get(id, {}).get("e", {}).get("AnswerMessage", "")
        soup = BeautifulSoup(answer_message, "html.parser")
        text = soup.get_text()
        answer[id] = text
    return answer



# 保存数据
def save(x, question, answer):
    result = []
    for items in question: 
        if "course_id" in items:
            continue
        data = {}
        data["id"] = x
        x += 1
        data["问"] = ""
        data["答"] = ""
        data["来源"] = "https://www.test-guide.com/"
        data["元数据"] = {
            "create_time": datetime.now().strftime("%Y%m%d %H:%M:%S"),
            "问题明细": items["QS_text"],
            "回答明细": answer[str(items["question_pro_id"])],    
            "扩展字段": ""
        }
        data["时间"] = datetime.now().strftime("%Y%m%d")
        result.append(data)

    file_path = f"D:/github_project/GRE_math_crewler/Qs_Rs/result2.json"
    with open(file_path, 'a', encoding='utf-8') as file:
        for item in result:
            data_str = json.dumps(item, ensure_ascii=False)
            file.write(data_str + "\n")




if __name__ == "__main__":
    print("begin")


    # 问题
    question_url = [
                    "https://www.test-guide.com/courses/gre/lessons/gre-quantitative-reasoning-practice-sets/quizzes/gre-math-numeric-entry-practice-test-1",
                    "https://www.test-guide.com/courses/gre/lessons/gre-quantitative-reasoning-practice-sets/quizzes/gre-math-numeric-entry-practice-test-2"
                    ]
   
    for i in range(2):
        html = question_request_url(question_url[i]) # 保存网页源码
        question = get_question(html)
        # 答案
        answer_url = "https://www.test-guide.com/wp-admin/admin-ajax.php"  # 答案
        data = {}
        id_list = []
        for items in question:
            if "course_id" in items:
                quizId = items["quizId"]
                quiz = items["quiz"]
                course_id = items["course_id"]
                quiz_nonce = items["quiz_nonce"].strip("'")
                continue
            id = str(items["question_pro_id"])
            id_list.append(id)
            data[id] = {
                "response": "1",
                "question_pro_id": items["question_pro_id"],
                "question_post_id": items["question_post_id"]
            }
        response = json.dumps(data)
        html = answer_request_url(quizId, quiz, course_id, quiz_nonce, response, answer_url) # 保存结果
        answer = get_answer(id_list, html)

        x = 40 + i*10
        # # 处理成规定格式，保存
        save(x, question, answer)


    print("over")



   
  