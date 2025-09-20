from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class VacanciesAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        self._base_url = base_url
        self._headers = headers or {"User-Agent": "Vacancies-Client"}

    @abstractmethod
    def _connect(self) -> None:
        """Проверка соединения с API"""
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Получение списка вакансий по ключевому слову"""
        raise NotImplementedError


class HeadHunterAPI(VacanciesAPI):
    """Класс работы с API hh.ru"""

    def __init__(self) -> None:
        super().__init__(base_url="https://api.hh.ru/vacancies", headers=({"User-Agent": "HH-User-Agent"}))
        self._params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100}

    def _connect(self) -> None:
        resp = requests.get(self._base_url, headers=self._headers, params={"per_page": 1})
        if resp.status_code != 200:
            raise ConnectionError(f"Соединение с API недоступно: {resp.status_code}")

    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Запрос вакансий с hh.ru по ключевому слову"""

        self._connect()
        items: List[Dict[str, Any]] = []
        self._params["text"] = query
        self._params["page"] = 0

        for _ in range(2):
            resp = requests.get(self._base_url, headers=self._headers, params=self._params)
            if resp.status_code != 200:
                break
            data = resp.json()
            page_items = data.get("items", [])
            items.extend(page_items)
            self._params["page"] += 1
        return items
