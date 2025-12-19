import requests
from bs4 import BeautifulSoup
import json
import sys
def parse_countries_data():
    url = "https://www.scrapethissite.com/pages/simple/"
    countries_data = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print("олучение данных с сайта...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        country_blocks = soup.find_all('div', class_='col-md-4 country')
        if not country_blocks:
            print("На странице не найдены блоки со странами.")
            return countries_data
        print(f"Найдено блоков стран: {len(country_blocks)}")
        for block in country_blocks:
            country_info = extract_country_info(block)
            if country_info:
                countries_data.append(country_info)
        print(f"Успешно обработано стран: {len(countries_data)}")
        return countries_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []
    except Exception as e:
        return []
def extract_country_info(country_block):
    try:
        name_elem = country_block.find('h3', class_='country-name')
        country_name = name_elem.get_text(strip=True) if name_elem else "Неизвестно"
        capital_elem = country_block.find('span', class_='country-capital')
        capital = capital_elem.get_text(strip=True) if capital_elem else "Неизвестно"
        population_elem = country_block.find('span', class_='country-population')
        population = population_elem.get_text(strip=True) if population_elem else "0"
        area_elem = country_block.find('span', class_='country-area')
        area = area_elem.get_text(strip=True) if area_elem else "0.0"
        try:
            population = int(population)
        except ValueError:
            population = 0
        try:
            area = float(area)
        except ValueError:
            area = 0.0
        country_info = {
            "name": country_name,
            "capital": capital,
            "population": population,
            "area_km2": area
        }
        return country_info
    except Exception as e:
        print(f"Ошибка при обработке блока страны: {e}")
        return None
def save_to_json(data, filename='countries_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные успешно сохранены в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")
        return False
def display_statistics(countries_data):
    if not countries_data:
        print("Нет данных для отображения статистики.")
        return
    print("\n" + "="*60)
    print("СТАТИСТИКА ПО СТРАНАМ МИРА")
    print("="*60)
    total_countries = len(countries_data)
    print(f"Всего стран: {total_countries}")
    total_population = sum(country['population'] for country in countries_data)
    print(f"Общее население мира: {total_population:,}")
    total_area = sum(country['area_km2'] for country in countries_data)
    print(f"Общая площадь: {total_area:,.2f} км2")
    largest_country = max(countries_data, key=lambda x: x['area_km2'])
    print(f"Самая большая страна: {largest_country['name']} ({largest_country['area_km2']:,.2f} км2)")
    non_zero_area = [c for c in countries_data if c['area_km2'] > 0]
    if non_zero_area:
        smallest_country = min(non_zero_area, key=lambda x: x['area_km2'])
        print(f"Самая маленькая страна: {smallest_country['name']} ({smallest_country['area_km2']:,.2f} км2)")
    most_populous = max(countries_data, key=lambda x: x['population'])
    print(f"Страна с наибольшим населением: {most_populous['name']} ({most_populous['population']:,})")
    avg_area = total_area / total_countries
    print(f"Средняя площадь страны: {avg_area:,.2f} км2")
    countries_no_capital = [c['name'] for c in countries_data if c['capital'] in ['None', 'Неизвестно', '']]
    if countries_no_capital:
        print(f"Стран без столицы: {len(countries_no_capital)}")
        print(f"  Например: {', '.join(countries_no_capital[:3])}")
def display_sample_data(countries_data, count=5):
    if not countries_data:
        return
    print("\n" + "="*60)
    print("ОБРАЗЕЦ ДАННЫХ (первые 5 стран)")
    print("="*60)
    for i, country in enumerate(countries_data[:count], 1):
        print(f"{i}. {country['name']}")
        print(f"   Столица: {country['capital']}")
        print(f"   Население: {country['population']:,}")
        print(f"   Площадь: {country['area_km2']:,.2f} км2")
        print()
def main():
    print("="*60)
    print("ПАРСИНГ ИНФОРМАЦИИ О СТРАНАХ МИРА")
    print("="*60)
    countries_data = parse_countries_data()
    if countries_data:
        display_sample_data(countries_data)
        if save_to_json(countries_data, 'countries_data.json'):
            display_statistics(countries_data)
            print("\n" + "="*60)
            print("ФАЙЛ С ДАННЫМИ")
            print("="*60)
            print("Данные сохранены в формате JSON.")
            print("Структура данных для каждой страны:")
            print("  - name: Название страны")
            print("  - capital: Столица")
            print("  - population: Население (число)")
            print("  - area_km2: Площадь в км² (число с плавающей точкой)")
            print("\nДля загрузки данных в другой программе используйте:")
            print("with open('countries_data.json', 'r', encoding='utf-8') as f:")
            print("    countries = json.load(f)")
    else:
        print("Не удалось получить данные о странах. Проверьте подключение к интернету.")
if __name__ == "__main__":
    main()
