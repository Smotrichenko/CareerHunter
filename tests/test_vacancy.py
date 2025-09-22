from src.vacancy import Vacancy


def test_vacancy_validation_defaults():
    """Тест на создание объекта Vacancy с пустыми и None значениями"""

    v = Vacancy(" ", "", None, None, None, "")
    assert v.title == "Без названия"
    assert v.url == ""
    assert v.currency == "RUR"
    assert v.avg_salary == 0
    assert "Описание не указано" in v.description


def test_vacancy_avg_and_compare():
    """Тест на расчет средней зарплаты и сравнение вакансий"""

    a = Vacancy("A", "u1", 100, 200, "RUR", "desc")
    b = Vacancy("B", "u2", 50, 100, "RUR", "desc")
    c = Vacancy("C", "u3", 0, 0, "RUR", "desc")
    assert a.avg_salary == 150
    assert b.avg_salary == 75
    assert c.avg_salary == 0
    assert a > b
    assert not (a == b)


def test_from_hh_strip_html_and_pick_alternate_url():
    """Тест на создание объекта Vacancy из данных API hh.ru"""

    item = {
        "name": "Dev",
        "alternate_url": "https://hh.ru/vacancy/123",
        "url": "https://api.hh.ru/vacancies/123",
        "salary": {"from": 100, "to": 200, "currency": "RUR"},
        "snippet": {"requirement": "Опыт с <highlighttext>Python</highlighttext>", "responsibility": "Писать код"},
    }
    v = Vacancy.from_hh(item)
    assert v.title == "Dev"
    assert v.url == "https://hh.ru/vacancy/123"
    assert "<highlighttext>" not in v.description
    assert v.salary_from == 100 and v.salary_to == 200 and v.currency == "RUR"
