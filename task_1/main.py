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
        print("Получение данных...")
        response = requests.get(url, headers=headers, timeout=10)
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
                    comment_links = subtext.find_all('a')
                    if comment_links:
                        comment_link = comment_links[-1]
                        if 'comment' in comment_link.text.lower():
                            comment_text = comment_link.text.strip()
                            if comment_text.lower() != 'discuss':
                                try:
                                    comment_parts = comment_text.split()
                                    if comment_parts:
                                        comments_text = comment_parts[0]
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
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return []
def save_to_json(data, filename='data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")
        return False
def display_news(news_list):
    print("\n" + "=" * 60)
    print("НОВОСТИ HACKER NEWS")
    print("=" * 60)
    if not news_list:
        print("Нет данных для отображения")
        return
    for item in news_list:
        print(f"{item['id']:3}. {item['title'][:60]}...")
        print(f"     Комментарии: {item['comments']:4} | Очки: {item['points']:4} | Ссылка: {item['link'][:50]}...")
        print("-" * 60)
def main():
    print("=" * 60)
    print("ЗАПУСК ПАРСЕРА HACKER NEWS")
    print("=" * 60)
    news_data = parse_hacker_news()
    if news_data:
        display_news(news_data)
        if save_to_json(news_data):
            print("\n" + "-" * 60)
            print("СТАТИСТИКА:")
            print(f"Всего новостей: {len(news_data)}")
            print(f"Всего комментариев: {sum(item['comments'] for item in news_data)}")
            print(f"Всего очков: {sum(item['points'] for item in news_data)}")
            print("\n" + "-" * 60)
            print("ПРИМЕР ДАННЫХ ИЗ ФАЙЛА:")
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    sample_data = json.load(f)
                    if sample_data:
                        first_item = sample_data[0]
                        print(f"Первая новость: {first_item['title']}")
                        print(f"Комментарии: {first_item['comments']}, Очки: {first_item['points']}")
                        print(f"Ссылка: {first_item['link']}")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
    else:
        print("Не удалось получить данные с Hacker News")
if __name__ == "__main__":
    main()
