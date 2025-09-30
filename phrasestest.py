import unittest


def solve(phrases: list):
    result = []  # список палиндромов
    for phrase in phrases:  # пройдите циклом по всем фразам
        clean_phrase = phrase.replace(" ", "")  # сохраните фразу без пробелов
        if clean_phrase == clean_phrase[::-1]:  # сравните фразу с ней же, развернутой наоборот (через [::-1])
            result.append(phrase)
    return result


class TestPalindrome(unittest.TestCase):

    def test_original_phrases(self):
        """Тестирование оригинального набора фраз"""
        phrases = ["нажал кабан на баклажан", "дом как комод", "рвал дед лавр", "азот калий и лактоза",
                   "а собака боса", "тонет енот", "карман мрак", "пуст суп"]
        result = solve(phrases)
        expected = ["нажал кабан на баклажан", "рвал дед лавр", "азот калий и лактоза",
                    "а собака боса", "тонет енот", "пуст суп"]
        self.assertEqual(result, expected)

    def test_single_word_palindromes(self):
        """Тестирование однословных палиндромов"""
        phrases = ["топот", "заказ", "комок", "ротор", "не палиндром"]
        result = solve(phrases)
        expected = ["топот", "заказ", "комок", "ротор"]
        self.assertEqual(result, expected)

    def test_multi_word_palindromes(self):
        """Тестирование многословных палиндромов"""
        phrases = ["а роза упала на лапу азора", "аргентина манит негра", "киборг побега робок"]
        result = solve(phrases)
        expected = ["а роза упала на лапу азора", "аргентина манит негра"]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        """Тестирование пустого списка"""
        result = solve([])
        self.assertEqual(result, [])

    def test_no_palindromes(self):
        """Тестирование когда нет палиндромов"""
        phrases = ["обычная фраза", "другая фраза", "просто текст"]
        result = solve(phrases)
        self.assertEqual(result, [])

    def test_all_palindromes(self):
        """Тестирование когда все фразы - палиндромы"""
        phrases = ["топот", "а роза упала на лапу азора", "ротор"]
        result = solve(phrases)
        self.assertEqual(result, phrases)

    def test_case_sensitivity(self):
        """Тестирование чувствительности к регистру"""
        phrases = ["Топот", "А роза упала на лапу азора", "РОТОР"]
        result = solve(phrases)
        # Функция не обрабатывает регистр, поэтому эти фразы не будут палиндромами
        self.assertEqual(result, [])

    def test_with_punctuation(self):
        """Тестирование с пунктуацией"""
        phrases = ["а роза упала на лапу азора!", "топот.", "мадам?"]
        result = solve(phrases)
        # Функция не удаляет пунктуацию, поэтому эти фразы не будут палиндромами
        self.assertEqual(result, [])

    def test_mixed_case_palindromes(self):
        """Тестирование палиндромов в разном регистре"""
        phrases = ["А роза упала на лапу азора", "Топот", "Шалаш"]
        # Приводим к нижнему регистру для корректного тестирования
        phrases_lower = [phrase.lower() for phrase in phrases]
        result = solve(phrases_lower)
        expected = ["а роза упала на лапу азора", "топот", "шалаш"]
        self.assertEqual(result, expected)

    def test_phrases_with_numbers(self):
        """Тестирование фраз с числами"""
        phrases = ["12321", "123 321", "не палиндром 123"]
        result = solve(phrases)
        expected = ["12321", "123 321"]
        self.assertEqual(result, expected)

    def test_special_characters(self):
        """Тестирование специальных символов"""
        phrases = ["a b a", "a ! a", "a b c b a"]
        result = solve(phrases)
        expected = ["a b a", "a b c b a"]
        self.assertEqual(result, expected)


# Параметризованные тесты с использованием subTest
class TestPalindromeParameterized(unittest.TestCase):

    def test_various_palindromes(self):
        """Параметризованный тест различных палиндромов"""
        test_cases = [
            (["топот"], ["топот"]),
            (["тест", "ротор"], ["ротор"]),
            (["а роза упала на лапу азора", "не палиндром"], ["а роза упала на лапу азора"]),
            ([], []),
            (["а", "б", "в"], ["а", "б", "в"]),  # Одиночные символы всегда палиндромы
        ]

        for input_phrases, expected in test_cases:
            with self.subTest(input=input_phrases, expected=expected):
                result = solve(input_phrases)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    # Запуск тестов
    unittest.main(verbosity=2)

    # Оригинальный код для проверки
    print("\n" + "=" * 50)
    print("Оригинальная проверка:")

    phrases = ["нажал кабан на баклажан", "дом как комод", "рвал дед лавр", "азот калий и лактоза",
               "а собака боса", "тонет енот", "карман мрак", "пуст суп"]
    result = solve(phrases)
    assert result == ["нажал кабан на баклажан", "рвал дед лавр", "азот калий и лактоза",
                      "а собака боса", "тонет енот", "пуст суп"], f"Неверный результат: {result}"
    print(f"Палиндромы: {result}")