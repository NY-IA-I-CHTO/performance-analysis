import argparse
import csv
from tabulate import tabulate

def read_file(path):
    data = []
    for file_path in path:
        with open(file_path, 'r', encoding='utf-8') as file:
            read_file = csv.DictReader(file, delimiter=',') # преобразуем строку в словарь, первая строка ключи
            for row in read_file:
                data.append(row) # получаем список словарей
    return data


def performance(data):
    performance_sum = {}
    performance_count = {}

    for value in data:
        position = value['position']
        performance = float(value['performance'])
        if position not in performance_sum:
            performance_sum[position] = 0.0
            performance_count[position] = 0

        performance_sum[position] += performance
        performance_count[position] += 1

    result = []
    for position in performance_sum:
        avg_performance = performance_sum[position] / performance_count[position]
        result.append([position, round(avg_performance, 2)])

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def main():
    parser = argparse.ArgumentParser(description='Анализ эффективности')
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--report', required=True)

    args = parser.parse_args()
    data = read_file(args.files)
    result_data = performance(data)

    print(tabulate(result_data, headers=['position', 'performance']))

if __name__ == '__main__':
    main()