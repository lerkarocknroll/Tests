import pytest


def solve(cook_book: list, person: int):
    result = []
    for dish in cook_book:
        dish_name = dish[0]
        ingredients = dish[1]
        ingredient_strings = []
        for ingredient in ingredients:
            name = ingredient[0]
            quantity = ingredient[1] * person
            unit = ingredient[2]
            ingredient_str = f"{name} {quantity} {unit}"
            ingredient_strings.append(ingredient_str)
        joined_ingredients = ', '.join(ingredient_strings)
        dish_line = f"{dish_name}: {joined_ingredients}"
        result.append(dish_line)
    return result


class TestCookBook:
    @pytest.fixture
    def sample_cook_book(self):
        return [
            ['Салат',
             [
                 ['картофель', 100, 'гр.'],
                 ['морковь', 50, 'гр.'],
                 ['огурцы', 50, 'гр.'],
                 ['горошек', 30, 'гр.'],
                 ['майонез', 70, 'мл.'],
             ]
             ],
            ['Пицца',
             [
                 ['сыр', 50, 'гр.'],
                 ['томаты', 50, 'гр.'],
                 ['тесто', 100, 'гр.'],
                 ['бекон', 30, 'гр.'],
                 ['колбаса', 30, 'гр.'],
                 ['грибы', 20, 'гр.'],
             ],
             ],
            ['Фруктовый десерт',
             [
                 ['хурма', 60, 'гр.'],
                 ['киви', 60, 'гр.'],
                 ['творог', 60, 'гр.'],
                 ['сахар', 10, 'гр.'],
                 ['мед', 50, 'мл.'],
             ]
             ]
        ]

    @pytest.mark.parametrize("persons,expected", [
        (1, [
            'Салат: картофель 100 гр., морковь 50 гр., огурцы 50 гр., горошек 30 гр., майонез 70 мл.',
            'Пицца: сыр 50 гр., томаты 50 гр., тесто 100 гр., бекон 30 гр., колбаса 30 гр., грибы 20 гр.',
            'Фруктовый десерт: хурма 60 гр., киви 60 гр., творог 60 гр., сахар 10 гр., мед 50 мл.'
        ]),
        (5, [
            'Салат: картофель 500 гр., морковь 250 гр., огурцы 250 гр., горошек 150 гр., майонез 350 мл.',
            'Пицца: сыр 250 гр., томаты 250 гр., тесто 500 гр., бекон 150 гр., колбаса 150 гр., грибы 100 гр.',
            'Фруктовый десерт: хурма 300 гр., киви 300 гр., творог 300 гр., сахар 50 гр., мед 250 мл.'
        ]),
        (0, [
            'Салат: картофель 0 гр., морковь 0 гр., огурцы 0 гр., горошек 0 гр., майонез 0 мл.',
            'Пицца: сыр 0 гр., томаты 0 гр., тесто 0 гр., бекон 0 гр., колбаса 0 гр., грибы 0 гр.',
            'Фруктовый десерт: хурма 0 гр., киви 0 гр., творог 0 гр., сахар 0 гр., мед 0 мл.'
        ]),
        (10, [
            'Салат: картофель 1000 гр., морковь 500 гр., огурцы 500 гр., горошек 300 гр., майонез 700 мл.',
            'Пицца: сыр 500 гр., томаты 500 гр., тесто 1000 гр., бекон 300 гр., колбаса 300 гр., грибы 200 гр.',
            'Фруктовый десерт: хурма 600 гр., киви 600 гр., творог 600 гр., сахар 100 гр., мед 500 мл.'
        ]),
    ])
    def test_solve_with_different_persons(self, sample_cook_book, persons, expected):
        """Тестирование функции с разным количеством персон"""
        result = solve(sample_cook_book, persons)
        assert result == expected

    def test_solve_empty_cook_book(self):
        """Тестирование с пустой кулинарной книгой"""
        result = solve([], 5)
        assert result == []

    def test_solve_single_dish(self, sample_cook_book):
        """Тестирование с одним блюдом"""
        single_dish_book = [sample_cook_book[0]]  # Только салат
        result = solve(single_dish_book, 2)
        expected = [
            'Салат: картофель 200 гр., морковь 100 гр., огурцы 100 гр., горошек 60 гр., майонез 140 мл.'
        ]
        assert result == expected

    def test_solve_ingredient_format(self, sample_cook_book):
        """Тестирование формата вывода ингредиентов"""
        result = solve(sample_cook_book, 1)

        # Проверяем, что каждый ингредиент имеет правильный формат
        for dish in result:
            assert ': ' in dish  # Проверяем разделитель между названием блюда и ингредиентами
            dish_name, ingredients_str = dish.split(': ')
            ingredients = ingredients_str.split(', ')

            for ingredient in ingredients:
                parts = ingredient.split(' ')
                assert len(parts) >= 3  # Должны быть название, количество и единица измерения
                assert parts[-1] in ['гр.', 'мл.']  # Проверяем единицы измерения

    @pytest.mark.parametrize("persons", [-1, -5, -10])
    def test_solve_negative_persons(self, sample_cook_book, persons):
        """Тестирование с отрицательным количеством персон"""
        result = solve(sample_cook_book, persons)
        # Проверяем, что количества ингредиентов отрицательные (это может быть ожидаемым поведением)
        for dish in result:
            ingredients_str = dish.split(': ')[1]
            ingredients = ingredients_str.split(', ')
            for ingredient in ingredients:
                quantity = int(ingredient.split(' ')[-2])
                assert quantity < 0  # Количества должны быть отрицательными


if __name__ == '__main__':
    # Оригинальный код для проверки
    cook_book = [
        ['Салат',
         [
             ['картофель', 100, 'гр.'],
             ['морковь', 50, 'гр.'],
             ['огурцы', 50, 'гр.'],
             ['горошек', 30, 'гр.'],
             ['майонез', 70, 'мл.'],
         ]
         ],
        ['Пицца',
         [
             ['сыр', 50, 'гр.'],
             ['томаты', 50, 'гр.'],
             ['тесто', 100, 'гр.'],
             ['бекон', 30, 'гр.'],
             ['колбаса', 30, 'гр.'],
             ['грибы', 20, 'гр.'],
         ],
         ],
        ['Фруктовый десерт',
         [
             ['хурма', 60, 'гр.'],
             ['киви', 60, 'гр.'],
             ['творог', 60, 'гр.'],
             ['сахар', 10, 'гр.'],
             ['мед', 50, 'мл.'],
         ]
         ]
    ]

    result = solve(cook_book, 5)
    expected = [
        'Салат: картофель 500 гр., морковь 250 гр., огурцы 250 гр., горошек 150 гр., майонез 350 мл.',
        'Пицца: сыр 250 гр., томаты 250 гр., тесто 500 гр., бекон 150 гр., колбаса 150 гр., грибы 100 гр.',
        'Фруктовый десерт: хурма 300 гр., киви 300 гр., творог 300 гр., сахар 50 гр., мед 250 мл.'
    ]
    assert result == expected, f"Неверный результат: {result}"
    print(f"Список покупок на 5 персон: {result}")