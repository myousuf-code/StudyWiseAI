#!/usr/bin/env python3
"""
StudyWiseAI Test Suite Runner
Automatically starts server and runs all tests
"""
import subprocess
import time
import sys
import signal
from pathlib import Path
import psutil

class TestSuiteRunner:
    def __init__(self):
        self.base_path = Path("C:/Code/StudyWiseAI")
        self.server_process = None
        
    def kill_existing_servers(self):
        """Kill any existing servers running on port 8000"""
        print("🔍 Checking for existing servers...")
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if process is using port 8000
                    for conn in proc.connections():
                        if conn.laddr.port == 8000:
                            print(f"🛑 Killing existing server process {proc.pid}")
                            proc.terminate()
                            proc.wait(timeout=5)
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"⚠️ Warning: Could not check for existing servers: {e}")
    
    def start_server(self):
        """Start the StudyWiseAI server"""
        print("🚀 Starting StudyWiseAI server...")
        
        # Kill any existing servers first
        self.kill_existing_servers()
        
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                str(self.base_path / "venv/Scripts/python.exe"),
                "-m", "uvicorn", 
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            cwd=self.base_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            print("⏳ Waiting for server to initialize...")
            time.sleep(8)  # Give server time to fully start
            
            if self.server_process.poll() is None:
                print("✅ Server started successfully")
                return True
            else:
                print("❌ Server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server"""
        if self.server_process and self.server_process.poll() is None:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("✅ Server stopped")
    
    def run_quick_test(self):
        """Run the quick test script"""
        print("\n" + "="*60)
        print("🧪 RUNNING QUICK TEST SUITE")
        print("="*60)
        
        try:
            result = subprocess.run([
                str(self.base_path / "venv/Scripts/python.exe"),
                "quick_test.py"
            ],
            cwd=self.base_path,
            timeout=600  # 10 minutes max
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏰ Test suite timed out after 10 minutes")
            return False
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            return False
    
    def run_full_test_suite(self):
        """Run the complete test suite with server management"""
        print("🤖 StudyWiseAI - Automated Test Suite Runner")
        print("="*60)
        print("This will:")
        print("1. Start the server automatically")
        print("2. Run all functionality tests")
        print("3. Stop the server when done")
        print("4. Provide a complete test report")
        print("-"*60)
        
        try:
            # Start server
            if not self.start_server():
                return False
            
            # Run tests
            test_success = self.run_quick_test()
            
            return test_success
            
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Test suite error: {e}")
            return False
        finally:
            # Always stop server
            self.stop_server()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for clean shutdown"""
        def signal_handler(signum, frame):
            print("\n🛑 Received interrupt signal, shutting down...")
            self.stop_server()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

def main():
    runner = TestSuiteRunner()
    runner.setup_signal_handlers()
    
    print("Choose test option:")
    print("1. Full automated test (starts server + runs tests)")
    print("2. Quick test only (assumes server is running)")
    print("3. Just start server")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return
    
    if choice == "1":
        success = runner.run_full_test_suite()
        if success:
            print("\n🎉 All tests completed successfully!")
        else:
            print("\n⚠️ Some tests failed - check output above")
    
    elif choice == "2":
        runner.run_quick_test()
    
    elif choice == "3":
        if runner.start_server():
            print("\n✅ Server is running at http://localhost:8000")
            print("Press Ctrl+C to stop the server")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                runner.stop_server()
        else:
            print("\n❌ Failed to start server")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()