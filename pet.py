import os


class Pet:
    def __init__(self, name, pet_type, age):
        self.name = name
        self.pet_type = pet_type
        self.age = age
        self.hunger = 50
        self.mood = 50
        self.energy = 50
        self.health = 100

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.health = min(100, self.health + 5)
        print(f"{self.name} покормлен! Голод: {self.hunger}")

    def play(self):
        self.mood = min(100, self.mood + 10)
        self.energy = max(0, self.energy - 15)
        self.hunger = min(100, self.hunger + 5)
        print(f"{self.name} поиграл! Настроение: {self.mood}")

    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.health = min(100, self.health + 5)
        print(f"{self.name} поспал! Энергия: {self.energy}")

    def walk(self):
        self.energy = max(0, self.energy - 10)
        self.mood = min(100, self.mood + 15)
        self.health = min(100, self.health + 5)
        print(f"{self.name} погулял! Настроение: {self.mood}")

    def show_info(self):
        print(f"\n=== {self.name} ({self.pet_type}, {self.age} лет) ===")
        print(f"Голод: {self.hunger}/100")
        print(f"Настроение: {self.mood}/100")
        print(f"Энергия: {self.energy}/100")
        print(f"Здоровье: {self.health}/100")


pets = []

def create_pets():
    pets.append(Pet("Барсик", "кот", 2))
    pets.append(Pet("Рекс", "пёс", 3))
    pets.append(Pet("Пушистик", "кролик", 1))

def show_all_pets():
    if not pets:
        print("Нет питомцев!")
        return
    print("\n=== Все питомцы ===")
    for i, pet in enumerate(pets, 1):
        print(f"{i}. {pet.name} ({pet.pet_type}, {pet.age} лет)")

def select_pet():
    if not pets:
        print("Нет питомцев!")
        return None
    show_all_pets()
    try:
        choice = int(input("Выберите номер питомца: ")) - 1
        if 0 <= choice < len(pets):
            return pets[choice]
        print("Неверный выбор!")
    except ValueError:
        print("Введите число!")
    return None

def main_menu():
    create_pets()
    while True:
        print("\n=== Меню ===")
        print("1. Показать всех питомцев")
        print("2. Выбрать питомца")
        print("3. Покормить")
        print("4. Поиграть")
        print("5. Уложить спать")
        print("6. Вывести на прогулку")
        print("0. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            show_all_pets()
        elif choice == "2":
            pet = select_pet()
            if pet:
                pet.show_info()
        elif choice == "3":
            pet = select_pet()
            if pet:
                pet.feed()
        elif choice == "4":
            pet = select_pet()
            if pet:
                pet.play()
        elif choice == "5":
            pet = select_pet()
            if pet:
                pet.sleep()
        elif choice == "6":
            pet = select_pet()
            if pet:
                pet.walk()
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main_menu()
