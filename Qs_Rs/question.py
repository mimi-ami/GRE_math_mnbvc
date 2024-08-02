from bs4 import BeautifulSoup
import requests
import json
import re

# 请求网页
def request_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=head)

    if response.status_code == 200:
        print("Request was successful")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")

    return response.text



# 保存数据
def saveData(data):
    file_path = f"D:/github_project/GRE_math_crewler/Qs_Rs/question.html"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)



def get_qs(html):

    datalist = []
    
    # 解析html
    soup = BeautifulSoup(html, "html.parser")
    # print(list[-2])

    quiz_id = soup.find('div', class_= "wpProQuiz_content")["data-quiz-meta"]
    print(quiz_id)

    for item in soup.find_all('li', class_="wpProQuiz_listItem"): # 10个list
        data = []
        question_id = item["data-question-meta"]
        print(question_id)
        p = item.find('div', class_='wpProQuiz_question_text')
        if p:
            question_text = p.get_text()
            print(question_text)
        question_list = []
        lists = item.find_all('li', class_='wpProQuiz_questionListItem')
        for i in lists:
            one = i.find('label').get_text()
            question_list.append(one.strip())
        print(question_list)


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

    # 输出结果
    for key, value in extracted_data.items():
        print(f"{key}: {value}")

    return datalist





if __name__ == "__main__":
    print("begin")
    url = "https://www.test-guide.com/courses/gre/lessons/gre-quantitative-reasoning-practice-sets/quizzes/gre-math-multiple-choice-many-practice-test-1" # 问题
    
    html = request_url(url) # 保存网页源码
    get_qs(html)
    # saveData(html)
   
    print("over")