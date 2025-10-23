"""
Тесты для основного модуля скрипта.
"""

import pytest
from pathlib import Path
import tempfile
import csv
from main import read_csv_files


class TestReadCsvFiles:
    """Тесты для функции чтения CSV файлов."""
    
    def test_read_single_file(self, tmp_path):
        """Проверка чтения одного CSV файла."""
        # Создаем временный CSV файл
        csv_file = tmp_path / "test.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
            writer.writeheader()
            writer.writerow({'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.5'})
        
        result = read_csv_files([str(csv_file)])
        
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
        assert result[0]['rating'] == '4.5'
    
    def test_read_multiple_files(self, tmp_path):
        """Проверка чтения нескольких CSV файлов."""
        # Создаем первый файл
        csv_file1 = tmp_path / "test1.csv"
        with open(csv_file1, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
            writer.writeheader()
            writer.writerow({'name': 'product1', 'brand': 'apple', 'price': '999', 'rating': '4.5'})
        
        # Создаем второй файл
        csv_file2 = tmp_path / "test2.csv"
        with open(csv_file2, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
            writer.writeheader()
            writer.writerow({'name': 'product2', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'})
        
        result = read_csv_files([str(csv_file1), str(csv_file2)])
        
        assert len(result) == 2
        assert result[0]['brand'] == 'apple'
        assert result[1]['brand'] == 'samsung'
    
    def test_file_not_found(self):
        """Проверка обработки несуществующего файла."""
        with pytest.raises(SystemExit):
            read_csv_files(['nonexistent.csv'])
    
    def test_empty_file(self, tmp_path):
        """Проверка чтения пустого CSV файла."""
        csv_file = tmp_path / "empty.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
            writer.writeheader()
        
        result = read_csv_files([str(csv_file)])
        
        assert len(result) == 0
