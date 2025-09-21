from typing import List

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], words: List[str]) -> List[Vacancy]:
    """Фильтр вакансий по ключевым словам в названии/описании"""

    if not words:
        return vacancies

    words_lower = [w.lower() for w in words]
    result: List[Vacancy] = []

    for v in vacancies:
        text = (v.title + " " + v.description).lower()
        if any(w in text for w in words_lower):
            result.append(v)
    return result


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтр вакансий по зарплате"""

    if not salary_range:
        return vacancies
    s = salary_range.replace(" ", "")
    parts = s.split("-")
    low = int(parts[0]) if parts and parts[0].isdigit() else 0
    high = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10**6

    def ok(v: Vacancy) -> bool:
        return low <= v.avg_salary <= high

    return [v for v in vacancies if ok(v)]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по убыванию"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """ТОП вакансии после фильтров"""
    if n <= 0:
        return []
    return vacancies[:n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    if not vacancies:
        print("По заданным условиям ничего не найдено.")
        return
    for i, v in enumerate(vacancies, 1):
        print(f"{i}. {v}")
