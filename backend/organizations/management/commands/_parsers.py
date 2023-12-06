import random
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from mimesis import Generic, Internet, Person, Text
from mimesis.builtins import RussiaSpecProvider
from mimesis.locales import Locale

from organizations.models import Organization


class OrgParser(ABC):
    """
    Парсер сведений об организациях.

    Методы
    -------
    parse()
        Абстрактный метод, реализующий логику сбора данных об организациях
    """

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        Определяет стратегию парсинга, которую необходимо описывать
        при наследовании.
        """

        pass


class GenerateOrgParser(OrgParser):
    """
    Создает приближенные к реальным данные об организациях.

    Атрибуты
    ----------
    num : int (по умолчанию 10 000)
        Количество организаций, которые нужно создать.

    Методы
    -------
    parse()
        Реализует логику генерации несуществующих организаций для демонстрации
    """

    forms: Dict[str, str] = {
        "ОАО": "ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО",
        "АО": "АКЦИОНЕРНОЕ ОБЩЕСТВО",
        "БУЗ": "БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ",
        "ООО": "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ",
        "ФКУ": "ФЕДЕРАЛЬНОЕ КАЗЕНОЕ УЧРЕЖДЕНИЕ"
    }

    def __init__(self, num: int = 10000):
        self.num = num

    def parse(
            self,
            *args,
            **kwargs
    ) -> Tuple[List['Organization'], Dict[str, Dict[str, str]]]:
        """
        Возвращает кортеж, состоящий из:
        [0] Список сгенерированных организаций, которые необходимо
        добавить в БД.
        [1] Словарь статистических штучек (сколько чего обработано, добавлено).
        """

        orgs: List['Organization'] = []
        internet = Internet()
        g = Generic(locale=Locale.RU)
        g.add_provider(RussiaSpecProvider)
        short_names: Tuple[str] = tuple(self.forms.keys())
        for _ in range(self.num):
            short_name_abbr: str = random.choice(short_names)
            full_name_abbr: str = self.forms[short_name_abbr]
            word: str = f'"{g.text.word().upper()}"'
            org = Organization(
                full_name=f'{full_name_abbr} {word}',
                short_name=f'{word}',
                inn=g.russia_provider.inn(),
                factual_address=g.address.address(),
                longitude=round(random.uniform(36, 36.4), 5),
                latitude=round(random.uniform(54.4, 54.6), 5),
                site=internet.url(),
                email=Person(locale=Locale.RU).email(),
                is_gov=random.choice([True, False]),
                is_full_time=random.choice([True, False]),
                about=Text(locale=Locale.RU).text(random.randint(2, 10))
            )
            orgs.append(org)

        stats = {
            'counter_new': {
                "verbose_name": 'Сгенерированных организаций залито',
                "value": self.num
            }
        }
        return orgs, stats
