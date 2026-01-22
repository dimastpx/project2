import json
from datetime import datetime

print("Hello")

DATA_EXAMPLE = {"operations": [{"money": 0,
                                "date": "19.01.2026",
                                "description": "Тестовая операция",
                                "category": "Переводы",
                                "type": "income"}],
                "income_category": ["Зарплата", "Стипендия", "Переводы", "Деп"],
                "expense_category": ["Еда", "Техника", "Продукты", "Деп"]}

def date_easter_check(date: datetime):
    match (date.day, date.month, date.year):
        case (1, 1, 1):
            return "Камни не считаются деньгами"
        case (1, 1, _):
            return "С новым годом!"
        case (25, 12, _) | (7, 1, _):
            return "С рождеством!"
        case (5, 11, 1955) | (21, 10, 2015):
            return "Не встретьте самого себя, это может вызвать разрыв временного континуума"
        case (8, 3, _):
            return "Убедитесь, что у вас добавлена категория \"Цветы\" в расходах, если только вы не продавец"
        case (24, 2, 2022):
            return "Думаю, после этого ваш бюджет мог пострадать"
        case (9, 5, 1945):
            return "Победа!"
        case (9, 5, _):
            return "С днём победы"
        case (30, _, _) | (31, _, _) | (28, 2, _) | (29, 2, _):
            return "Зарплата или стипендия уже пришли?"
        case (_, _, 2077):
            return "Я не играл"
        case (3, 9, _):
            return "Я календарь переверну..."

        case _:
            return False




class Main:
    def __init__(self):
        try:
            self.load()
        except FileNotFoundError:
            self.data = DATA_EXAMPLE
            self.save()
        except json.decoder.JSONDecodeError:
            self.data = DATA_EXAMPLE
            self.save()

        while True:
            choice = None
            while choice is None:
                print("=" * 50)
                print("Что хотите сделать?:")
                print("0 - Выйти")
                print("1 - Добавить доход")
                print("2 - Добавить расход")
                print("3 - Посмотреть общую статистику")
                print("4 - Посмотреть все записи")
                print("5 - Добавить категорию")

                try:
                    choice = int(input("Выберите действие: "))
                except ValueError:
                    choice = None

                if not(0 <= choice <= 5):
                    choice = None

            match choice:
                case 0:
                    break
                case 1:
                    self.add_income()
                case 2:
                    self.add_expense()
                case 3:
                    self.show_general()
                case 4:
                    self.show_all()
                case 5:
                    self.add_category()

    def add_income(self):
        income = {}
        try:
            money = float(input("Введите сумму дохода в рублях: "))
            income["money"] = abs(money)

            print("Выберите категорию(чтобы отменить процесс добавления дохода введите не число): ")
            choice = None
            while choice is None:
                for i, cat in enumerate(self.data["income_category"]):
                    print(f"{i + 1}. {cat}")

                choice = int(input("Введите число: "))

                if not(1 <= choice <= len(self.data["income_category"])):
                    choice = None
                    print("Вы выбрали что-то не то")
            income["category"] = self.data["income_category"][choice - 1]

            print("Дата (dd.mm.yyyy)")

            date = input("Выедите дату строго формата дд.мм.гггг (оставьте пустым для сегодняшней): ")
            if date == "":
                date = datetime.today().strftime("%d.%m.%Y")
            date = datetime.strptime(date, "%d.%m.%Y")

            if date_easter_check(date):
                print(date_easter_check(date))

            income["date"] = date.strftime("%d.%m.%Y")

            description = input("Добавьте описание по желанию: ")
            income["description"] = description

            income["type"] = "income"

            self.data["operations"].append(income)
            self.save()

        except ValueError:
            print("Ошибка. Вы ввели не число или неверно ввели дату")

    def add_expense(self):
        expense = {}
        try:
            money = float(input("Введите сумму расхода в рублях: "))
            expense["money"] = abs(money)

            print("Выберите категорию(чтобы отменить процесс добавления расхода введите не число): ")
            choice = None
            while choice is None:
                for i, cat in enumerate(self.data["expense_category"]):
                    print(f"{i + 1}. {cat}")

                choice = int(input("Введите число: "))

                if not(1 <= choice <= len(self.data["expense_category"])):
                    choice = None
            expense["category"] = self.data["expense_category"][choice - 1]

            print("Дата (dd.mm.yyyy)")

            date = input("Выедите дату строго формата дд.мм.гггг (оставьте пустым для сегодняшней): ")
            if date == "":
                date = datetime.today().strftime("%d.%m.%Y")
            date = datetime.strptime(date, "%d.%m.%Y")

            if date_easter_check(date):
                print(date_easter_check(date))

            expense["date"] = date.strftime("%d.%m.%Y")

            description = input("Добавьте описание по желанию: ")
            expense["description"] = description

            expense["type"] = "expense"

            self.data["operations"].append(expense)
            self.save()

        except ValueError:
            print("Ошибка. Вы ввели не число или неверно ввели дату")

    def show_general(self):
        print("="*50)
        income_count = float(sum(i["money"] for i in self.data["operations"] if i["type"] == "income"))
        expenses_count = float(sum(i["money"] for i in self.data["operations"] if i["type"] == "expense"))

        print(f"Доходы: {income_count}")
        print(f"Расходы: {expenses_count}")
        print(f"Итог: {income_count - expenses_count}")

        try:
            ratio = (expenses_count / income_count) * 100
            print(f"Процент доходов от расходов {ratio}%")
            if ratio > 100:
                print("Ваши расходы превышают доходы")
        except ZeroDivisionError:
            print("Доходы равны нулю, поэтому процент показать не получится")

    def add_category(self):
        print("="*50)
        print("Какую категорию добавить?")
        choice = None
        while choice is None:
            print("1 - Доход")
            print("2 - Расход")
            try:
                choice = int(input("Ваш выбор: "))
                if not(1 <= choice <= 2):
                    choice = None
            except ValueError:
                choice = None

        name = input("Напишите название категории: ")
        match choice:
            case 1:
                self.data["income_category"].append(name)
            case 2:
                self.data["expense_category"].append(name)
        print("Категория добавлена")

        print("Все категории:")
        print("Доходы:")
        print()
        for i in self.data["income_category"]:
            print(i)
        print("Расходы:")
        print()
        for i in self.data["expense_category"]:
            print(i)

        self.save()

    def show_all(self):
        print("="*25 + "Отчёт" + "="*25)
        lst = sorted(self.data["operations"], key=lambda x: datetime.strptime(x['date'], "%d.%m.%Y"),
                     reverse=True)
        for i in lst:
            print_op(i)

        self.show_general()

        print("Выберите действия:")
        print("0 - Вернуться в меню")
        print("1 - Фильтр по категориям")
        print("2 - Фильтр по дате")

        choice = None
        while choice is None:
            choice = input("Введите ваш выбор: ")
            match choice:
                case "0":
                    pass
                case "1":
                    self.show_filter_category()
                case "2":
                    self.show_filter_date()
                case _:
                    choice = None
                    print("Ошибка: вы ввели что-то не то")

    def show_filter_category(self):
        print("="*50)
        choice = None
        while choice is None:
            print("Выберите категорию:")
            cats = list(set(self.data["income_category"] + self.data["expense_category"]))
            for i, cat in enumerate(cats):
                print(f"{i + 1}. {cat}")

            try:
                choice = int(input("Введите ваш выбор: "))

                if not(1 <= choice <= len(cats)):
                    choice = None
                else:
                    category = cats[choice - 1]


                    if (category.capitalize() in self.data["income_category"]
                            and category.capitalize() in self.data["expense_category"]):

                        print(f"Категория \"{category}\" находится одновременно и в доходах, и в расходах, выберите одно")
                        choice2 = None
                        while choice2 is None:
                            print("1 - Доходы")
                            print("2 - Расходы")
                            choice2 = input("Выберите одно: ")
                            match choice2:
                                case "1":
                                    lst = (i for i in self.data["operations"] if i["type"] == "income"
                                           and i["category"] == category)
                                    print_op_list(lst)

                                case "2":
                                    lst = (i for i in self.data["operations"] if i["type"] == "expense"
                                           and i["category"] == category)
                                    print_op_list(lst)

                                case _:
                                    print("Ошибка: вы выбрали что то не то")
                                    choice2 = None

                    elif category.capitalize() in self.data["income_category"]:
                        lst = (i for i in self.data["operations"] if i["type"] == "income"
                               and i["category"] == category)
                        print_op_list(lst)

                    elif category.capitalize() in self.data["expense_category"]:
                        lst = (i for i in self.data["operations"] if i["type"] == "expense"
                               and i["category"] == category)
                        print_op_list(lst)



            except ValueError:
                choice = None
                print("Вы ввели не число")



    def show_filter_date(self):
        print("="*50)
        try:
            date = input("Выедите дату строго формата дд.мм.гггг (оставьте пустым для сегодняшней): ")
            if date == "":
                date = datetime.today().strftime("%d.%m.%Y")
            date = datetime.strftime(datetime.strptime(date, "%d.%m.%Y"), "%d.%m.%Y")

            lst = (i for i in self.data["operations"] if i["date"] == date)
            print_op_list(lst)

        except ValueError:
            print("Ошибка: неверный формат даты")

    def save(self):
        with open("save.json", "w") as f:
            json.dump(self.data, f)

    def load(self):
        with open("save.json", "r") as f:
            self.data = json.load(f)

def print_op_list(lst):
    lst = list(lst)
    if not lst:
        print("Операции по заданным фильтрам отсутствуют")
    else:
        for i in lst:
            print_op(i)

def print_op(operation):
    print(
        f"||Вид: {"Доход" if operation["type"] == "income" else "Расход"} | "
        f"Сумма: {operation['money']} | Дата:"
        f"{operation["date"]} | Категория: {operation["category"]}||")



Main()