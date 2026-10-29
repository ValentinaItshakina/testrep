import re

def validate_age(age: int) -> bool:
    """
    AC-013 / TR-VAL-01: Проверка возраста пользователя.
    Допустимый диапазон: 18 <= age <= 99 (от 18 до 98 включительно).
    """
    return 18 <= age <= 99


def validate_password(password: str) -> bool:
    """
    AC-014 / TR-VAL-02: Проверка сложности пароля.
    Требования: минимум 8 символов и хотя бы одна цифра.
    """
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    return True


def validate_discount(discount_percent: float) -> bool:
    """
    TR-VAL-03: Проверка размера скидки.
    Максимально допустимый размер: 30%.
    """
    return discount_percent <= 30.0