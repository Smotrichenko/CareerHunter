from src.api import HeadHunterAPI


class _DummyResp:
    """Мок класс ответа для имитации вызовов requests.get.
    Позволяет задавать статус-код и возвращаемый JSON."""

    def __init__(self, status_code: int, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def test_hh_get_vacancies(monkeypatch):
    """Тест для метода get_vacancies класса HeadHunterAPI с использованием мок-объекта requests.get."""

    calls = {"n": 0}

    def fake_get(url, headers=None, params=None):
        calls["n"] += 1
        if params and params.get("per_page") == 1:
            return _DummyResp(200, {"items": []})
        return _DummyResp(
            200,
            {
                "items": [
                    {
                        "name": "Dev",
                        "alternate_url": "https://hh.ru/vacancy/1",
                        "salary": {"from": 100, "to": 200, "currency": "RUR"},
                        "snippet": {"requirement": "python"},
                    }
                ]
            },
        )

    monkeypatch.setattr("src.api.requests.get", fake_get)

    api = HeadHunterAPI()
    data = api.get_vacancies("python")
    assert isinstance(data, list)
    assert data and data[0]["name"] == "Dev"
    assert calls["n"] >= 2
