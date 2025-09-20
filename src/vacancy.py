from typing import Any, Dict, List


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("title", "url", "salary_from", "salary_to", "currency", "description")

    def __init__(
        self, title: str, url: str, salary_from: int, salary_to: int, currency: str, description: str
    ) -> None:
        self.title = self._validate_str(title, "Без названия")
        self.url = self._validate_str(url, "")
        self.salary_from, self.salary_to, self.currency = self._validate_str(salary_from, salary_to, currency)
        self.description = self._validate_str(description, "Без названия")

    # Приватная валидация данных
    def _validate_str(self, value: Any, default: str) -> str:
        return value.strip() if isinstance(value, str) and value.strip() else default

    def _validate_salary(self, s_from: Any, s_to: Any, cur: Any) -> None:
        def _to_int(x: Any) -> int:
            try:
                return int(x)
            except (TypeError, ValueError):
                return 0

        low = _to_int(s_from)
        high = _to_int(s_to)
        if high and low and high < low:
            low, high = high, low
        currency = cur if isinstance(cur, str) and cur.strip() else "RUR"
        return low, high, currency

    @property
    def avg_salary(self) -> int:
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) // 2
        return self.salary_to or self.salary_from or 0

    def __lt__(self, other: "Vacancy") -> bool:
        return self.avg_salary < other.avg_salary

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return False
        return self.avg_salary == other.avg_salary

    @classmethod
    def from_hh(cls, item: Dict[str, Any]) -> "Vacancy":
        name = item.get("name")
        url = item.get("url") or item.get("alternate_url") or ""
        salary = item.get("salary") or {}
        description = item.get("snippet", {}).get("requirement") or item.get("snippet", {}).get("responsibility") or ""
        return cls(
            title=name or "Без названия",
            url=url,
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            currnecy=salary.get("currency"),
            description=description or "Описание не указано",
        )

    @classmethod
    def cast_to_object_list(cls, data: List[Dict[str, Any]]) -> List["Vacancy"]:
        return [cls.from_hh(item) for item in data]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "description": self.description,
        }

    def __str__(self) -> str:
        sal = self.avg_salary
        sal_text = f"Зарплата: {sal} {self.currency}" if sal else "Зарплата не указана"
        return f"{self.title}\n{sal_text}\n{self.url}\n{self.description}"
