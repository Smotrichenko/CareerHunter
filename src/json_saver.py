import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseStorage(ABC):
    """Абстрактный класс для сохранения файлов"""

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(
        self, keyword: str | None = None, salary_from: int | None = None, salary_to: int | None = None
    ) -> List[Dict[str, Any]]:
        return NotImplementedError

    @abstractmethod
    def delete_vacancy(self, url: str | None = None) -> None:
        return NotImplementedError

    # Заглушка для будущих БД-интеграций
    def update_vacancy(self, *args, **kwargs) -> None:
        pass


class JSONSaver(BaseStorage):
    """Хранение данных в JSON файле без дублей вакансий"""

    def __init__(self, filename: str | None = None) -> None:
        self._filename = filename or os.path.join("data", "vacancies.json")
        os.makedirs(os.path.dirname(self._filename), exist_ok=True)
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def _read_all(self) -> List[Dict[str, Any]]:
        with open(self._filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, rows: List[Dict[str, Any]]) -> None:
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        rows = self._read_all()
        urls = {r.get("url") for r in rows}
        if vacancy.get("url") not in urls:
            rows.append(vacancy)
            self._write_all(rows)

    def get_vacancies(
        self, keyword: str | None = None, salary_from: int | None = None, salary_to: int | None = None
    ) -> List[Dict[str, Any]]:
        rows = self._read_all()
        result = rows
        if keyword:
            kw = keyword.lower()
            result = [r for r in result if kw in (r.get("title", "").lower() + " " + r.get("description", "").lower())]
        if salary_from is not None or salary_to is not None:
            low = salary_from or 0
            high = salary_to or 10**6

            def ok(r: Dict[str, Any]) -> bool:
                s_from = int(r.get("salary_from") or 0)
                s_to = int(r.get("salary_to") or 0)
                avg = (s_from + s_to) // 2 if s_from and s_to else (s_to or s_from)
                return low <= (avg or 0) <= high

            result = [r for r in result if ok(r)]
        return result

    def delete_vacancy(self, url: str | None = None) -> None:
        if not url:
            return
        rows = self._read_all()
        rows = [r for r in rows if r.get("url") != url]
        self._write_all(rows)
