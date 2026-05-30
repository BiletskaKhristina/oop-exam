import math
from abc import ABC, abstractmethod
from google.adk.agents import Agent


# =========================
# OOP: АБСТРАКЦІЯ
# =========================
class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


# =========================
# НАСЛІДУВАННЯ + ПОЛІМОРФІЗМ
# =========================
class Rectangle(Shape):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Triangle(Shape):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))


# =========================
# ІНКАПСУЛЯЦІЯ
# =========================
class ShapeStorage:

    def __init__(self):
        self.__shapes = []

    def add(self, shape):
        self.__shapes.append(shape)

    def total_area(self):
        return sum(s.area() for s in self.__shapes)


# =========================
# TOOL (СТІЙКИЙ ДО ПОМИЛОК)
# =========================
def calculate_shape_area(shape: str, params: dict):

    try:
        if shape == "rectangle":
            obj = Rectangle(
                float(params.get("width", 0)),
                float(params.get("height", 0))
            )

        elif shape == "circle":
            obj = Circle(
                float(params.get("radius", 0))
            )

        elif shape == "triangle":
            a = params.get("a") or params.get("side1")
            b = params.get("b") or params.get("side2")
            c = params.get("c") or params.get("side3")

            if a is None or b is None or c is None:
                return {
                    "error": "Triangle requires 3 sides: a, b, c"
                }

            obj = Triangle(float(a), float(b), float(c))

        else:
            return {"error": "Unknown shape"}

        return {
            "shape": shape,
            "area": obj.area(),
            "perimeter": obj.perimeter()
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# ROOT AGENT
# =========================
root_agent = Agent(
    name="geometry_agent",
    description="Математичний асистент з геометрії",
    instruction="Допомагає обчислювати площі та периметри фігур українською мовою",
    tools=[calculate_shape_area]
)