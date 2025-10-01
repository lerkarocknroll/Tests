import pytest


def solve(phrases: list):
    result = []  # список палиндромов
    for phrase in phrases:  # пройдите циклом по всем фразам
        clean_phrase = phrase.replace(" ", "")  # сохраните фразу без пробелов
        if clean_phrase == clean_phrase[::-1]:  # сравните фразу с ней же, развернутой наоборот (через [::-1])
            result.append(phrase)
    return result


# Fixtures
@pytest.fixture
def original_phrases():
    """Фикстура с оригинальным набором фраз"""
    return [
        "нажал кабан на баклажан", "дом как комод", "рвал дед лавр",
        "азот калий и лактоза", "а собака боса", "тонет енот",
        "карман мрак", "пуст суп"
    ]


@pytest.fixture
def expected_original_result():
    """Ожидаемый результат для оригинального набора"""
    return [
        "нажал кабан на баклажан", "рвал дед лавр", "азот калий и лактоза",
        "а собака боса", "тонет енот", "пуст суp"
    ]


# Basic Tests
class TestPalindromeBasic:
    """Базовые тесты для функции поиска палиндромов"""

    def test_original_phrases(self, original_phrases):
        """Тестирование оригинального набора фраз"""
        result = solve(original_phrases)
        expected = [
            "нажал кабан на баклажан", "рвал дед лавр", "азот калий и лактоза",
            "а собака боса", "тонет енот", "пуст суp"
        ]
        assert result == expected

    def test_single_word_palindromes(self):
        """Тестирование однословных палиндромов"""
        phrases = ["топот", "заказ", "комок", "ротор", "не палиндром"]
        result = solve(phrases)
        expected = ["топот", "заказ", "комок", "ротор"]
        assert result == expected

    def test_multi_word_palindromes(self):
        """Тестирование многословных палиндромов"""
        phrases = ["а роза упала на лапу азора", "аргентина манит негра", "киборг побега робок"]
        result = solve(phrases)
        expected = ["а роза упала на лапу азора", "аргентина манит негра"]
        assert result == expected

    def test_empty_list(self):
        """Тестирование пустого списка"""
        result = solve([])
        assert result == []

    def test_no_palindromes(self):
        """Тестирование когда нет палиндромов"""
        phrases = ["обычная фраза", "другая фраза", "просто текст"]
        result = solve(phrases)
        assert result == []

    def test_all_palindromes(self):
        """Тестирование когда все фразы - палиндромы"""
        phrases = ["топот", "а роза упала на лапу азора", "ротор"]
        result = solve(phrases)
        assert result == phrases


# Edge Cases Tests
class TestPalindromeEdgeCases:
    """Тесты граничных случаев"""

    def test_case_sensitivity(self):
        """Тестирование чувствительности к регистру"""
        phrases = ["Топот", "А роза упала на лапу азора", "РОТОР"]
        result = solve(phrases)
        # Функция не обрабатывает регистр, поэтому эти фразы не будут палиндромами
        assert result == []

    def test_with_punctuation(self):
        """Тестирование с пунктуацией"""
        phrases = ["а роза упала на лапу азора!", "топот.", "мадам?"]
        result = solve(phrases)
        # Функция не удаляет пунктуацию, поэтому эти фразы не будут палиндромами
        assert result == []

    def test_mixed_case_palindromes(self):
        """Тестирование палиндромов в разном регистре"""
        phrases = ["А роза упала на лапу азора", "Топот", "Шалаш"]
        # Приводим к нижнему регистру для корректного тестирования
        phrases_lower = [phrase.lower() for phrase in phrases]
        result = solve(phrases_lower)
        expected = ["а роза упала на лапу азора", "топот", "шалаш"]
        assert result == expected

    def test_phrases_with_numbers(self):
        """Тестирование фраз с числами"""
        phrases = ["12321", "123 321", "не палиндром 123"]
        result = solve(phrases)
        expected = ["12321", "123 321"]
        assert result == expected

    def test_special_characters(self):
        """Тестирование специальных символов"""
        phrases = ["a b a", "a ! a", "a b c b a"]
        result = solve(phrases)
        expected = ["a b a", "a b c b a"]
        assert result == expected

    def test_single_character_phrases(self):
        """Тестирование одиночных символов"""
        phrases = ["а", "б", "в", "г"]
        result = solve(phrases)
        # Одиночные символы всегда палиндромы
        assert result == phrases


# Parametrized Tests
class TestPalindromeParametrized:
    """Параметризованные тесты различных сценариев"""

    @pytest.mark.parametrize("phrases,expected", [
        # Одиночные палиндромы
        (["топот"], ["топот"]),
        (["ротор"], ["ротор"]),
        (["а роза упала на лапу азора"], ["а роза упала на лапу азора"]),

        # Смешанные случаи
        (["тест", "ротор"], ["ротор"]),
        (["а роза упала на лапу азора", "не палиндром"], ["а роза упала на лапу азора"]),
        (["топот", "заказ", "не палиндром"], ["топот", "заказ"]),

        # Граничные случаи
        ([], []),
        (["а", "б", "в"], ["а", "б", "в"]),  # Одиночные символы всегда палиндромы
        ([" "], [" "]),  # Пробел
        (["  "], ["  "]),  # Несколько пробелов
    ])
    def test_various_palindromes(self, phrases, expected):
        """Параметризованный тест различных палиндромов"""
        result = solve(phrases)
        assert result == expected

    @pytest.mark.parametrize("non_palindromes", [
        ["обычная фраза"],
        ["не палиндром", "тоже не палиндром"],
        ["test", "phrase"],
        ["123456", "abcdef"],
    ])
    def test_non_palindromes(self, non_palindromes):
        """Тестирование не-палиндромов"""
        result = solve(non_palindromes)
        assert result == []

    @pytest.mark.parametrize("palindrome", [
        "топот",
        "ротор",
        "а роза упала на лапу азора",
        "аргентина манит негра",
        "12321",
        "123 321",
        "a b a",
    ])
    def test_single_palindromes(self, palindrome):
        """Тестирование отдельных палиндромов"""
        result = solve([palindrome])
        assert result == [palindrome]


# Advanced Parametrized Tests
class TestPalindromeAdvanced:
    """Продвинутые параметризованные тесты"""

    @pytest.mark.parametrize("input_phrases,expected_output,test_id", [
        (["топот", "дом", "ротор"], ["топот", "ротор"], "mixed_case"),
        (["а", "б", "в д"], ["а", "б", "в д"], "single_chars_with_space"),
        (["a", "b", "c"], ["a", "b", "c"], "english_chars"),
        (["1", "2", "3"], ["1", "2", "3"], "digits"),
        (["", " "], ["", " "], "empty_strings"),
    ], ids=lambda x: x if isinstance(x, str) else "")
    def test_complex_scenarios(self, input_phrases, expected_output, test_id):
        """Комплексные сценарии с идентификаторами тестов"""
        result = solve(input_phrases)
        assert result == expected_output

    @pytest.mark.parametrize("phrase,expected", [
        ("топот", True),
        ("ротор", True),
        ("а роза упала на лапу азора", True),
        ("не палиндром", False),
        ("обычная фраза", False),
        ("12321", True),
        ("123 321", True),
        ("123456", False),
    ])
    def test_individual_phrase_detection(self, phrase, expected):
        """Тестирование определения палиндромов для отдельных фраз"""
        result = solve([phrase])
        if expected:
            assert result == [phrase]
        else:
            assert result == []


# Fixture-based Tests
class TestPalindromeWithFixtures:
    """Тесты с использованием фикстур"""

    @pytest.fixture
    def common_palindromes(self):
        """Фикстура с общими палиндромами"""
        return ["топот", "ротор", "а роза упала на лапу азора", "12321"]

    @pytest.fixture
    def common_non_palindromes(self):
        """Фикстура с общими не-палиндромами"""
        return ["не палиндром", "обычная фраза", "test phrase", "123456"]

    def test_mixed_with_fixtures(self, common_palindromes, common_non_palindromes):
        """Тест смешанного набора с использованием фикстур"""
        mixed_phrases = common_palindromes + common_non_palindromes
        result = solve(mixed_phrases)
        assert result == common_palindromes

    def test_only_palindromes_fixture(self, common_palindromes):
        """Тест только палиндромов из фикстуры"""
        result = solve(common_palindromes)
        assert result == common_palindromes

    def test_only_non_palindromes_fixture(self, common_non_palindromes):
        """Тест только не-палиндромов из фикстуры"""
        result = solve(common_non_palindromes)
        assert result == []


# Tests with Marks
class TestPalindromeMarked:
    """Тесты с использованием маркеров"""

    @pytest.mark.slow
    def test_large_input(self):
        """Тест с большим количеством данных (помечен как медленный)"""
        phrases = [f"phrase_{i}" for i in range(1000)]
        # Добавим несколько палиндромов
        phrases[100] = "топот"
        phrases[500] = "ротор"
        phrases[900] = "а роза упала на лапу азора"

        result = solve(phrases)
        expected = ["топот", "ротор", "а роза упала на лапу азора"]
        assert result == expected

    @pytest.mark.xfail(reason="Функция не обрабатывает регистр")
    def test_case_insensitive_expected_fail(self):
        """Ожидаемо падающий тест - функция не поддерживает регистронезависимость"""
        phrases = ["Топот", "Ротор"]
        result = solve(phrases)
        # Этот тест должен упасть, так как функция чувствительна к регистру
        assert result == ["Топот", "Ротор"]

    @pytest.mark.skip(reason="Функция не удаляет пунктуацию")
    def test_punctuation_handling(self):
        """Пропущенный тест - функция не обрабатывает пунктуацию"""
        phrases = ["а роза упала на лапу азора!", "топот."]
        result = solve(phrases)
        assert result == ["а роза упала на лапу азора!", "топот."]


# Final validation test
def test_original_validation():
    """Оригинальная проверка из основного блока"""
    phrases = [
        "нажал кабан на баклажан", "дом как комод", "рвал дед лавр",
        "азот калий и лактоза", "а собака боса", "тонет енот",
        "карман мрак", "пуст суp"
    ]
    result = solve(phrases)
    expected = [
        "нажал кабан на баклажан", "рвал дед лавр", "азот калий и лактоза",
        "а собака боса", "тонет енот", "пуст суp"
    ]
    assert result == expected, f"Неверный результат: {result}"
    print(f"Палиндромы: {result}")


# Custom pytest configuration
def pytest_configure(config):
    """Регистрация кастомных маркеров"""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    # Запуск pytest программно
    pytest.main([__file__, "-v", "--tb=short"])

    # Дополнительная проверка
    print("\n" + "=" * 50)
    print("Дополнительная проверка:")
    test_original_validation()