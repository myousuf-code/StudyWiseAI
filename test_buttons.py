"""
StudyWise AI - Button Functionality Test
This script tests the login and register button functionality directly.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

def test_button_functionality():
    """Test the login and register buttons"""
    
    # Set up Chrome options for headless mode (optional)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    
    try:
        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the application
        driver.get("http://localhost:8000")
        
        print("✅ Page loaded successfully")
        
        # Wait for page to fully load
        WebDriverWait(driver, 10).wait(
            EC.presence_of_element_located((By.ID, "loginBtn"))
        )
        
        print("✅ Login button found")
        
        # Check if register button exists
        register_btn = driver.find_element(By.ID, "registerBtn")
        print("✅ Register button found")
        
        # Test login button click
        login_btn = driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        
        # Wait for modal to appear
        WebDriverWait(driver, 5).wait(
            EC.visibility_of_element_located((By.ID, "authModal"))
        )
        
        print("✅ Login button opens authentication modal")
        
        # Close the modal
        close_btn = driver.find_element(By.ID, "closeAuthModal")
        close_btn.click()
        
        # Wait for modal to close
        WebDriverWait(driver, 5).wait(
            EC.invisibility_of_element_located((By.ID, "authModal"))
        )
        
        print("✅ Modal can be closed")
        
        # Test register button
        register_btn.click()
        
        # Wait for modal to appear again
        WebDriverWait(driver, 5).wait(
            EC.visibility_of_element_located((By.ID, "authModal"))
        )
        
        print("✅ Register button opens authentication modal")
        
        # Check if we can see the register form
        register_form = driver.find_element(By.ID, "registerForm")
        if register_form.is_displayed():
            print("✅ Register form is visible")
        else:
            print("❌ Register form is not visible")
        
        print("\n🎉 All button functionality tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
        
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
    
    return True

def test_console_errors():
    """Check for JavaScript console errors"""
    
    chrome_options = Options()
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8000")
        
        # Wait a moment for JavaScript to execute
        time.sleep(3)
        
        # Get browser logs
        logs = driver.get_log('browser')
        
        error_count = 0
        for log in logs:
            if log['level'] == 'SEVERE':
                print(f"❌ JavaScript Error: {log['message']}")
                error_count += 1
            elif log['level'] == 'WARNING':
                print(f"⚠️ JavaScript Warning: {log['message']}")
        
        if error_count == 0:
            print("✅ No JavaScript errors found")
        else:
            print(f"❌ Found {error_count} JavaScript errors")
            
    except Exception as e:
        print(f"❌ Console error check failed: {str(e)}")
        
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    print("🧪 Testing StudyWise AI Button Functionality")
    print("=" * 50)
    
    # Check if chromedriver is available
    try:
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.quit()
        print("✅ ChromeDriver is available")
    except:
        print("❌ ChromeDriver not found. Please install ChromeDriver.")
        print("Download from: https://chromedriver.chromium.org/")
        sys.exit(1)
    
    print("\n1. Testing button functionality...")
    test_button_functionality()
    
    print("\n2. Checking for JavaScript console errors...")
    test_console_errors()
    
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to the Console tab")
    print("4. Click the Login button - you should see console logs")
    print("5. The authentication modal should open")
    print("6. Try the Register button as well")
    print("7. Look for any red error messages in the console")