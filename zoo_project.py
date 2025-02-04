import json
import os

# Базовый класс Animal
class Animal:
    def __init__(self, name, age):
        self.name = name  # Имя животного
        self.age = age    # Возраст животного

    def make_sound(self):
        pass  # Метод будет переопределен в подклассах

    def eat(self):
        print(f"{self.name} is eating.")  # Вывод сообщения о том, что животное ест

# Подклассы, наследуемые от Animal
class Bird(Animal):
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly  # Способность летать

    def make_sound(self):
        print(f"{self.name} says: Chirp!")  # Звук, который издает птица

    def fly(self):
        if self.can_fly:
            print(f"{self.name} is flying.")  # Сообщение о полете
        else:
            print(f"{self.name} cannot fly.")  # Сообщение о неспособности летать

class Mammal(Animal):
    def __init__(self, name, age, has_fur=True):
        super().__init__(name, age)
        self.has_fur = has_fur  # Наличие шерсти

    def make_sound(self):
        print(f"{self.name} says: Grr!")  # Звук, который издает млекопитающее

    def run(self):
        print(f"{self.name} is running.")  # Сообщение о беге

class Reptile(Animal):
    def __init__(self, name, age, is_venomous=False):
        super().__init__(name, age)
        self.is_venomous = is_venomous  # Ядовитость

    def make_sound(self):
        print(f"{self.name} says: Hiss!")  # Звук, который издает рептилия

    def crawl(self):
        print(f"{self.name} is crawling.")  # Сообщение о ползании

# Функция для демонстрации полиморфизма
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()  # Вызов метода make_sound() для каждого животного

# Класс Zoo с использованием композиции
class Zoo:
    def __init__(self, name):
        self.name = name  # Название зоопарка
        self.animals = []  # Список животных
        self.employees = []  # Список сотрудников

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Added {animal.name} to the zoo.")  # Сообщение о добавлении животного

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"Hired {employee.name} as a {employee.position}.")  # Сообщение о найме сотрудника

    def save_to_file(self, filename="zoo_state.json"):
        data = {
            "name": self.name,
            "animals": [{"type": type(animal).__name__, "name": animal.name, "age": animal.age, "attributes": {k: v for k, v in animal.__dict__.items() if k != "name" and k != "age"}} for animal in self.animals],
            "employees": [{"type": type(employee).__name__, "name": employee.name, "position": employee.position, "attributes": {k: v for k, v in employee.__dict__.items() if k != "name" and k != "position"}} for employee in self.employees]
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)  # Сохранение данных в файл в формате JSON
        print(f"Zoo state saved to {filename}.")  # Сообщение о сохранении состояния зоопарка

    def load_from_file(self, filename="zoo_state.json"):
        if not os.path.exists(filename):
            print("No saved state found.")  # Сообщение о том, что файл не найден
            return
        with open(filename, "r") as file:
            data = json.load(file)  # Загрузка данных из файла
        self.name = data["name"]
        self.animals = []
        for animal_data in data["animals"]:
            animal_type = globals()[animal_data["type"]]
            animal_args = {"name": animal_data["name"], "age": animal_data["age"]}
            animal_args.update(animal_data["attributes"])
            animal = animal_type(**animal_args)  # Создание экземпляра животного
            self.animals.append(animal)
        self.employees = []
        for employee_data in data["employees"]:
            employee_type = globals()[employee_data["type"]]
            employee_args = {"name": employee_data["name"]}  # Убираем position, так как он задан в конструкторе
            employee_args.update({k: v for k, v in employee_data["attributes"].items() if k != "position"})
            employee = employee_type(**employee_args)  # Создание экземпляра сотрудника
            self.employees.append(employee)
        print(f"Zoo state loaded from {filename}.")  # Сообщение о загрузке состояния зоопарка

# Классы для сотрудников
class ZooEmployee:
    def __init__(self, name, position):
        self.name = name  # Имя сотрудника
        self.position = position  # Должность сотрудника

class ZooKeeper(ZooEmployee):
    def __init__(self, name):
        super().__init__(name, "Смотритель зоопарка")  # Назначение должности "Смотритель зоопарка"

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")  # Сообщение о кормлении животного

class Veterinarian(ZooEmployee):
    def __init__(self, name):
        super().__init__(name, "Ветеринар")  # Назначение должности "Ветеринар"

    def treat_animal(self, animal):
        print(f"{self.name} is treating {animal.name}.")  # Сообщение о лечении животного

# Пример использования
if __name__ == "__main__":
    # Создание зоопарка
    zoo = Zoo("Казанский зоопарк")  # Создание экземпляра зоопарка

    # Создание животных
    parrot = Bird("Попугай", 2)  # Создание экземпляра птицы
    lion = Mammal("Лев", 5)  # Создание экземпляра млекопитающего
    snake = Reptile("Змея", 3)  # Создание экземпляра рептилии

    # Добавление животных в зоопарк
    zoo.add_animal(parrot)  # Добавление птицы
    zoo.add_animal(lion)  # Добавление млекопитающего
    zoo.add_animal(snake)  # Добавление рептилии

    # Создание сотрудников
    keeper = ZooKeeper("Руслан")  # Создание экземпляра смотрителя
    vet = Veterinarian("Стас")  # Создание экземпляра ветеринара

    # Добавление сотрудников в зоопарк
    zoo.add_employee(keeper)  # Добавление смотрителя
    zoo.add_employee(vet)  # Добавление ветеринара

    # Демонстрация полиморфизма
    print("\nAnimal sounds:")  # Заголовок для звуков животных
    animal_sound(zoo.animals)  # Вызов функции для демонстрации звуков

    # Использование методов сотрудников
    keeper.feed_animal(lion)  # Кормление льва
    vet.treat_animal(snake)  # Лечение змеи

    # Сохранение состояния зоопарка
    zoo.save_to_file()  # Сохранение в файл

    # Загрузка состояния зоопарка
    new_zoo = Zoo("New Zoo")  # Создание нового зоопарка
    new_zoo.load_from_file()  # Загрузка из файла

    # Демонстрация загруженного состояния
    print("\nLoaded animal sounds:")  # Заголовок для загруженных звуков
    animal_sound(new_zoo.animals)  # Вызов функции для демонстрации звуков