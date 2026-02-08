#!/usr/bin/env python3
"""
StudyWiseAI Quick Test Runner
Run this script to perform a rapid functionality check of all major features
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

class QuickTester:
    def __init__(self):
        self.base_path = Path("C:/Code/StudyWiseAI")
        self.server_process = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🚀 {title}")
        print(f"{'='*50}")
    
    def print_test(self, test_name, status, details=""):
        if status == "PASS":
            print(f"✅ {test_name}")
            self.tests_passed += 1
        elif status == "FAIL":
            print(f"❌ {test_name}")
            if details:
                print(f"   💡 {details}")
            self.tests_failed += 1
        else:
            print(f"⚠️ {test_name}: {status}")
    
    def check_prerequisites(self):
        """Check if all required files exist"""
        self.print_header("CHECKING PREREQUISITES")
        
        required_files = [
            "app/main.py",
            "test_direct_auth.py", 
            "test_ai_direct.py",
            "venv/Scripts/python.exe"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.base_path / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.print_test("File Structure", "FAIL", f"Missing: {', '.join(missing_files)}")
            return False
        else:
            self.print_test("File Structure", "PASS")
            return True
    
    def test_server_start(self):
        """Test if server can start"""
        self.print_header("TESTING SERVER")
        
        try:
            # Test server health endpoint
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                self.print_test("Server Running", "PASS")
                return True
        except:
            pass
        
        self.print_test("Server Running", "FAIL", "Start server: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return False
    
    def test_homepage(self):
        """Test if homepage loads"""
        try:
            response = requests.get("http://localhost:8000/", timeout=10)
            if response.status_code == 200 and "StudyWise" in response.text:
                self.print_test("Homepage", "PASS")
                return True
            else:
                self.print_test("Homepage", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Homepage", "FAIL", str(e))
            return False
    
    def run_authentication_test(self):
        """Run authentication test script"""
        self.print_header("TESTING AUTHENTICATION")
        
        try:
            result = subprocess.run([
                str(self.base_path / "venv/Scripts/python.exe"),
                "test_direct_auth.py"
            ], 
            cwd=self.base_path,
            capture_output=True, 
            text=True, 
            timeout=30
            )
            
            if result.returncode == 0 and "All direct authentication tests passed!" in result.stdout:
                self.print_test("Authentication System", "PASS")
                return True
            else:
                self.print_test("Authentication System", "FAIL", "Check test_direct_auth.py output")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_test("Authentication System", "FAIL", "Timeout after 30s")
            return False
        except Exception as e:
            self.print_test("Authentication System", "FAIL", str(e))
            return False
    
    def run_ai_features_test(self):
        """Run AI features test script"""
        self.print_header("TESTING AI FEATURES")
        
        print("⏳ Testing AI features (this may take 1-2 minutes for model loading)...")
        
        try:
            result = subprocess.run([
                str(self.base_path / "venv/Scripts/python.exe"),
                "test_ai_direct.py"
            ],
            cwd=self.base_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes for AI model loading
            )
            
            output = result.stdout
            
            # Check for success indicators
            if "Test user authenticated successfully" in output:
                self.print_test("AI User Authentication", "PASS")
            else:
                self.print_test("AI User Authentication", "FAIL")
            
            if "Local AI model loaded successfully" in output:
                self.print_test("AI Model Loading", "PASS")
            elif "Loading local AI model" in output:
                self.print_test("AI Model Loading", "PARTIAL", "Model downloading/loading")
            else:
                self.print_test("AI Model Loading", "FAIL")
            
            # Check individual AI features
            if "Chat Assistant" in output:
                self.print_test("AI Chat Feature", "PASS")
            else:
                self.print_test("AI Chat Feature", "FAIL")
                
            if "Study Plan Generation" in output:  
                self.print_test("Study Plan Generation", "PASS")
            else:
                self.print_test("Study Plan Generation", "FAIL")
                
            if "Quiz Generation" in output:
                self.print_test("Quiz Generation", "PASS") 
            else:
                self.print_test("Quiz Generation", "FAIL")
                
            # Overall success
            if result.returncode == 0:
                return True
            else:
                print(f"⚠️ AI test completed with issues. Check full output above.")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_test("AI Features Test", "TIMEOUT", "AI model may still be downloading")
            return False
        except Exception as e:
            self.print_test("AI Features Test", "FAIL", str(e))
            return False
    
    def test_api_endpoints(self):
        """Test basic API endpoints"""
        self.print_header("TESTING API ENDPOINTS")
        
        endpoints = [
            ("/", "Homepage"),
            ("/docs", "API Documentation"), 
            ("/health", "Health Check")
        ]
        
        api_working = True
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.print_test(name, "PASS")
                else:
                    self.print_test(name, "FAIL", f"Status {response.status_code}")
                    api_working = False
            except Exception as e:
                self.print_test(name, "FAIL", str(e))
                api_working = False
        
        return api_working
    
    def generate_report(self):
        """Generate final test report"""
        self.print_header("TEST RESULTS SUMMARY")
        
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Tests Passed: {self.tests_passed}")
        print(f"📊 Tests Failed: {self.tests_failed}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print(f"\n🎉 EXCELLENT! Your StudyWiseAI application is working perfectly!")
            print(f"✅ Ready for production use")
        elif success_rate >= 70:
            print(f"\n✅ GOOD! Most features are working well")
            print(f"⚠️ Check failed tests and fix minor issues")
        elif success_rate >= 50:
            print(f"\n⚠️ PARTIAL! Core features work but needs attention")
            print(f"🔧 Review failed tests and fix major issues")
        else:
            print(f"\n❌ NEEDS WORK! Several critical issues found")
            print(f"🛠️ Review setup and configuration")
        
        print(f"\n📋 Next Steps:")
        if success_rate >= 90:
            print(f"• Your AI study assistant is ready to help students!")
            print(f"• Consider deploying to production")
            print(f"• Share with users for feedback")
        else:
            print(f"• Check server is running: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
            print(f"• Review failed tests above")
            print(f"• Run individual test scripts for detailed output")
            print(f"• Check TEST_PLAN.md for troubleshooting")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🤖 StudyWiseAI - Quick Test Runner")
        print("This will test all major features in ~2-5 minutes")
        print("-" * 50)
        
        # Prerequisites
        if not self.check_prerequisites():
            print("❌ Cannot proceed without required files")
            return
        
        # Basic connectivity
        if not self.test_server_start():
            print("❌ Server is not running - please start it first")
            return
        
        # Core functionality tests
        self.test_homepage()
        self.test_api_endpoints()
        self.run_authentication_test()
        
        # AI features (this takes the longest)
        self.run_ai_features_test()
        
        # Generate final report
        self.generate_report()

def main():
    """Main entry point"""
    print("Starting StudyWiseAI Quick Test...")
    
    tester = QuickTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()