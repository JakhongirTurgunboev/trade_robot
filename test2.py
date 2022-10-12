import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:  # Используйте нижний регистр для имен переменных
            if record.date == dt.datetime.now().date():
                today_stats = today_stats + record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                    7 > (today - record.date).days >= 0  # Упростил цепочку
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Получает остаток калорий на сегодня"""
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'    # Не нужно использовать скобки, будьте последовательны в своем коде


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                usd_rate=USD_RATE, eur_rate=EURO_RATE):  # Используйте заглавные буквы
        # только для КОНСТАНТОВ. Следуйте правилам PEP8
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= usd_rate
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= eur_rate
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # cash_remained == 1.00. Этот код не имеет никакого эффекта
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()


if __name__ == "__main__":
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

    print(cash_calculator.get_today_cash_remained("rub"))
    # должно напечататься
    # На сегодня осталось 555 руб
