"""
Тесты для модуля формирования отчетов.
"""

import pytest
from reports import AverageRatingReport, get_report


class TestAverageRatingReport:
    """Тесты для отчета по среднему рейтингу."""
    
    def test_simple_average(self):
        """Проверка расчета среднего рейтинга для одного бренда."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.5'},
            {'name': 'product2', 'brand': 'apple', 'price': '899', 'rating': '4.7'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
        assert result[0]['rating'] == 4.6
    
    def test_multiple_brands(self):
        """Проверка работы с несколькими брендами."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
            {'name': 'product2', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
            {'name': 'product3', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert len(result) == 3
        assert result[0]['brand'] == 'apple'
        assert result[0]['rating'] == 4.9
        assert result[1]['brand'] == 'samsung'
        assert result[2]['brand'] == 'xiaomi'
    
    def test_sorting_by_rating(self):
        """Проверка сортировки по рейтингу в порядке убывания."""
        data = [
            {'name': 'product1', 'brand': 'brand_c', 'price': '100', 'rating': '3.0'},
            {'name': 'product2', 'brand': 'brand_a', 'price': '200', 'rating': '5.0'},
            {'name': 'product3', 'brand': 'brand_b', 'price': '150', 'rating': '4.0'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert result[0]['brand'] == 'brand_a'
        assert result[1]['brand'] == 'brand_b'
        assert result[2]['brand'] == 'brand_c'
    
    def test_empty_data(self):
        """Проверка работы с пустыми данными."""
        data = []
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert len(result) == 0
    
    def test_invalid_rating(self):
        """Проверка обработки невалидных рейтингов."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': 'invalid'},
            {'name': 'product2', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert len(result) == 1
        assert result[0]['brand'] == 'samsung'
    
    def test_rounding(self):
        """Проверка округления среднего значения."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.55'},
            {'name': 'product2', 'brand': 'apple', 'price': '899', 'rating': '4.54'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        # (4.55 + 4.54) / 2 = 4.545, округляется до 4.54
        assert result[0]['rating'] == 4.54
    
    def test_empty_brand(self):
        """
        Проверка обработки пустых брендов.
        Записи с пустым брендом должны пропускаться как невалидные данные.
        """
        data = [
            {'name': 'product1', 'brand': '', 'price': '999', 'rating': '4.5'},
            {'name': 'product2', 'brand': 'apple', 'price': '899', 'rating': '4.7'},
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
    
    def test_rating_out_of_range(self):
        """
        Проверка валидации диапазона рейтингов.
        Рейтинги должны быть в диапазоне 0-5 (стандарт для товаров).
        Значения вне диапазона пропускаются.
        """
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '-1'},  # Отрицательный
            {'name': 'product2', 'brand': 'apple', 'price': '899', 'rating': '6.0'},  # Больше 5
            {'name': 'product3', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},  # Валидный
        ]
        
        report = AverageRatingReport()
        result = report.generate(data)
        
        # Только samsung должен попасть в результат
        assert len(result) == 1
        assert result[0]['brand'] == 'samsung'
        assert result[0]['rating'] == 4.8


class TestGetReport:
    """Тесты для функции получения отчета."""
    
    def test_get_average_rating_report(self):
        """Проверка получения отчета по среднему рейтингу."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.5'},
        ]
        
        result = get_report('average-rating', data)
        
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
    
    def test_unknown_report(self):
        """Проверка обработки неизвестного отчета."""
        data = [
            {'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.5'},
        ]
        
        with pytest.raises(ValueError) as exc_info:
            get_report('unknown-report', data)
        
        assert 'не найден' in str(exc_info.value)
