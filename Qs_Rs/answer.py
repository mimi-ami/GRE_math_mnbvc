from bs4 import BeautifulSoup
import requests
import json


# 请求网页
def request_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    payload = {
        "action": "ld_adv_quiz_pro_ajax",
        "func": "checkAnswers",
        "data[quizId]": 811,
        "data[quiz]": 17246,
        "data[course_id]": 55283,
        "data[quiz_nonce]": "6de863c7ce",
        "data[responses]": json.dumps({
            "5126": {
                "response": {
                    "0": "false",
                    "1": "false",
                    "2": "true",
                    "3": "true",
                    "4": "false",
                    "5": "false"
                },
                "question_pro_id": 5126,
                "question_post_id": 21175
            }
        }),
        "quiz": 17246,
        "course_id": 55283,
        "quiz_nonce": "6de863c7ce"
    }
    response = requests.post(url, headers=head, data=payload)
    print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)   
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")

    return data



def get_result(data):
    answer_message = data.get("5126", {}).get("e", {}).get("AnswerMessage", "")
    soup = BeautifulSoup(answer_message, "html.parser")
    text = soup.get_text()

    return text


# 保存数据到表格
def saveData(data):
    file_path = f"D:/github_project/GRE_math_crewler/Qs_Rs/answer.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)




if __name__ == "__main__":
    print("begin")
    url = "https://www.test-guide.com/wp-admin/admin-ajax.php"  # 答案
    
    html = request_url(url) # 保存结果
    result = get_result(html)
    saveData(result)
    print("over")