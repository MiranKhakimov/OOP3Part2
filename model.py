import json
import os

class Model:
    A, B, C = 0, 1, 2
    min, max = 0, 100
    path = "value_data.json"

    def __init__(self):
        self.values = [10, 50, 90]
        self.observers = []
        self.load()

    def attach(self, callback):
        self.observers.append(callback)
        callback()

    def notify(self):
        for callback in self.observers:
            callback()

    def get_values(self):
        return list(self.values)

    def set_value(self, index, value):
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max

        old = list(self.values)
        self.values[index] = value

        if index == self.A:
            self.values[self.B] = max(self.values[self.A], self.values[self.B])
            self.values[self.C] = max(self.values[self.B], self.values[self.C])
        elif index == self.B:
            self.values[self.B] = max(self.values[self.B], self.values[self.A])
            self.values[self.B] = min(self.values[self.B], self.values[self.C])
        elif index == self.C:
            self.values[self.B] = min(self.values[self.B], self.values[self.C])
            self.values[self.A] = min(self.values[self.A], self.values[self.B])

        if self.values == old:
            return

        print("Значения модели изменены на: "+str(self.values))
        self.save()
        self.notify()

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {"a": self.values[self.A],
                 "b": self.values[self.B],
                 "c": self.values[self.C]},
                f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.values[self.A] = int(data.get("a", self.values[self.A]))
            self.values[self.B] = int(data.get("b", self.values[self.B]))
            self.values[self.C] = int(data.get("c", self.values[self.C]))
        except Exception:
            pass