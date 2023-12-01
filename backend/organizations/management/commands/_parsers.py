import random
import string
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from mimesis import Generic, Internet
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
        region_code_choices: str = string.digits
        short_names: Tuple[str] = tuple(self.forms.keys())

        for _ in range(self.num):
            address = (f'{g.address.address()}, '
                       f'{g.address.city()}, '
                       f'{g.address.region()}, '
                       f'{g.address.zip_code()}').upper()
            short_name_abbr: str = random.choice(short_names)
            full_name_abbr: str = self.forms[short_name_abbr]
            word: str = f'"{g.text.word().upper()}"'
            region_code: str = (random.choice(region_code_choices)
                                + random.choice(region_code_choices))
            org = Organization(
                full_name=f'{full_name_abbr} {word}',
                short_name=f'{word}',
                inn=g.russia_provider.inn(),
                factual_address=address,
                region_code=region_code,
                longitude=g.address.longitude(),
                latitude=g.address.latitude(),
                site=internet.url()
            )
            orgs.append(org)

        stats = {
            'counter_new': {
                "verbose_name": 'Сгенерированных организаций залито',
                "value": self.num
            }
        }
        return orgs, stats
