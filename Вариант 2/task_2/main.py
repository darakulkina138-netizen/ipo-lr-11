import requests
from bs4 import BeautifulSoup
import json
import os
import sys
def parse_countries_data():
    url = "https://www.scrapethissite.com/pages/simple/"
    countries_data = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print("Получение данных с сайта...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        country_blocks = soup.find_all('div', class_='col-md-4 country')
        if not country_blocks:
            print("Не найдены блоки со странами.")
            return countries_data
        print(f"Найдено стран: {len(country_blocks)}")
        for block in country_blocks:
            country_info = extract_country_info(block)
            if country_info:
                countries_data.append(country_info)
        print(f"Успешно обработано: {len(countries_data)} стран")
        return countries_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return []
def extract_country_info(country_block):
    try:
        name_elem = country_block.find('h3', class_='country-name')
        if not name_elem:
            return None
        country_name = name_elem.get_text(strip=True)
        if not country_name:
            return None
        capital_elem = country_block.find('span', class_='country-capital')
        capital = capital_elem.get_text(strip=True) if capital_elem else "Не указана"
        population_elem = country_block.find('span', class_='country-population')
        population_text = population_elem.get_text(strip=True) if population_elem else "0"
        area_elem = country_block.find('span', class_='country-area')
        area_text = area_elem.get_text(strip=True) if area_elem else "0.0"
        try:
            population = int(population_text)
        except (ValueError, TypeError):
            population = 0
        try:
            area = float(area_text)
        except (ValueError, TypeError):
            area = 0.0
        population_formatted = format(population, ",").replace(",", " ")
        area_formatted = format(area, ",.2f").replace(",", " ") if area >= 0.01 else "0.00"
        return {
            "name": country_name,
            "capital": capital,
            "population": population,
            "population_formatted": population_formatted,
            "area": area,
            "area_formatted": area_formatted
        }
    except Exception as e:
        print(f"Ошибка при обработке блока: {e}")
        return None
def save_to_json(data, filename='data.json'):
    """
    Сохраняет данные в JSON файл
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False
def generate_html_page(countries_data):
    """
    Генерирует HTML страницу с таблицей стран
    """
    if not countries_data:
        print("Нет данных для генерации HTML страницы")
        return False
    total_countries = len(countries_data)
    total_population = sum(country['population'] for country in countries_data)
    total_area = sum(country['area'] for country in countries_data)
    total_population_formatted = format(total_population, ",").replace(",", " ")
    total_area_formatted = format(total_area, ",.0f").replace(",", " ")
    
    html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Страны мира - Статистика</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.8rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .stats-bar {
            background: #f8f9fa;
            padding: 15px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            border-bottom: 1px solid #dee2e6;
        }
        
        .stat-item {
            text-align: center;
            padding: 10px;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1a2980;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #666;
        }
        
        .table-container {
            padding: 30px;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        thead {
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            position: sticky;
            top: 0;
        }
        
        th {
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            letter-spacing: 0.5px;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        th:last-child {
            border-right: none;
        }
        
        tbody tr {
            border-bottom: 1px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        
        tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tbody tr:hover {
            background-color: #e3f2fd;
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        td {
            padding: 15px;
            vertical-align: middle;
        }
        
        .country-name {
            font-weight: 600;
            color: #1a2980;
        }
        
        .capital {
            color: #26d0ce;
            font-weight: 500;
        }
        
        .population {
            text-align: right;
            font-family: 'Courier New', monospace;
            color: #27ae60;
            font-weight: bold;
        }
        
        .area {
            text-align: right;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            font-weight: bold;
        }
        
        .index {
            text-align: center;
            font-weight: bold;
            color: #7f8c8d;
        }
        
        footer {
            background: #1a2980;
            color: white;
            padding: 25px;
            text-align: center;
            border-top: 1px solid #34495e;
        }
        
        .source-link {
            display: inline-block;
            background: linear-gradient(135deg, #26d0ce 0%, #1a2980 100%);
            color: white;
            padding: 12px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 10px;
            border: none;
        }
        
        .source-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .update-info {
            font-size: 0.9rem;
            color: #bdc3c7;
            margin-top: 15px;
        }
        
        .no-data {
            text-align: center;
            padding: 50px;
            color: #7f8c8d;
            font-size: 1.2rem;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            header {
                padding: 25px 15px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            th, td {
                padding: 10px 8px;
                font-size: 0.85rem;
            }
            
            .table-container {
                padding: 15px;
            }
            
            .stats-bar {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Страны мира</h1>
            <p class="subtitle">Полная статистика по всем странам планеты</p>
        </header>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">''' + str(total_countries) + '''</div>
                <div class="stat-label">Всего стран</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">''' + total_population_formatted + '''</div>
                <div class="stat-label">Общее население</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">''' + total_area_formatted + ''' км²</div>
                <div class="stat-label">Общая площадь</div>
            </div>
        </div>
        
        <div class="table-container">
'''
    if countries_data:
        html_content += '''
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Страна</th>
                        <th>Столица</th>
                        <th>Население</th>
                        <th>Площадь (км²)</th>
                    </tr>
                </thead>
                <tbody>
'''
        for i, country in enumerate(countries_data, 1):
            html_content += f'''
                    <tr>
                        <td class="index">{i}</td>
                        <td class="country-name">{country['name']}</td>
                        <td class="capital">{country['capital']}</td>
                        <td class="population">{country['population_formatted']}</td>
                        <td class="area">{country['area_formatted']}</td>
                    </tr>
'''
        
        html_content += '''
                </tbody>
            </table>
'''
    else:
        html_content += '''
            <div class="no-data">
                <p>Нет данных для отображения</p>
            </div>
'''
    html_content += '''
        </div>
        
        <footer>
            <p>Данные предоставлены сайтом:</p>
            <a href="https://www.scrapethissite.com/pages/simple/" 
               class="source-link" 
               target="_blank" 
               rel="noopener noreferrer">
                📊 Посетить источник данных
            </a>
            <div class="update-info">
                Данные обновлены автоматически при запуске программы
            </div>
        </footer>
    </div>
</body>
</html>'''
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("HTML страница создана: index.html")
        return True
    except Exception as e:
        print(f"Ошибка при создании HTML: {e}")
        return False

def open_in_browser():
    try:
        import webbrowser
        html_file = os.path.abspath('index.html')
        if os.path.exists(html_file):
            webbrowser.open(f'file://{html_file}')
            print("Открываю страницу в браузере...")
        else:
            print("HTML файл не найден")
    except ImportError:
        print("Модуль webbrowser не доступен")
    except Exception as e:
        print(f"Не удалось открыть в браузере: {e}")

def main():
    print("="*60)
    print("ПАРСИНГ ДАННЫХ О СТРАНАХ И СОЗДАНИЕ HTML СТРАНИЦЫ")
    print("="*60)
    countries_data = parse_countries_data()
    
    if not countries_data:
        print("Не удалось получить данные. Завершение работы.")
        return
    if save_to_json(countries_data, 'data.json'):
        if generate_html_page(countries_data):
            print("\n" + "="*60)
            print("ВСЁ ГОТОВО!")
            print("="*60)
            print("Данные сохранены в: data.json")
            print("HTML страница создана: index.html")
            print("\nОткройте файл index.html в браузере для просмотра")
            print("\nВы можете:")
            print("1. Открыть файл index.html вручную")
            print("2. Нажать Enter, чтобы открыть автоматически")
            
            try:
                input("\nНажмите Enter для продолжения...")
                open_in_browser()
            except KeyboardInterrupt:
                print("\n\nПрограмма завершена пользователем")
            except:
                print("\nФайл будет открыт в браузере по умолчанию")
                open_in_browser()
    else:
        print(" Ошибка при сохранении данных")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\n Критическая ошибка: {e}")
