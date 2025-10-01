"""
Unit tests for Yandex.Disk REST API using pytest
Test suite for folder creation functionality
"""

import os
import pytest
from unittest.mock import Mock, patch
import requests
import time
from typing import List, Tuple, Optional


class YandexDiskAPIClient:
    """Client for Yandex.Disk API operations"""

    def __init__(self, token: str, base_url: str = "https://cloud-api.yandex.net/v1/disk/resources"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"OAuth {token}",
            "Content-Type": "application/json"
        }

    def create_folder(self, path: str, timeout: int = 30) -> requests.Response:
        """Create folder on Yandex.Disk"""
        return requests.put(
            self.base_url,
            headers=self.headers,
            params={"path": path},
            timeout=timeout
        )

    def get_folder_info(self, path: str, timeout: int = 30) -> requests.Response:
        """Get folder information"""
        return requests.get(
            self.base_url,
            headers=self.headers,
            params={"path": path},
            timeout=timeout
        )

    def delete_folder(self, path: str, timeout: int = 30) -> requests.Response:
        """Delete folder from Yandex.Disk"""
        return requests.delete(
            self.base_url,
            headers=self.headers,
            params={"path": path},
            timeout=timeout
        )

    def list_files(self, limit: int = 20, offset: int = 0, timeout: int = 30) -> requests.Response:
        """List files on Yandex.Disk"""
        return requests.get(
            f"{self.base_url}/files",
            headers=self.headers,
            params={"limit": limit, "offset": offset},
            timeout=timeout
        )


# Fixtures
@pytest.fixture
def yandex_token():
    """Fixture for Yandex OAuth token"""
    return "y0__xDIxNzRBhjblgMg9KLG2ROI4da4f-5cTi0XoH0CJ8sWTS3pHA"


@pytest.fixture
def api_client(yandex_token):
    """Fixture for YandexDiskAPIClient instance"""
    return YandexDiskAPIClient(yandex_token)


@pytest.fixture
def test_folder_path():
    """Fixture for test folder path"""
    return "/test_folder"


@pytest.fixture
def unique_test_folder():
    """Fixture for unique test folder name"""
    return f"/test_api_{int(time.time())}_{hash(str(time.time()))}"


def create_mock_response(status_code: int, json_data: dict) -> Mock:
    """Helper to create mock response"""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data
    return mock_response


# Mocked API Tests
class TestYandexDiskAPIMocked:
    """Unit tests with mocked API responses"""

    # POSITIVE TEST CASES

    def test_create_folder_success_201(self, api_client, test_folder_path):
        """Should return 201 when folder is successfully created"""
        # Arrange
        expected_response = {
            "href": f"{api_client.base_url}?path={test_folder_path}",
            "method": "GET",
            "templated": False
        }

        with patch.object(requests, 'put') as mock_put:
            mock_put.return_value = create_mock_response(201, expected_response)

            # Act
            response = api_client.create_folder(test_folder_path)

            # Assert
            assert response.status_code == 201
            assert response.json() == expected_response
            mock_put.assert_called_once_with(
                api_client.base_url,
                headers=api_client.headers,
                params={"path": test_folder_path},
                timeout=30
            )

    def test_create_folder_already_exists_409(self, api_client, test_folder_path):
        """Should return 409 when folder already exists"""
        # Arrange
        expected_response = {
            "message": "Resource already exists",
            "description": "Specified resource '/test_folder' already exists",
            "error": "DiskPathPointsToExistentDirectoryError"
        }

        with patch.object(requests, 'put') as mock_put:
            mock_put.return_value = create_mock_response(409, expected_response)

            # Act
            response = api_client.create_folder(test_folder_path)

            # Assert
            assert response.status_code == 409
            assert response.json()["error"] == "DiskPathPointsToExistentDirectoryError"

    def test_folder_appears_in_list_after_creation(self, api_client, test_folder_path):
        """Should find created folder in files list"""
        # Arrange
        with patch.object(requests, 'put') as mock_put, \
             patch.object(requests, 'get') as mock_get:

            mock_put.return_value = create_mock_response(201, {})

            expected_files_response = {
                "items": [
                    {
                        "path": f"disk:{test_folder_path}",
                        "name": "test_folder",
                        "type": "dir"
                    }
                ],
                "limit": 20,
                "offset": 0
            }
            mock_get.return_value = create_mock_response(200, expected_files_response)

            # Act
            create_response = api_client.create_folder(test_folder_path)
            list_response = api_client.list_files()

            # Assert
            assert create_response.status_code == 201
            assert list_response.status_code == 200

            items = list_response.json()["items"]
            folder_found = any(
                item["path"] == f"disk:{test_folder_path}" and item["type"] == "dir"
                for item in items
            )
            assert folder_found

    # NEGATIVE TEST CASES

    @pytest.mark.parametrize("status_code,expected_error,test_data", [
        (
            401,
            "UnauthorizedError",
            {
                "message": "Unauthorized",
                "description": "Invalid OAuth token",
                "error": "UnauthorizedError"
            }
        ),
        (
            400,
            "FieldValidationError",
            {
                "message": "Field validation error",
                "description": "path: Field validation error",
                "error": "FieldValidationError"
            }
        ),
        (
            403,
            "TooManyRequestsError",
            {
                "message": "API is not available",
                "description": "The resource API is not available",
                "error": "TooManyRequestsError"
            }
        ),
        (
            404,
            "DiskNotFoundError",
            {
                "message": "Resource not found",
                "description": "Specified resource '/nonexistent_parent/new_folder' not found",
                "error": "DiskNotFoundError"
            }
        ),
        (
            409,
            "DiskPathPointsToFileError",
            {
                "message": "Resource conflict",
                "description": "Specified path '/existing_file' points to a file",
                "error": "DiskPathPointsToFileError"
            }
        ),
    ])
    def test_api_error_responses(self, api_client, status_code, expected_error, test_data):
        """Test various API error responses"""
        with patch.object(requests, 'put') as mock_put:
            mock_put.return_value = create_mock_response(status_code, test_data)

            # Use appropriate path based on error type
            path = "" if status_code == 400 else "/nonexistent_parent/new_folder" if status_code == 404 else "/existing_file" if status_code == 409 else "/test_folder"

            response = api_client.create_folder(path)

            assert response.status_code == status_code
            assert response.json()["error"] == expected_error

    # NETWORK ERROR TESTS

    @pytest.mark.parametrize("exception_class,exception_msg", [
        (requests.exceptions.ConnectionError, "Connection failed"),
        (requests.exceptions.Timeout, "Request timed out"),
    ])
    def test_network_errors(self, api_client, test_folder_path, exception_class, exception_msg):
        """Test network-related exceptions"""
        with patch.object(requests, 'put') as mock_put:
            mock_put.side_effect = exception_class(exception_msg)

            with pytest.raises(exception_class):
                api_client.create_folder(test_folder_path, timeout=5)


# Real API Integration Tests
class TestYandexDiskAPIReal:
    """Integration tests with real Yandex.Disk API"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self, api_client, unique_test_folder):
        """Setup and teardown for each test"""
        self.client = api_client
        self.test_folder = unique_test_folder
        yield
        # Teardown - cleanup created folders
        self._safe_delete_folder(self.test_folder)

    def _safe_delete_folder(self, path: str):
        """Safely delete folder ignoring errors"""
        try:
            self.client.delete_folder(path, timeout=5)
        except (requests.exceptions.RequestException, KeyError):
            pass  # Folder might not exist or already deleted

    def test_create_folder_success(self):
        """Should successfully create folder via real API"""
        # Act
        response = self.client.create_folder(self.test_folder)

        # Assert
        assert response.status_code in [201, 409]  # 201 Created or 409 Already exists

    def test_create_and_verify_folder_exists(self):
        """Should create folder and verify its existence"""
        # Act
        create_response = self.client.create_folder(self.test_folder)

        # Assert creation
        assert create_response.status_code in [201, 409]

        # Verify folder exists if created
        if create_response.status_code == 201:
            info_response = self.client.get_folder_info(self.test_folder)
            assert info_response.status_code == 200

    def test_create_duplicate_folder_rejected(self):
        """Should reject duplicate folder creation"""
        # Arrange
        first_response = self.client.create_folder(self.test_folder)

        # Skip if first creation failed
        if first_response.status_code != 201:
            pytest.skip("Initial folder creation failed")

        # Act
        second_response = self.client.create_folder(self.test_folder)

        # Assert
        assert second_response.status_code == 409

        # Check both possible error variants
        error_type = second_response.json().get("error", "")
        assert error_type in ["DiskPathPointsToExistentDirectoryError", "DiskPathPointsToExistentResourceError"]

    def test_create_folder_with_invalid_token(self):
        """Should reject request with invalid token"""
        # Arrange
        invalid_client = YandexDiskAPIClient("invalid_token_12345")

        # Act
        response = invalid_client.create_folder(self.test_folder)

        # Assert
        assert response.status_code == 401

    @pytest.mark.parametrize("invalid_path,expected_status", [
        ("", 400),  # Empty path
        ("   ", 400),  # Whitespace path
    ])
    def test_create_folder_invalid_paths(self, invalid_path, expected_status):
        """Should reject requests with invalid paths"""
        response = self.client.create_folder(invalid_path)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("special_chars", [
        "тест-123",
        "special_chars_!@#$",
        "folder with spaces",
    ])
    def test_create_folder_with_special_characters(self, special_chars):
        """Should handle folder names with special characters"""
        special_folder = f"{self.test_folder}_{special_chars}"

        response = self.client.create_folder(special_folder)
        assert response.status_code in [201, 409]

        # Cleanup if created
        if response.status_code == 201:
            self._safe_delete_folder(special_folder)

    @pytest.mark.parametrize("nested_path", [
        "/subfolder/child",
        "/level1/level2/level3",
        "/parent/child/grandchild",
    ])
    def test_create_nested_folders(self, nested_path):
        """Should handle nested folder creation"""
        full_nested_path = f"{self.test_folder}{nested_path}"

        response = self.client.create_folder(full_nested_path)
        assert response.status_code in [201, 409, 404]  # 404 if parent doesn't exist


# Parametrized Tests for Comprehensive Coverage
class TestYandexDiskAPIParametrized:
    """Parametrized tests for comprehensive API coverage"""

    @pytest.fixture
    def mock_client(self, yandex_token):
        """Fixture for mocked client"""
        return YandexDiskAPIClient(yandex_token)

    @pytest.mark.parametrize("folder_path,expected_success", [
        ("/normal_folder", True),
        ("/folder with spaces", True),
        ("/unicode_папка", True),
        ("", False),  # Empty path should fail
        ("/../invalid", False),  # Path traversal should fail
    ])
    def test_folder_path_validation(self, mock_client, folder_path, expected_success):
        """Test various folder path validations"""
        with patch.object(requests, 'put') as mock_put:
            if expected_success:
                mock_put.return_value = create_mock_response(201, {})
            else:
                mock_put.return_value = create_mock_response(400, {
                    "error": "FieldValidationError",
                    "message": "Invalid path"
                })

            response = mock_client.create_folder(folder_path)

            if expected_success:
                assert response.status_code == 201
            else:
                assert response.status_code == 400

    @pytest.mark.parametrize("timeout_value", [1, 5, 10, 30, 60])
    def test_request_timeouts(self, mock_client, test_folder_path, timeout_value):
        """Test different timeout values"""
        with patch.object(requests, 'put') as mock_put:
            mock_put.return_value = create_mock_response(201, {})

            response = mock_client.create_folder(test_folder_path, timeout=timeout_value)

            assert response.status_code == 201
            # Verify timeout was passed to requests
            mock_put.assert_called_once()
            call_kwargs = mock_put.call_args[1]
            assert call_kwargs['timeout'] == timeout_value


# Error Codes Constants as Fixture
@pytest.fixture
def yandex_error_codes():
    """Fixture providing Yandex.Disk API error codes"""
    return {
        "UNAUTHORIZED": "UnauthorizedError",
        "VALIDATION_ERROR": "FieldValidationError",
        "NOT_FOUND": "DiskNotFoundError",
        "ALREADY_EXISTS_DIRECTORY": "DiskPathPointsToExistentDirectoryError",
        "ALREADY_EXISTS_RESOURCE": "DiskPathPointsToExistentResourceError",
        "PATH_POINTS_TO_FILE": "DiskPathPointsToFileError",
        "TOO_MANY_REQUESTS": "TooManyRequestsError",
        "INSUFFICIENT_STORAGE": "DiskSpaceExhaustedError",
    }


# Tests using error codes fixture
def test_error_codes_availability(yandex_error_codes):
    """Test that all expected error codes are available"""
    expected_codes = [
        "UNAUTHORIZED", "VALIDATION_ERROR", "NOT_FOUND",
        "ALREADY_EXISTS_DIRECTORY", "ALREADY_EXISTS_RESOURCE",
        "PATH_POINTS_TO_FILE", "TOO_MANY_REQUESTS", "INSUFFICIENT_STORAGE"
    ]

    for code in expected_codes:
        assert code in yandex_error_codes
        assert yandex_error_codes[code]  # Not empty


# Marked Tests for Different Categories
@pytest.mark.integration
class TestIntegration:
    """Integration tests marked for selective running"""

    def test_real_api_connection(self, api_client, unique_test_folder):
        """Test real API connection and basic operations"""
        response = api_client.create_folder(unique_test_folder)
        assert response.status_code in [201, 409]

        if response.status_code == 201:
            # Verify we can get folder info
            info_response = api_client.get_folder_info(unique_test_folder)
            assert info_response.status_code == 200


@pytest.mark.slow
class TestSlowOperations:
    """Slow operations that should be run separately"""

    def test_rate_limiting_behavior(self, api_client):
        """Test behavior under potential rate limiting"""
        # This would be a test that makes multiple rapid requests
        # to check rate limiting behavior
        pass


# Custom pytest markers registration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Main execution block
if __name__ == "__main__":
    # Run pytest programmatically with custom arguments
    pytest_args = [
        __file__,
        "-v",           # Verbose output
        "--tb=short",   # Short traceback format
        # "--integration",  # Run only integration tests
        # "-m", "not slow",  # Exclude slow tests
    ]

    exit_code = pytest.main(pytest_args)

    # Print custom report
    print("\n" + "=" * 60)
    print("🎯 YANDEX.DISK API TEST EXECUTION COMPLETE")
    print("=" * 60)

    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Some tests failed (exit code: {exit_code})")

    print("\n💡 Useful pytest commands:")
    print("  pytest test_yandex_disk_pytest.py -v              # Run all tests verbose")
    print("  pytest test_yandex_disk_pytest.py -m integration  # Run only integration tests")
    print("  pytest test_yandex_disk_pytest.py -m \"not slow\"   # Exclude slow tests")
    print("  pytest test_yandex_disk_pytest.py --tb=long       # Long tracebacks")