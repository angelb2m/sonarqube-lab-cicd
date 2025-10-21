def sumar(a, b):
    """Devuelve la suma de dos números"""
    return a + b


def dividir(a, b):
    """Devuelve la división de a entre b"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b


if __name__ == "__main__":
    print("Suma:", sumar(4, 5))
    print("División:", dividir(10, 2))

