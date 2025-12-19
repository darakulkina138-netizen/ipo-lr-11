import requests
from bs4 import BeautifulSoup
import json
import time
def parse_hacker_news():
    url = "https://news.ycombinator.com/"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print("Получение данных")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_rows = soup.find_all('span', class_='titleline')
        subtext_rows = soup.find_all('td', class_='subtext')
        news_list = []
        for i in range(len(title_rows)):
            title_link = title_rows[i].find('a')
            if title_link:
                title = title_link.text.strip()
                link = title_link.get('href', '')
                comments = 0
                if i < len(subtext_rows):
                    subtext = subtext_rows[i]
                    comment_link = subtext.find_all('a')[-1]
                    if 'comment' in comment_link.text:
                        comment_text = comment_link.text.strip()
                        if comment_text != 'discuss':
                            try:
                                comments_text = comment_text.split()[0]
                                comments = int(comments_text) if comments_text.isdigit() else 0
                            except:
                                comments = 0
                points = 0
                if i < len(subtext_rows):
                    subtext = subtext_rows[i]
                    score_elem = subtext.find('span', class_='score')
                    if score_elem:
                        try:
                            points_text = score_elem.text.split()[0]
                            points = int(points_text)
                        except:
                            points = 0
                news_item = {
                    'id': i + 1,
                    'title': title,
                    'link': link,
                    'comments': comments,
                    'points': points,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                news_list.append(news_item)
        return news_list
        return []
def save_to_json(data, filename='data.json'): 
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в файл: {filename}")
        return 
def display_news(news_list):
    print("\n" + " ")
    print("Новости:")
    print(" ")
    for item in news_list:
        print(f"{item['id']}. Title: {item['title']}; Comments: {item['comments']};")
def main():
    print("Запуск парсера")
    print("-" * 40)
    news_data = parse_hacker_news()
    if news_data:
        display_news(news_data)
        save_to_json(news_data)
        print("\n" + "-" * 40)
        print(f"Всего новостей: {len(news_data)}")
        print(f"Всего комментариев: {sum(item['comments'] for item in news_data)}")
        print(f"Сохранено")
        print("\n" + " " * 40)
        print("Пример данных:")
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
                if sample_data:
                    print(f"Первая новость: {sample_data[0]['title'][:50]}...")

if __name__ == "__main__":
    main()
