"""
Unit tests for Yandex.Disk REST API
Test suite for folder creation functionality
"""

import os
import unittest
from unittest.mock import patch, Mock
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


class TestYandexDiskAPIMocked(unittest.TestCase):
    """
    Unit tests with mocked API responses
    Fast, isolated tests for business logic validation
    """

    def setUp(self):
        """Test setup"""
        self.token = "y0__xDIxNzRBhjblgMg9KLG2ROI4da4f-5cTi0XoH0CJ8sWTS3pHA"
        self.client = YandexDiskAPIClient(self.token)
        self.test_folder_path = "/test_folder"

    def _create_mock_response(self, status_code: int, json_data: dict) -> Mock:
        """Helper to create mock response"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data
        return mock_response

    # POSITIVE TEST CASES

    @patch.object(requests, 'put')
    def test_create_folder_success_201(self, mock_put):
        """Should return 201 when folder is successfully created"""
        # Arrange
        expected_response = {
            "href": f"{self.client.base_url}?path={self.test_folder_path}",
            "method": "GET",
            "templated": False
        }
        mock_put.return_value = self._create_mock_response(201, expected_response)

        # Act
        response = self.client.create_folder(self.test_folder_path)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_response)
        mock_put.assert_called_once_with(
            self.client.base_url,
            headers=self.client.headers,
            params={"path": self.test_folder_path},
            timeout=30
        )

    @patch.object(requests, 'put')
    def test_create_folder_already_exists_409(self, mock_put):
        """Should return 409 when folder already exists"""
        # Arrange
        expected_response = {
            "message": "Resource already exists",
            "description": "Specified resource '/test_folder' already exists",
            "error": "DiskPathPointsToExistentDirectoryError"  # Исправлено
        }
        mock_put.return_value = self._create_mock_response(409, expected_response)

        # Act
        response = self.client.create_folder(self.test_folder_path)

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "DiskPathPointsToExistentDirectoryError")

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_folder_appears_in_list_after_creation(self, mock_put, mock_get):
        """Should find created folder in files list"""
        # Arrange
        mock_put.return_value = self._create_mock_response(201, {})

        expected_files_response = {
            "items": [
                {
                    "path": f"disk:{self.test_folder_path}",
                    "name": "test_folder",
                    "type": "dir"
                }
            ],
            "limit": 20,
            "offset": 0
        }
        mock_get.return_value = self._create_mock_response(200, expected_files_response)

        # Act
        create_response = self.client.create_folder(self.test_folder_path)
        list_response = self.client.list_files()

        # Assert
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(list_response.status_code, 200)

        items = list_response.json()["items"]
        folder_found = any(
            item["path"] == f"disk:{self.test_folder_path}" and item["type"] == "dir"
            for item in items
        )
        self.assertTrue(folder_found)

    # NEGATIVE TEST CASES

    @patch.object(requests, 'put')
    def test_create_folder_unauthorized_401(self, mock_put):
        """Should return 401 with invalid token"""
        # Arrange
        expected_response = {
            "message": "Unauthorized",
            "description": "Invalid OAuth token",
            "error": "UnauthorizedError"
        }
        mock_put.return_value = self._create_mock_response(401, expected_response)

        # Act
        response = self.client.create_folder(self.test_folder_path)

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "UnauthorizedError")

    @patch.object(requests, 'put')
    def test_create_folder_bad_request_400(self, mock_put):
        """Should return 400 with invalid path"""
        # Arrange
        expected_response = {
            "message": "Field validation error",
            "description": "path: Field validation error",
            "error": "FieldValidationError"
        }
        mock_put.return_value = self._create_mock_response(400, expected_response)

        # Act
        response = self.client.create_folder("")  # Empty path

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "FieldValidationError")

    @patch.object(requests, 'put')
    def test_create_folder_forbidden_403(self, mock_put):
        """Should return 403 when API access is forbidden"""
        # Arrange
        expected_response = {
            "message": "API is not available",
            "description": "The resource API is not available",
            "error": "TooManyRequestsError"
        }
        mock_put.return_value = self._create_mock_response(403, expected_response)

        # Act
        response = self.client.create_folder(self.test_folder_path)

        # Assert
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"], "TooManyRequestsError")

    @patch.object(requests, 'put')
    def test_create_folder_not_found_404(self, mock_put):
        """Should return 404 when parent folder doesn't exist"""
        # Arrange
        expected_response = {
            "message": "Resource not found",
            "description": "Specified resource '/nonexistent_parent/new_folder' not found",
            "error": "DiskNotFoundError"
        }
        mock_put.return_value = self._create_mock_response(404, expected_response)

        # Act
        response = self.client.create_folder("/nonexistent_parent/new_folder")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "DiskNotFoundError")

    @patch.object(requests, 'put')
    def test_create_folder_conflict_409_file_exists(self, mock_put):
        """Should return 409 when path points to existing file"""
        # Arrange
        expected_response = {
            "message": "Resource conflict",
            "description": "Specified path '/existing_file' points to a file",
            "error": "DiskPathPointsToFileError"
        }
        mock_put.return_value = self._create_mock_response(409, expected_response)

        # Act
        response = self.client.create_folder("/existing_file")

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "DiskPathPointsToFileError")

    # NETWORK ERROR TESTS

    @patch.object(requests, 'put')
    def test_create_folder_connection_error(self, mock_put):
        """Should raise ConnectionError on network issues"""
        # Arrange
        mock_put.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # Act & Assert
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.client.create_folder(self.test_folder_path)

    @patch.object(requests, 'put')
    def test_create_folder_timeout_error(self, mock_put):
        """Should raise Timeout on request timeout"""
        # Arrange
        mock_put.side_effect = requests.exceptions.Timeout("Request timed out")

        # Act & Assert
        with self.assertRaises(requests.exceptions.Timeout):
            self.client.create_folder(self.test_folder_path, timeout=5)


class TestYandexDiskAPIReal(unittest.TestCase):
    """
    Integration tests with real Yandex.Disk API
    Requires valid OAuth token and internet connection
    """

    def setUp(self):
        """Test setup with unique folder names"""
        self.token = "y0__xDIxNzRBhjblgMg9KLG2ROI4da4f-5cTi0XoH0CJ8sWTS3pHA"
        self.client = YandexDiskAPIClient(self.token)
        self.test_folder = f"/test_api_{int(time.time())}_{hash(self)}"

    def tearDown(self):
        """Cleanup created test folders"""
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
        self.assertIn(response.status_code, [201, 409])  # 201 Created or 409 Already exists

        if response.status_code == 201:
            self.addCleanup(lambda: self._safe_delete_folder(self.test_folder))

    def test_create_and_verify_folder_exists(self):
        """Should create folder and verify its existence"""
        # Arrange & Act
        create_response = self.client.create_folder(self.test_folder)

        # Assert creation
        self.assertIn(create_response.status_code, [201, 409])

        # Verify folder exists
        if create_response.status_code == 201:
            info_response = self.client.get_folder_info(self.test_folder)
            self.assertEqual(info_response.status_code, 200)
            self.addCleanup(lambda: self._safe_delete_folder(self.test_folder))

    def test_create_duplicate_folder_rejected(self):
        """Should reject duplicate folder creation"""
        # Arrange
        first_response = self.client.create_folder(self.test_folder)

        # Skip if first creation failed
        if first_response.status_code != 201:
            self.skipTest("Initial folder creation failed")

        # Act
        second_response = self.client.create_folder(self.test_folder)

        # Assert
        self.assertEqual(second_response.status_code, 409)

        # Проверяем оба возможных варианта ошибки
        error_type = second_response.json().get("error", "")
        self.assertIn(error_type, ["DiskPathPointsToExistentDirectoryError", "DiskPathPointsToExistentResourceError"])

        # Cleanup
        self.addCleanup(lambda: self._safe_delete_folder(self.test_folder))

    def test_create_folder_with_invalid_token(self):
        """Should reject request with invalid token"""
        # Arrange
        invalid_client = YandexDiskAPIClient("invalid_token_12345")

        # Act
        response = invalid_client.create_folder(self.test_folder)

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_create_folder_with_empty_path(self):
        """Should reject request with empty path"""
        # Act
        response = self.client.create_folder("")

        # Assert
        self.assertEqual(response.status_code, 400)

    def test_create_folder_with_special_characters(self):
        """Should handle folder names with special characters"""
        # Arrange
        special_folder = f"{self.test_folder}_special_тест-123"

        # Act
        response = self.client.create_folder(special_folder)

        # Assert
        self.assertIn(response.status_code, [201, 409])

        # Cleanup
        if response.status_code == 201:
            self.addCleanup(lambda: self._safe_delete_folder(special_folder))

    def test_create_nested_folders(self):
        """Should handle nested folder creation"""
        # Arrange
        nested_folder = f"{self.test_folder}/subfolder/child"

        # Act
        response = self.client.create_folder(nested_folder)

        # Assert
        self.assertIn(response.status_code, [201, 409, 404])  # 404 if parent doesn't exist

        # Cleanup
        if response.status_code == 201:
            self.addCleanup(lambda: self._safe_delete_folder(self.test_folder))


class YandexDiskErrorCodes:
    """Constants for Yandex.Disk API error codes"""
    UNAUTHORIZED = "UnauthorizedError"
    VALIDATION_ERROR = "FieldValidationError"
    NOT_FOUND = "DiskNotFoundError"
    ALREADY_EXISTS_DIRECTORY = "DiskPathPointsToExistentDirectoryError"
    ALREADY_EXISTS_RESOURCE = "DiskPathPointsToExistentResourceError"  # Альтернативное название
    PATH_POINTS_TO_FILE = "DiskPathPointsToFileError"
    TOO_MANY_REQUESTS = "TooManyRequestsError"
    INSUFFICIENT_STORAGE = "DiskSpaceExhaustedError"


def run_tests():
    """Execute test suites with comprehensive reporting"""
    print("🚀 YANDEX.DISK API TEST SUITE")
    print("=" * 60)

    # Discover and load tests
    loader = unittest.TestLoader()

    # Mocked tests (fast, isolated)
    mocked_suite = loader.loadTestsFromTestCase(TestYandexDiskAPIMocked)

    # Real API tests (integration)
    real_suite = loader.loadTestsFromTestCase(TestYandexDiskAPIReal)

    # Run mocked tests
    print("\n🔧 MOCKED TESTS - Business Logic Validation")
    print("-" * 50)
    mocked_runner = unittest.TextTestRunner(verbosity=2, resultclass=unittest.TextTestResult)
    mocked_result = mocked_runner.run(mocked_suite)

    # Run real API tests
    print("\n🌐 REAL API TESTS - Integration Validation")
    print("-" * 50)
    real_runner = unittest.TextTestRunner(verbosity=2, resultclass=unittest.TextTestResult)
    real_result = real_runner.run(real_suite)

    # Generate test report
    print("\n" + "=" * 60)
    print("📊 TEST EXECUTION REPORT")
    print("=" * 60)

    total_tests = mocked_result.testsRun + real_result.testsRun
    total_failures = len(mocked_result.failures) + len(real_result.failures)
    total_errors = len(mocked_result.errors) + len(real_result.errors)
    total_success = total_tests - total_failures - total_errors

    print(f"Mocked Tests:  {mocked_result.testsRun - len(mocked_result.failures) - len(mocked_result.errors)}/{mocked_result.testsRun} passed")
    print(f"Real API Tests: {real_result.testsRun - len(real_result.failures) - len(real_result.errors)}/{real_result.testsRun} passed")
    print(f"Total:         {total_success}/{total_tests} passed")

    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"❌ {total_failures} failures, {total_errors} errors detected")

        # Show detailed failure info
        if mocked_result.failures:
            print(f"\nMocked test failures:")
            for test, traceback in mocked_result.failures:
                print(f"  - {test}")
        if real_result.failures:
            print(f"\nReal API test failures:")
            for test, traceback in real_result.failures:
                print(f"  - {test}")


if __name__ == '__main__':
    run_tests()