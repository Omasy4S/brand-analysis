# Анализ рейтинга брендов

Скрипт для обработки CSV файлов с данными о товарах и формирования отчетов по брендам.

## Установка

```bash
pip install -r requirements.txt
```

## Использование

Запуск скрипта с указанием файлов и типа отчета:

```bash
python main.py --files products1.csv products2.csv --report average-rating
```

### Параметры

- `--files` - пути к одному или нескольким CSV файлам с данными
- `--report` - название отчета (доступные: `average-rating`)

## Формат CSV файлов

CSV файлы должны содержать следующие колонки:
- `name` - название товара
- `brand` - бренд товара
- `price` - цена товара
- `rating` - рейтинг товара

Пример:
```
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
```

## Доступные отчеты

### average-rating
Показывает средний рейтинг по каждому бренду. Бренды сортируются по рейтингу в порядке убывания.

## Запуск тестов

```bash
pytest
```

Проверка покрытия кода тестами:

```bash
pytest --cov=. --cov-report=term-missing
```

## Добавление новых отчетов

Чтобы добавить новый отчет:

1. Создайте класс отчета в файле `reports.py`
2. Реализуйте метод `generate()` для формирования данных отчета
3. Добавьте новый отчет в словарь `AVAILABLE_REPORTS`

Пример:

```python
class AveragePriceReport:
    def generate(self, data: List[Dict[str, str]]) -> List[Dict[str, any]]:
        # Собираем цены по брендам
        brand_prices = {}
        for item in data:
            brand = item.get('brand', '').strip()
            price = float(item.get('price', '0'))
            if brand not in brand_prices:
                brand_prices[brand] = []
            brand_prices[brand].append(price)
        
        # Вычисляем среднюю цену
        result = []
        for brand, prices in brand_prices.items():
            avg_price = sum(prices) / len(prices)
            result.append({'brand': brand, 'price': round(avg_price, 2)})
        
        return result

AVAILABLE_REPORTS = {
    'average-rating': AverageRatingReport(),
    'average-price': AveragePriceReport(),
}
```
