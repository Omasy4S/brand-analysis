"""
Скрипт для анализа рейтинга брендов из CSV файлов.
Читает данные о товарах и формирует отчеты по брендам.
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict
from tabulate import tabulate

from reports import get_report


def read_csv_files(file_paths: List[str]) -> List[Dict[str, str]]:
    """
    Читает данные из CSV файлов и объединяет их в один список.
    
    Args:
        file_paths: Список путей к CSV файлам
        
    Returns:
        Список словарей с данными о товарах
    """
    all_data = []
    
    for file_path in file_paths:
        path = Path(file_path)
        
        if not path.exists():
            print(f"Ошибка: файл {file_path} не найден")
            sys.exit(1)
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                all_data.extend(data)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            sys.exit(1)
    
    return all_data


def main():
    """Основная функция скрипта."""
    parser = argparse.ArgumentParser(
        description='Анализ рейтинга брендов из CSV файлов'
    )
    
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам с данными'
    )
    
    parser.add_argument(
        '--report',
        required=True,
        help='Название отчета для формирования'
    )
    
    args = parser.parse_args()
    
    # Читаем данные из файлов
    data = read_csv_files(args.files)
    
    if not data:
        print("Ошибка: файлы не содержат данных")
        sys.exit(1)
    
    # Получаем отчет
    try:
        report_data = get_report(args.report, data)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    
    # Выводим отчет в виде таблицы
    print(tabulate(report_data, headers='keys', tablefmt='grid', showindex=True, stralign='left'))


if __name__ == '__main__':
    main()
