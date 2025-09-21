from src.filters import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies
from src.vacancy import Vacancy


def _vac(title: str, s: int) -> Vacancy:
    return Vacancy(title, f"url-{title}", s, s, "RUR", "python разработчик")


def test_filter_and_sort_and_top():
    items = [_vac("A", 100000), _vac("B", 200000), _vac("C", 150000)]

    # фильтр по словам
    filtered = filter_vacancies(items, ["python"])
    assert len(filtered) == 3

    # фильтр по зарплате
    ranged = get_vacancies_by_salary(items, "120000-180000")
    assert {v.title for v in ranged} == {"C"}

    # сортировка по зарплате по убыванию
    sorted_vs = sort_vacancies(items)
    assert [v.title for v in sorted_vs] == ["B", "C", "A"]

    # топ
    top2 = get_top_vacancies(sorted_vs, 2)
    assert [v.title for v in top2] == ["B", "C"]

    # n больше длины — возвращаем всё, что есть
    top10 = get_top_vacancies(sorted_vs, 10)
    assert len(top10) == 3
