from typing import List
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.filters import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, print_vacancies


def user_interaction() -> None:
    api = HeadHunterAPI()
    storage = JSONSaver()

    search_query = input("Введите поисковый запрос: ")
    try:
        top_n = int(input("Введите количество вакансий для вывода ТОП №: "))
    except ValueError:
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например, 100000-150000): ")

    raw = api.get_vacancies(search_query)
    vacancies: List[Vacancy] = Vacancy.cast_to_object_list(raw)
    print(f"Найдено по запросу '{search_query}': {len(vacancies)} вакансий.")

    # Сохраним в файл
    for v in vacancies:
        storage.add_vacancy(v.to_dict())

    # Фильтры/Сортировка/Топ
    filtered = filter_vacancies(vacancies, filter_words)
    print(f"После фильтра по словам {filter_words}: {len(filtered)} вакансий.")
    ranged = get_vacancies_by_salary(filtered, salary_range)
    print(f"После фильтра по диапазону '{salary_range}': {len(ranged)} вакансий.")
    sorted_vs = sort_vacancies(ranged)
    top = get_top_vacancies(sorted_vs, top_n)

    print("\nТоп вакансий:\n")
    print_vacancies(top)


if __name__ == "__main__":
    user_interaction()
