from bs4 import BeautifulSoup
import requests
import time


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
    file_path = f"D:/project/python_study/Qs_Rs/result.html"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)



def get_qs(html):

    datalist = []
    
    # 解析html
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('div', class_="wpProQuiz_listItem"): # 10个list
        question_id = item["data-question-meta"]
        p = item.find('wpProQuiz_question_text')
        if p:
            print(p.get_text())
            datalist.append(p.get_text())
    

    return datalist





if __name__ == "__main__":
    print("begin")
    url = "https://www.test-guide.com/courses/gre/lessons/gre-quantitative-reasoning-practice-sets/quizzes/gre-math-multiple-choice-many-practice-test-1" # 问题
    
    html = request_url(url) # 保存网页源码
    answer = get_qs(html)
    print(answer)
    # saveData(answer)
   
    print("over")