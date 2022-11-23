from fastapi import FastAPI, Form
from typing import List, Optional
from pydantic import BaseModel

class Animal:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Animal({self.name})"


class Dog(Animal):
    def __init__(self, name: str, age: int):
        super(Dog, self).__init__(name)
        self.name = name
        self.age = age

    def bark(self):
        return self.name + " says woof!"


class Cat(Animal):
    def __init__(self, name: str, age: int):
        super(Cat, self).__init__(name)
        self.name = name
        self.age = age

    def meow(self):
        return self.name + " says meow!"


class Vet:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.animals = []

    def register_animal(self, animal):
        self.animals.append(animal)

    def remove_animal_by_name(self, name):
        self.animals = [animal for animal in self.animals if animal.name != name]

    def get_animals(self):
        return self.animals

    def get_dogs(self):
        return [animal for animal in self.animals if isinstance(animal, Dog)]

    def get_cats(self):
        return [animal for animal in self.animals if isinstance(animal, Cat)]



veterinarian = Vet("Dr. John", "New York, 405 E 72nd St, New York, NY 10021")

app = FastAPI()


@app.get("/")
def welcome():
    return f"Welcome to the {veterinarian.name} veterinary clinic in {veterinarian.city}!"


class RegisterAnimalInput(BaseModel):
    name: str
    animal_type: Optional[str] = "dog"


@app.post("/")
def register_animal(input: List[RegisterAnimalInput]):
    for animal in input:
        if animal.animal_type == "dog":
            veterinarian.register_animal(Dog(animal.name, 0))
        elif animal.animal_type == "cat":
            veterinarian.register_animal(Cat(animal.name, 0))
    return veterinarian.get_animals()


@app.get("/animals")
def get_animals():
    return veterinarian.get_animals() #



