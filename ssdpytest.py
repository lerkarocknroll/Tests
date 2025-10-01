import pytest
from typing import List, Tuple


def solve(models: list, available: list, manufacturers: list) -> Tuple[List[str], int]:
    """
    Select SSD drives for repair based on availability and manufacturer criteria.

    Args:
        models: List of SSD model names
        available: List of availability flags (1 - available, 0 - not available)
        manufacturers: List of manufacturer names to filter by

    Returns:
        Tuple of (selected_ssds, repair_count)
    """
    repair_count = 0
    ssds = []
    for model, avail in zip(models, available):
        if avail == 1:
            if any(manuf in model for manuf in manufacturers):
                ssds.append(model)
                repair_count += 1
    return ssds, repair_count


# Fixtures for test data
@pytest.fixture
def sample_models():
    """Fixture providing sample SSD models"""
    return [
        '480 ГБ 2.5" SATA накопитель Kingston A400',
        '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
        '480 ГБ 2.5" SATA накопитель ADATA SU650',
        '240 ГБ 2.5" SATA накопитель ADATA SU650',
        '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
        '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
        '480 ГБ 2.5" SATA накопитель WD Green',
        '500 ГБ 2.5" SATA накопитель WD Red SA500'
    ]


@pytest.fixture
def sample_available():
    """Fixture providing sample availability data"""
    return [1, 1, 1, 1, 0, 1, 1, 0]


@pytest.fixture
def sample_manufacturers():
    """Fixture providing sample manufacturers"""
    return ['Intel', 'Samsung', 'WD']


class TestSSDSelection:
    """Test class for SSD selection functionality"""

    # POSITIVE TESTS

    def test_original_case(self, sample_models, sample_available, sample_manufacturers):
        """Test original case with sample data"""
        result = solve(sample_models, sample_available, sample_manufacturers)
        expected = (
            [
                '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '480 ГБ 2.5" SATA накопитель WD Green'
            ],
            2
        )
        assert result == expected

    def test_empty_manufacturers(self, sample_models, sample_available):
        """Test with empty manufacturers list"""
        result = solve(sample_models, sample_available, [])
        expected = ([], 0)
        assert result == expected

    def test_empty_models(self, sample_manufacturers):
        """Test with empty models list"""
        result = solve([], [], sample_manufacturers)
        expected = ([], 0)
        assert result == expected

    def test_all_available(self, sample_models, sample_manufacturers):
        """Test when all disks are available"""
        available_all = [1, 1, 1, 1, 1, 1, 1, 1]
        result = solve(sample_models, available_all, sample_manufacturers)
        expected = (
            [
                '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '480 ГБ 2.5" SATA накопитель WD Green',
                '500 ГБ 2.5" SATA накопитель WD Red SA500'
            ],
            4
        )
        assert result == expected

    def test_none_available(self, sample_models, sample_manufacturers):
        """Test when no disks are available"""
        available_none = [0, 0, 0, 0, 0, 0, 0, 0]
        result = solve(sample_models, available_none, sample_manufacturers)
        expected = ([], 0)
        assert result == expected

    def test_single_manufacturer(self, sample_models, sample_available):
        """Test with single manufacturer"""
        result = solve(sample_models, sample_available, ['Samsung'])
        expected = (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO'], 1)
        assert result == expected

    # EDGE CASES

    def test_case_sensitivity(self):
        """Test case sensitivity in manufacturer names"""
        models_case = [
            '500 ГБ 2.5" SATA накопитель samsung 870 EVO',
            '480 ГБ 2.5" SATA накопитель wd Green'
        ]
        available_case = [1, 1]
        manufacturers_case = ['samsung', 'wd']
        result = solve(models_case, available_case, manufacturers_case)
        expected = ([], 0)  # Case doesn't match
        assert result == expected

    def test_partial_manufacturer_name(self):
        """Test partial manufacturer name matching"""
        models_partial = [
            '500 ГБ 2.5" SATA накопитель Sam 870 EVO',
            '480 ГБ 2.5" SATA накопитель Western Digital Green'
        ]
        available_partial = [1, 1]
        manufacturers_partial = ['Sam', 'Western']
        result = solve(models_partial, available_partial, manufacturers_partial)
        expected = (
            [
                '500 ГБ 2.5" SATA накопитель Sam 870 EVO',
                '480 ГБ 2.5" SATA накопитель Western Digital Green'
            ],
            2
        )
        assert result == expected

    def test_manufacturer_not_in_list(self, sample_models, sample_available):
        """Test with different manufacturers"""
        manufacturers_other = ['Kingston', 'ADATA', 'Apacer']
        result = solve(sample_models, sample_available, manufacturers_other)
        expected = (
            [
                '480 ГБ 2.5" SATA накопитель Kingston A400',
                '480 ГБ 2.5" SATA накопитель ADATA SU650',
                '240 ГБ 2.5" SATA накопитель ADATA SU650',
                '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER'
            ],
            4
        )
        assert result == expected

    def test_mixed_availability(self):
        """Test mixed availability scenarios"""
        models_mixed = ['Samsung SSD', 'WD SSD', 'Intel SSD', 'Kingston SSD']
        available_mixed = [1, 0, 1, 1]
        manufacturers_mixed = ['Samsung', 'WD', 'Intel']
        result = solve(models_mixed, available_mixed, manufacturers_mixed)
        expected = (['Samsung SSD', 'Intel SSD'], 2)
        assert result == expected

    def test_duplicate_manufacturers(self, sample_models, sample_available):
        """Test with duplicate manufacturers"""
        manufacturers_dup = ['Samsung', 'WD', 'Samsung', 'Intel']
        result = solve(sample_models, sample_available, manufacturers_dup)
        expected = (
            [
                '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '480 ГБ 2.5" SATA накопитель WD Green'
            ],
            2
        )
        assert result == expected

    def test_manufacturer_substring(self):
        """Test when manufacturer name is a substring"""
        models_sub = ['Samsung Galaxy', 'MySamsung SSD', 'WD Passport', 'AWD Drive']
        available_sub = [1, 1, 1, 1]
        manufacturers_sub = ['Samsung', 'WD']
        result = solve(models_sub, available_sub, manufacturers_sub)
        expected = (['Samsung Galaxy', 'MySamsung SSD', 'WD Passport', 'AWD Drive'], 4)
        assert result == expected

    def test_different_availability_length(self, sample_manufacturers):
        """Test when lists have different lengths"""
        models_short = ['Samsung SSD', 'WD SSD']
        available_long = [1, 1, 1, 1]  # zip will truncate to shortest length
        result = solve(models_short, available_long, sample_manufacturers)
        expected = (['Samsung SSD', 'WD SSD'], 2)
        assert result == expected

    def test_special_characters_in_names(self):
        """Test special characters in names"""
        models_special = ['Samsung+ SSD', 'WD@ SSD', 'Intel® SSD']
        available_special = [1, 1, 1]
        manufacturers_special = ['Samsung+', 'WD@', 'Intel®']
        result = solve(models_special, available_special, manufacturers_special)
        expected = (['Samsung+ SSD', 'WD@ SSD', 'Intel® SSD'], 3)
        assert result == expected

    def test_numbers_in_manufacturer_names(self):
        """Test numbers in manufacturer names"""
        models_num = ['NVMe SSD M2-2280', 'SATA3 SSD']
        available_num = [1, 1]
        manufacturers_num = ['M2', 'SATA3']
        result = solve(models_num, available_num, manufacturers_num)
        expected = (['NVMe SSD M2-2280', 'SATA3 SSD'], 2)
        assert result == expected

    def test_whitespace_in_names(self):
        """Test whitespace in names"""
        models_ws = ['  Samsung  SSD  ', 'WD  SSD']
        available_ws = [1, 1]
        manufacturers_ws = ['Samsung', 'WD']
        result = solve(models_ws, available_ws, manufacturers_ws)
        expected = (['  Samsung  SSD  ', 'WD  SSD'], 2)
        assert result == expected

    def test_empty_string_manufacturer(self):
        """Test empty string in manufacturers"""
        models_empty = [' SSD', 'Samsung SSD']
        available_empty = [1, 1]
        manufacturers_empty = ['', 'Samsung']
        # Empty string will be found in any string
        result = solve(models_empty, available_empty, manufacturers_empty)
        expected = ([' SSD', 'Samsung SSD'], 2)
        assert result == expected

    def test_none_values(self):
        """Test None values raise TypeError"""
        with pytest.raises(TypeError):
            solve([None], [1], ['Samsung'])


# PARAMETRIZED TESTS
class TestParametrizedSSDSelection:
    """Parametrized tests for various scenarios"""

    @pytest.mark.parametrize("models, available, manufacturers, expected", [
        # Empty cases
        ([], [], [], ([], 0)),
        (['Samsung SSD'], [], ['Samsung'], ([], 0)),

        # Single item cases
        (['Samsung SSD'], [1], ['Samsung'], (['Samsung SSD'], 1)),
        (['Samsung SSD'], [0], ['Samsung'], ([], 0)),
        (['Kingston SSD'], [1], ['Samsung'], ([], 0)),

        # Multiple items
        (
                ['Samsung SSD', 'WD SSD'],
                [1, 1],
                ['Samsung', 'WD'],
                (['Samsung SSD', 'WD SSD'], 2)
        ),
        (
                ['Samsung SSD', 'WD SSD'],
                [1, 0],
                ['Samsung', 'WD'],
                (['Samsung SSD'], 1)
        ),
        (
                ['Intel SSD', 'Samsung SSD', 'WD SSD'],
                [1, 0, 1],
                ['Samsung', 'WD'],
                (['WD SSD'], 1)
        ),
    ])
    def test_various_scenarios(self, models, available, manufacturers, expected):
        """Test various scenarios with parametrization"""
        result = solve(models, available, manufacturers)
        assert result == expected

    @pytest.mark.parametrize("models, available, manufacturers", [
        (['Test SSD'], [2], ['Test']),  # Invalid availability
        (['Test SSD'], [-1], ['Test']),  # Negative availability
        (['Test SSD'], [1.5], ['Test']),  # Float availability
    ])
    def test_invalid_availability_values(self, models, available, manufacturers):
        """Test behavior with invalid availability values"""
        # Function should work but might not select drives correctly
        result = solve(models, available, manufacturers)
        # Just check it doesn't crash and returns proper structure
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)


# FIXTURE-BASED PARAMETRIZED TESTS
@pytest.fixture(params=[
    # (models, available, manufacturers, expected_description, expected_result)
    (
            ['Samsung SSD 1', 'Samsung SSD 2'],
            [1, 1],
            ['Samsung'],
            "multiple matching models",
            (['Samsung SSD 1', 'Samsung SSD 2'], 2)
    ),
    (
            ['Samsung SSD', 'Kingston SSD'],
            [1, 1],
            ['Samsung'],
            "mixed manufacturers",
            (['Samsung SSD'], 1)
    ),
    (
            ['WD SSD', 'Seagate SSD'],
            [0, 1],
            ['WD', 'Seagate'],
            "mixed availability",
            (['Seagate SSD'], 1)
    ),
])
def complex_scenario(request):
    """Fixture for complex test scenarios"""
    return request.param


def test_complex_scenarios(complex_scenario):
    """Test complex scenarios using fixture parametrization"""
    models, available, manufacturers, description, expected = complex_scenario
    result = solve(models, available, manufacturers)
    assert result == expected, f"Failed for scenario: {description}"


# TEST WITH MARKS
@pytest.mark.slow
def test_large_dataset():
    """Test with large dataset (marked as slow)"""
    models = [f"SSD {i}" for i in range(1000)]
    available = [1 if i % 2 == 0 else 0 for i in range(1000)]
    manufacturers = ['SSD']

    result = solve(models, available, manufacturers)
    # Should select about half of the models
    assert len(result[0]) == 500
    assert result[1] == 500


@pytest.mark.xfail(reason="Empty string matching might be unexpected behavior")
def test_empty_string_matching():
    """Test that empty string matching might be considered a bug"""
    models = ['Some SSD', 'Another SSD']
    available = [1, 1]
    manufacturers = ['']
    result = solve(models, available, manufacturers)
    # This might not be the desired behavior
    assert result == (['Some SSD', 'Another SSD'], 2)


def test_original_validation():
    """Original validation from the main block"""
    models = [
        '480 ГБ 2.5" SATA накопитель Kingston A400',
        '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
        '480 ГБ 2.5" SATA накопитель ADATA SU650',
        '240 ГБ 2.5" SATA накопитель ADATA SU650',
        '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
        '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
        '480 ГБ 2.5" SATA накопитель WD Green',
        '500 ГБ 2.5" SATA накопитель WD Red SA500'
    ]
    available = [1, 1, 1, 1, 0, 1, 1, 0]
    manufacturers = ['Intel', 'Samsung', 'WD']

    result = solve(models, available, manufacturers)
    expected = (
        [
            '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
            '480 ГБ 2.5" SATA накопитель WD Green'
        ],
        2
    )
    assert result == expected, f"Неверный результат: {result}"

    # Print for verification (optional)
    print(f"Сисадмин Василий сможет купить диски: {result[0]} и починить {result[1]} компьютера")


if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])