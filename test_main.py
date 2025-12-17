import pytest
import os
import tempfile
from main import read_file, performance


def test_read_file_basic(): # тест считывания данных
    csv_content = "name,position,performance\nDavid Chen,Developer,4.6\nElena Popova,Backend Developer,4.8"  # Создаем временный CSV файл

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        data = read_file([temp_path])
        assert len(data) == 2

        assert data[0]['name'] == 'David Chen'
        assert data[0]['position'] == 'Developer'
        assert data[0]['performance'] == '4.6'

        assert data[1]['name'] == 'Elena Popova'
        assert data[1]['position'] == 'Backend Developer'
        assert data[1]['performance'] == '4.8'
    finally:
        os.unlink(temp_path)


def test_read_file_empty(): # тест для заголовков
    csv_content = "name,position,performance\n"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        data = read_file([temp_path])
        assert data == []
    finally:
        os.unlink(temp_path)


def test_read_file_multiple(): # тест для нескольких файлов
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f1:
        f1.write("name,position,performance\nChris Wilson,DevOps Engineer,4.7")
        path1 = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f2:
        f2.write("name,position,performance\nRobert Kim,Data Engineer,4.7")
        path2 = f2.name

    try:
        data = read_file([path1, path2])

        assert len(data) == 2

        names = [row['name'] for row in data]
        assert 'Chris Wilson' in names
        assert 'Robert Kim' in names
    finally:
        os.unlink(path1)
        os.unlink(path2)


def test_performance_basic(): # avg по одной должности
    data = [
        {'position': 'Data Scientist', 'performance': '4.0'},
        {'position': 'Data Scientist', 'performance': '5.0'}
    ]

    result = performance(data)

    assert len(result) == 1
    assert result[0][0] == 'Data Scientist'
    assert result[0][1] == 4.5


def test_performance_two_positions(): # 2 разные должности
    data = [
        {'position': 'Data Scientist', 'performance': '4.5'},
        {'position': 'Mobile Developer', 'performance': '4.0'},
        {'position': 'Data Scientist', 'performance': '5.5'},
        {'position': 'Mobile Developer', 'performance': '4.5'}
    ]

    result = performance(data)

    assert len(result) == 2

    for position, avg in result:
        if position == 'Data Scientist':
            assert avg == 5.0
        elif position == 'Mobile Developer':
            assert avg == 4.25


def test_performance_sorting(): # тест на сортировку
    data = [
        {'position': 'QA Engineer', 'performance': '4.8'},
        {'position': 'Backend Developer', 'performance': '4.6'},
        {'position': 'Frontend Developer', 'performance': '4.7'},
        {'position': 'QA Engineer', 'performance': '4.8'}
    ]

    result = performance(data)

    assert result[0][0] == 'QA Engineer' and result[0][1] == 4.8
    assert result[1][0] == 'Frontend Developer' and result[1][1] == 4.7
    assert result[2][0] == 'Backend Developer' and result[2][1] == 4.6


def test_performance_error_handling(): # тест на некорректные данные
    data = [
        {'position': 'DevOps Engineer'}
    ]

    with pytest.raises(KeyError):
        performance(data)


def test_performance_invalid_number(): # тест на не число
    data = [
        {'position': 'Data Engineer', 'performance': 'не_число'}
    ]

    with pytest.raises(ValueError):
        performance(data)
