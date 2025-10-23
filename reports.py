"""
Модуль для формирования отчетов по данным о товарах.
"""

from typing import List, Dict


class AverageRatingReport:
    """Отчет по среднему рейтингу брендов."""
    
    def generate(self, data: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Формирует отчет со средним рейтингом по каждому бренду.
        Бренды сортируются по рейтингу в порядке убывания.
        
        Args:
            data: Список словарей с данными о товарах
            
        Returns:
            Список словарей с брендами и их средним рейтингом
        """
        # Собираем рейтинги по брендам
        brand_ratings = {}
        
        for item in data:
            brand = item.get('brand', '').strip()
            rating_str = item.get('rating', '0')
            
            try:
                rating = float(rating_str)
            except ValueError:
                continue
            
            if brand not in brand_ratings:
                brand_ratings[brand] = []
            
            brand_ratings[brand].append(rating)
        
        # Вычисляем средний рейтинг для каждого бренда
        result = []
        for brand, ratings in brand_ratings.items():
            avg_rating = sum(ratings) / len(ratings)
            result.append({
                'brand': brand,
                'rating': round(avg_rating, 2)
            })
        
        # Сортируем по рейтингу в порядке убывания
        result.sort(key=lambda x: x['rating'], reverse=True)
        
        return result


# Словарь доступных отчетов
AVAILABLE_REPORTS = {
    'average-rating': AverageRatingReport(),
}


def get_report(report_name: str, data: List[Dict[str, str]]) -> List[Dict[str, any]]:
    """
    Получает и генерирует отчет по названию.
    
    Args:
        report_name: Название отчета
        data: Данные для формирования отчета
        
    Returns:
        Данные отчета
        
    Raises:
        ValueError: Если отчет с таким названием не найден
    """
    report = AVAILABLE_REPORTS.get(report_name)
    
    if report is None:
        available = ', '.join(AVAILABLE_REPORTS.keys())
        raise ValueError(
            f"Отчет '{report_name}' не найден. "
            f"Доступные отчеты: {available}"
        )
    
    return report.generate(data)
