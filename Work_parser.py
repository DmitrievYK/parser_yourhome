from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument('start-maximized')
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get("https://tvoydom.ru/")
time.sleep(30)

# Функция для парсинга товаров из каждого раздела
def parse_category(driver, category, limit_items=200):
    items = []
    driver.get(category['url'])

    # Дожидаемся загрузки товаров
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'products-list')]//div[contains(@class, 'product product')]"))
    )

    # Обрабатываем страницы
    while len(items) < limit_items:
        try:
            wait = WebDriverWait(driver, 10)
            products = wait.until(EC.presence_of_all_elements_located ((By.XPATH, "//ul[contains(@class, 'products-list')]//div[contains(@class, 'product product')]")))
            print(f"Найдено товаров на странице: {len(products)}")
            driver.execute_script("window.scrollBy(0,3000)")
            time.sleep(5)  # Задержка для загрузки новых товаров
        except TimeoutException:
            print("Не удалось найти продукты на странице. Возможно, это последняя страница или страница не загрузилась.")
            break
        
        for product in products:
            if len(items) >= limit_items:
                break  # Если достигли предела товаров, выходим из цикла
            
            try:
                name = product.find_element(By.XPATH, ".//p[@class='product__name']").text
                items.append({
                    'name': name,
                    'category': category['name'],
                })
            except Exception as e:
                print(f"Ошибка при получении данных товара: {e}")

        # Пытаемся найти кнопку "Показать еще"
        try:
            button_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'js-show-more-list')]//span")))
            actions = ActionChains(driver)
            actions.move_to_element(button_next).click().perform()
            time.sleep(3)  # Задержка для загрузки новых товаров
        except TimeoutException:
            print("Кнопка 'Показать еще' не найдена, выходим...")
            break  # Выходим из цикла, если кнопка не найдена

    return items

# Основной код
categories = [
    {"name": "Мебель", "url": "https://tvoydom.ru/catalog/mebel-1/"},
    {"name": "Посуда", "url": "https://tvoydom.ru/catalog/posuda-1/"},
    {"name": "Текстиль", "url": "https://tvoydom.ru/catalog/tekstil-1/"},
    {"name": "Освещение", "url": "https://tvoydom.ru/catalog/osveschenie-1/"},
    {"name": "Декор и интерьер", "url": "https://tvoydom.ru/catalog/dekor-i-interer-1/"},
    {"name": "Климат", "url": "https://tvoydom.ru/catalog/klimat-1/"},
    {"name": "Мангалы, барбекю", "url": "https://tvoydom.ru/catalog/mangaly-barbekyu-1/"},
    {"name": "Товары для сада", "url": "https://tvoydom.ru/catalog/tovary-dlya-sada-1/"},
    {"name": "Бассейны", "url": "https://tvoydom.ru/catalog/basseyny-i-aksessuary-1/"},
    {"name": "Уборка и хренение", "url": "https://tvoydom.ru/catalog/uborka-i-hranenie-1/"},
    {"name": "Косметика, гигиена", "url": "https://tvoydom.ru/catalog/kosmetika-gigiena-1/"},
    {"name": "Спорт и туризм", "url": "https://tvoydom.ru/catalog/sport-i-turizm-1/"},
    {"name": "Бытовая техника", "url": "https://tvoydom.ru/catalog/bytovaya-tehnika-1/"},
    {"name": "Цифровая техника", "url": "https://tvoydom.ru/catalog/cifrovaya-tehnika-1/"},
    {"name": "Теле-аудио-видео", "url": "https://tvoydom.ru/catalog/tele-audio-video-1/"},
    {"name": "Детские товары", "url": "https://tvoydom.ru/catalog/detskie-tovary-1/"},
    {"name": "Продукты", "url": "https://tvoydom.ru/catalog/produkty-1/"},
    {"name": "Зоотовары", "url": "https://tvoydom.ru/catalog/zootovary-1/"},
    {"name": "Автотовары", "url": "https://tvoydom.ru/catalog/avtotovary-1/"},
    {"name": "Инструменты для ремонта", "url": "https://tvoydom.ru/catalog/instrumenty-dlya-remonta-1/"},
    {"name": "Отделочные материалы", "url": "https://tvoydom.ru/catalog/otdelochnye-materialy-1/"},
    {"name": "Сантехника и товары для ванной", "url": "https://tvoydom.ru/catalog/santehnika-i-tovary-dlya-vannoy-1/"},
    {"name": "Одежда, обувь, аксессуары", "url": "https://tvoydom.ru/catalog/odezhda-obuv-aksessuary-1/"},
    {"name": "Книги", "url": "https://tvoydom.ru/catalog/knigi-1/"}
]

all_products = []

for category in categories:
    try:
        products = parse_category(driver, category, limit_items=200)  # Установленный лимит на количество товаров
        all_products.extend(products)
    except Exception as e:
        print(f"Ошибка при парсинге категории {category['name']}: {e}")

# Сохранить в JSON файл
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)

driver.quit()