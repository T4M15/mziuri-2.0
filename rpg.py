#1

class Character:
    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self._hp = hp
        self.level = level
        Character.count += 1

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)

    def take_damage(self, amount):
        self.hp -= amount

    @property
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        target.take_damage(5)

    @classmethod
    def from_string(cls, text):
        name, hp = text.split(";")
        return cls(name=name, hp=int(hp))

    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name and self.level == other.level
        return False

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"




if __name__ == "__main__":
    a = Character("Tariel")
    b = Character("Avtandil", hp=50)
    b.take_damage(70)

    print(a)
    print(b)
    print(b.is_alive)
    print(Character.count)



#2




class Warrior(Character):
    def __init__(self, name, hp=100, level=1, strength=10):
        super().__init__(name, hp, level)
        self.strength = strength

    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp, level)
        self.mana = mana

    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} MP {self.mana}"



t = Warrior("Tariel", hp=120, strength=15)
n = Mage("Nestan", hp=80, mana=15)

t.attack(n)
print(n)

n.attack(t)
n.attack(t)
print(t)




#3


class HealerMixin:
    def heal(self, target, amount):
        target.hp += amount


class Priest(HealerMixin, Mage):
    pass


p = Priest("Nestan", hp=60)
w = Warrior.from_string("Tariel;120")

p.heal(w, 30)
print(w)
print(type(w).__name__)
print(Character.is_valid_name("T"))
print(Character("A") == Character("A"))
print(Priest.__mro__)