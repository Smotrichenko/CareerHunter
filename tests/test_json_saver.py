from src.json_saver import JSONSaver


def test_json_add_get_delete(tmp_path):
    filename = tmp_path / "vacancies.json"
    saver = JSONSaver(str(filename))

    # изначально пусто
    assert saver.get_vacancies() == []

    row1 = {
        "title": "Dev",
        "url": "http://example.com/1",
        "salary_from": 100000,
        "salary_to": 150000,
        "currency": "RUR",
        "description": "python developer",
    }
    row2 = {
        "title": "Data",
        "url": "http://example.com/2",
        "salary_from": 200000,
        "salary_to": 0,
        "currency": "RUR",
        "description": "data engineer",
    }

    saver.add_vacancy(row1)
    saver.add_vacancy(row1)  # дубли не должны добавляться
    saver.add_vacancy(row2)

    data = saver.get_vacancies()
    assert len(data) == 2

    # фильтрация по ключевому слову
    only_py = saver.get_vacancies(keyword="python")
    assert len(only_py) == 1 and only_py[0]["url"] == "http://example.com/1"

    # фильтрация по зарплате
    in_range = saver.get_vacancies(salary_from=120000, salary_to=300000)
    # row1 avg = 125000, row2 avg = 200000 -> обе попадают
    assert {r["url"] for r in in_range} == {"http://example.com/1", "http://example.com/2"}

    # удаление
    saver.delete_vacancy(url="http://example.com/1")
    left = saver.get_vacancies()
    assert len(left) == 1 and left[0]["url"] == "http://example.com/2"
