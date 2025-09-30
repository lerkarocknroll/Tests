import unittest


def solve(models: list, available: list, manufacturers: list):
    repair_count = 0
    ssds = []
    for model, avail in zip(models, available):
        if avail == 1:
            if any(manuf in model for manuf in manufacturers):
                ssds.append(model)
                repair_count += 1
    return ssds, repair_count


class TestSSDSelection(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.models = ['480 ГБ 2.5" SATA накопитель Kingston A400',
                       '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                       '480 ГБ 2.5" SATA накопитель ADATA SU650',
                       '240 ГБ 2.5" SATA накопитель ADATA SU650',
                       '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                       '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
                       '480 ГБ 2.5" SATA накопитель WD Green',
                       '500 ГБ 2.5" SATA накопитель WD Red SA500']
        self.available = [1, 1, 1, 1, 0, 1, 1, 0]
        self.manufacturers = ['Intel', 'Samsung', 'WD']

    def test_original_case(self):
        """Тестирование оригинального случая"""
        result = solve(self.models, self.available, self.manufacturers)
        expected = (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                     '480 ГБ 2.5" SATA накопитель WD Green'], 2)
        self.assertEqual(result, expected)

    def test_empty_manufacturers(self):
        """Тестирование с пустым списком производителей"""
        result = solve(self.models, self.available, [])
        expected = ([], 0)
        self.assertEqual(result, expected)

    def test_empty_models(self):
        """Тестирование с пустым списком моделей"""
        result = solve([], [], self.manufacturers)
        expected = ([], 0)
        self.assertEqual(result, expected)

    def test_all_available(self):
        """Тестирование когда все диски доступны"""
        available_all = [1, 1, 1, 1, 1, 1, 1, 1]
        result = solve(self.models, available_all, self.manufacturers)
        expected = (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                     '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                     '480 ГБ 2.5" SATA накопитель WD Green',
                     '500 ГБ 2.5" SATA накопитель WD Red SA500'], 4)
        self.assertEqual(result, expected)

    def test_none_available(self):
        """Тестирование когда нет доступных дисков"""
        available_none = [0, 0, 0, 0, 0, 0, 0, 0]
        result = solve(self.models, available_none, self.manufacturers)
        expected = ([], 0)
        self.assertEqual(result, expected)

    def test_single_manufacturer(self):
        """Тестирование с одним производителем"""
        result = solve(self.models, self.available, ['Samsung'])
        expected = (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO'], 1)
        self.assertEqual(result, expected)

    def test_case_sensitivity(self):
        """Тестирование чувствительности к регистру"""
        models_case = ['500 ГБ 2.5" SATA накопитель samsung 870 EVO',
                       '480 ГБ 2.5" SATA накопитель wd Green']
        available_case = [1, 1]
        manufacturers_case = ['samsung', 'wd']
        result = solve(models_case, available_case, manufacturers_case)
        expected = ([], 0)  # Регистр не совпадает
        self.assertEqual(result, expected)

    def test_partial_manufacturer_name(self):
        """Тестирование частичного совпадения имени производителя"""
        models_partial = ['500 ГБ 2.5" SATA накопитель Sam 870 EVO',
                          '480 ГБ 2.5" SATA накопитель Western Digital Green']
        available_partial = [1, 1]
        manufacturers_partial = ['Sam', 'Western']
        result = solve(models_partial, available_partial, manufacturers_partial)
        expected = (['500 ГБ 2.5" SATA накопитель Sam 870 EVO',
                     '480 ГБ 2.5" SATA накопитель Western Digital Green'], 2)
        self.assertEqual(result, expected)

    def test_manufacturer_not_in_list(self):
        """Тестирование когда нужные производители отсутствуют"""
        manufacturers_other = ['Kingston', 'ADATA', 'Apacer']
        result = solve(self.models, self.available, manufacturers_other)
        expected = (['480 ГБ 2.5" SATA накопитель Kingston A400',
                     '480 ГБ 2.5" SATA накопитель ADATA SU650',
                     '240 ГБ 2.5" SATA накопитель ADATA SU650',
                     '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER'], 4)
        self.assertEqual(result, expected)

    def test_mixed_availability(self):
        """Тестирование смешанной доступности"""
        models_mixed = ['Samsung SSD', 'WD SSD', 'Intel SSD', 'Kingston SSD']
        available_mixed = [1, 0, 1, 1]
        manufacturers_mixed = ['Samsung', 'WD', 'Intel']
        result = solve(models_mixed, available_mixed, manufacturers_mixed)
        expected = (['Samsung SSD', 'Intel SSD'], 2)
        self.assertEqual(result, expected)

    def test_duplicate_manufacturers(self):
        """Тестирование с дублирующимися производителями"""
        manufacturers_dup = ['Samsung', 'WD', 'Samsung', 'Intel']
        result = solve(self.models, self.available, manufacturers_dup)
        expected = (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                     '480 ГБ 2.5" SATA накопитель WD Green'], 2)
        self.assertEqual(result, expected)

    def test_manufacturer_substring(self):
        """Тестирование когда имя производителя является подстрокой"""
        models_sub = ['Samsung Galaxy', 'MySamsung SSD', 'WD Passport', 'AWD Drive']
        available_sub = [1, 1, 1, 1]
        manufacturers_sub = ['Samsung', 'WD']
        result = solve(models_sub, available_sub, manufacturers_sub)
        expected = (['Samsung Galaxy', 'MySamsung SSD', 'WD Passport', 'AWD Drive'], 4)
        self.assertEqual(result, expected)

    def test_different_availability_length(self):
        """Тестирование когда списки разной длины"""
        models_short = ['Samsung SSD', 'WD SSD']
        available_long = [1, 1, 1, 1]  # zip обрежет до минимальной длины
        result = solve(models_short, available_long, self.manufacturers)
        expected = (['Samsung SSD', 'WD SSD'], 2)
        self.assertEqual(result, expected)


# Параметризованные тесты с использованием subTest
class TestSSDParameterized(unittest.TestCase):

    def test_various_scenarios(self):
        """Параметризованный тест различных сценариев"""
        test_cases = [
            # (models, available, manufacturers, expected)
            ([], [], [], ([], 0)),
            (['Samsung SSD'], [1], ['Samsung'], (['Samsung SSD'], 1)),
            (['Samsung SSD'], [0], ['Samsung'], ([], 0)),
            (['Kingston SSD'], [1], ['Samsung'], ([], 0)),
            (['Samsung SSD', 'WD SSD'], [1, 1], ['Samsung', 'WD'], (['Samsung SSD', 'WD SSD'], 2)),
            (['Samsung SSD', 'WD SSD'], [1, 0], ['Samsung', 'WD'], (['Samsung SSD'], 1)),
        ]

        for models, available, manufacturers, expected in test_cases:
            with self.subTest(models=models, available=available, manufacturers=manufacturers):
                result = solve(models, available, manufacturers)
                self.assertEqual(result, expected)


class TestSSDEdgeCases(unittest.TestCase):

    def test_special_characters_in_names(self):
        """Тестирование специальных символов в названиях"""
        models_special = ['Samsung+ SSD', 'WD@ SSD', 'Intel® SSD']
        available_special = [1, 1, 1]
        manufacturers_special = ['Samsung+', 'WD@', 'Intel®']
        result = solve(models_special, available_special, manufacturers_special)
        expected = (['Samsung+ SSD', 'WD@ SSD', 'Intel® SSD'], 3)
        self.assertEqual(result, expected)

    def test_numbers_in_manufacturer_names(self):
        """Тестирование цифр в названиях производителей"""
        models_num = ['NVMe SSD M2-2280', 'SATA3 SSD']
        available_num = [1, 1]
        manufacturers_num = ['M2', 'SATA3']
        result = solve(models_num, available_num, manufacturers_num)
        expected = (['NVMe SSD M2-2280', 'SATA3 SSD'], 2)
        self.assertEqual(result, expected)

    def test_whitespace_in_names(self):
        """Тестирование пробелов в названиях"""
        models_ws = ['  Samsung  SSD  ', 'WD  SSD']
        available_ws = [1, 1]
        manufacturers_ws = ['Samsung', 'WD']
        result = solve(models_ws, available_ws, manufacturers_ws)
        expected = (['  Samsung  SSD  ', 'WD  SSD'], 2)
        self.assertEqual(result, expected)

    def test_empty_string_manufacturer(self):
        """Тестирование с пустыми строками в производителях"""
        models_empty = [' SSD', 'Samsung SSD']
        available_empty = [1, 1]
        manufacturers_empty = ['', 'Samsung']
        result = solve(models_empty, available_empty, manufacturers_empty)
        # Пустая строка всегда будет найдена в любой строке
        expected = ([' SSD', 'Samsung SSD'], 2)
        self.assertEqual(result, expected)

    def test_none_values(self):
        """Тестирование с None значениями"""
        with self.assertRaises(TypeError):
            solve([None], [1], ['Samsung'])


if __name__ == '__main__':
    # Запуск тестов
    unittest.main(verbosity=2)

    # Оригинальный код для проверки
    print("\n" + "=" * 50)
    print("Оригинальная проверка:")

    models = ['480 ГБ 2.5" SATA накопитель Kingston A400', '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
              '480 ГБ 2.5" SATA накопитель ADATA SU650', '240 ГБ 2.5" SATA накопитель ADATA SU650',
              '250 ГБ 2.5" SATA накопитель Samsung 870 EVO', '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
              '480 ГБ 2.5" SATA накопитель WD Green', '500 ГБ 2.5" SATA накопитель WD Red SA500']
    available = [1, 1, 1, 1, 0, 1, 1, 0]
    manufacturers = ['Intel', 'Samsung', 'WD']

    result = solve(models, available, manufacturers)
    assert result == (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO', '480 ГБ 2.5" SATA накопитель WD Green'], 2), \
        f"Неверный результат: {result}"
    print(f"Сисадмин Василий сможет купить диски: {result[0]} и починить {result[1]} компьютера")