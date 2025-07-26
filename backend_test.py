#!/usr/bin/env python3
"""
Backend API Testing for Telegram Bot System
Tests all API endpoints to ensure they work correctly
"""

import requests
import sys
import json
from datetime import datetime

class TelegramBotAPITester:
    def __init__(self, base_url="https://c96d850f-73f9-40d1-ace6-5b78aa62cd15.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")

    def test_root_endpoint(self):
        """Test GET /api/ endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Root API Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Root API Endpoint", False, f"- Error: {str(e)}")
            return False

    def test_admin_login(self):
        """Test POST /api/login/admin endpoint"""
        try:
            credentials = {"username": "admin", "password": "admin123"}
            response = self.session.post(f"{self.base_url}/api/login/admin", json=credentials)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('success', False) and data.get('role') == 'admin'
                details = f"- Status: {response.status_code}, Success: {data.get('success')}, Role: {data.get('role')}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Admin Login", success, details)
            return success
            
        except Exception as e:
            self.log_test("Admin Login", False, f"- Error: {str(e)}")
            return False

    def test_teacher_login(self):
        """Test POST /api/login/teacher endpoint"""
        try:
            credentials = {"username": "teacher", "password": "teacher123"}
            response = self.session.post(f"{self.base_url}/api/login/teacher", json=credentials)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('success', False) and data.get('role') == 'teacher'
                details = f"- Status: {response.status_code}, Success: {data.get('success')}, Role: {data.get('role')}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Teacher Login", success, details)
            return success
            
        except Exception as e:
            self.log_test("Teacher Login", False, f"- Error: {str(e)}")
            return False

    def test_student_login(self):
        """Test POST /api/login/student endpoint"""
        try:
            credentials = {"username": "student", "password": "student123"}
            response = self.session.post(f"{self.base_url}/api/login/student", json=credentials)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('success', False) and data.get('role') == 'student'
                details = f"- Status: {response.status_code}, Success: {data.get('success')}, Role: {data.get('role')}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Student Login", success, details)
            return success
            
        except Exception as e:
            self.log_test("Student Login", False, f"- Error: {str(e)}")
            return False

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            credentials = {"username": "invalid", "password": "invalid"}
            response = self.session.post(f"{self.base_url}/api/login/admin", json=credentials)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                # Should return success: false for invalid credentials
                success = not data.get('success', True)
                details = f"- Status: {response.status_code}, Success: {data.get('success')}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Invalid Login Handling", success, details)
            return success
            
        except Exception as e:
            self.log_test("Invalid Login Handling", False, f"- Error: {str(e)}")
            return False

    def test_users_endpoint(self):
        """Test GET /api/users endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/users")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Status: {response.status_code}, Users count: {len(data) if isinstance(data, list) else 'N/A'}"
            else:
                details = f"- Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Users Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Users Endpoint", False, f"- Error: {str(e)}")
            return False

    def test_status_endpoints(self):
        """Test status check endpoints"""
        try:
            # Test POST /api/status
            status_data = {"client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"}
            response = self.session.post(f"{self.base_url}/api/status", json=status_data)
            
            post_success = response.status_code == 200
            if post_success:
                created_status = response.json()
                post_details = f"- POST Status: {response.status_code}, ID: {created_status.get('id', 'N/A')}"
            else:
                post_details = f"- POST Status: {response.status_code}, Response: {response.text[:100]}"
            
            self.log_test("Status Creation", post_success, post_details)
            
            # Test GET /api/status
            response = self.session.get(f"{self.base_url}/api/status")
            get_success = response.status_code == 200
            
            if get_success:
                statuses = response.json()
                get_details = f"- GET Status: {response.status_code}, Count: {len(statuses) if isinstance(statuses, list) else 'N/A'}"
            else:
                get_details = f"- GET Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test("Status Retrieval", get_success, get_details)
            
            return post_success and get_success
            
        except Exception as e:
            self.log_test("Status Endpoints", False, f"- Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Telegram Bot API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test all endpoints
        self.test_root_endpoint()
        self.test_admin_login()
        self.test_teacher_login()
        self.test_student_login()
        self.test_invalid_login()
        self.test_users_endpoint()
        self.test_status_endpoints()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Backend API is working correctly.")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Please check the issues above.")
            return False

def main():
    """Main function to run tests"""
    tester = TelegramBotAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())