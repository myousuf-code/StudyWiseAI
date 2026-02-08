#!/usr/bin/env python3
"""
StudyWiseAI Quick Start Script
Automates the initial setup and launch process
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current Python version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    venv_exists = Path("venv").exists()
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    return venv_exists, in_venv

def create_virtual_environment():
    """Create a virtual environment"""
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📥 Installing dependencies...")
    try:
        # Use the virtual environment's pip
        if os.name == 'nt':  # Windows
            pip_path = "venv\\Scripts\\pip"
        else:  # Unix/Linux/macOS
            pip_path = "venv/bin/pip"
        
        subprocess.run([pip_path, "install", "-r", "requirements-minimal.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    except FileNotFoundError:
        print("❌ Virtual environment pip not found")
        return False

def setup_environment_file():
    """Set up environment configuration"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("🔧 Setting up environment configuration...")
        shutil.copy(env_example, env_file)
        print("✅ Environment file created (.env)")
        print("⚠️  Please edit .env file with your actual configuration values")
        return True
    elif env_file.exists():
        print("✅ Environment file already exists")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def check_database_config():
    """Check database configuration"""
    print("🗄️  Database configuration:")
    print("   - Make sure PostgreSQL is running")
    print("   - Update DATABASE_URL in .env file")
    print("   - Default: postgresql://studywise:password@localhost:5432/studywiseai")
    return True

def check_openai_config():
    """Check OpenAI configuration"""
    print("🤖 AI Configuration:")
    print("   - Get your OpenAI API key from: https://platform.openai.com/account/api-keys")
    print("   - Update OPENAI_API_KEY in .env file")
    print("   - Make sure you have sufficient credits")
    return True

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    try:
        # Use the virtual environment's python
        if os.name == 'nt':  # Windows
            python_path = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS  
            python_path = "venv/bin/python"
        
        subprocess.run([python_path, "-m", "app.core.init_db"], check=True)
        print("✅ Database initialized successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize database")
        print("   Make sure PostgreSQL is running and connection details are correct")
        return False
    except FileNotFoundError:
        print("❌ Virtual environment python not found")
        return False

def start_server():
    """Start the development server"""
    print("🚀 Starting development server...")
    try:
        # Use the virtual environment's python
        if os.name == 'nt':  # Windows
            python_path = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS
            python_path = "venv/bin/python"
        
        print("✅ Server starting at http://localhost:8000")
        print("📚 API docs available at http://localhost:8000/docs")
        print("🔧 Press Ctrl+C to stop the server")
        subprocess.run([python_path, "-m", "uvicorn", "app.main:app", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        return False

def main():
    """Main setup function"""
    print("🎓 StudyWiseAI Quick Start Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    venv_exists, in_venv = check_virtual_environment()
    
    if not venv_exists:
        if not create_virtual_environment():
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    if in_venv:
        print("✅ Already running in virtual environment")
    else:
        print("⚠️  Not in virtual environment. Activating...")
        print("   Please run the activation command and then run this script again:")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("   source venv/bin/activate")
        
        # Try to use virtual environment directly
        if not install_dependencies():
            sys.exit(1)
    
    # Setup environment
    setup_environment_file()
    
    # Configuration reminders
    check_database_config()
    check_openai_config()
    
    print("\n" + "=" * 40)
    print("🔧 CONFIGURATION REQUIRED:")
    print("   1. Edit .env file with your actual values")
    print("   2. Make sure PostgreSQL is running")
    print("   3. Add your OpenAI API key")
    print("=" * 40)
    
    response = input("\nContinue with database initialization? (y/n): ")
    if response.lower() in ['y', 'yes']:
        if initialize_database():
            print("\n🎉 Setup completed successfully!")
            print("\nTest User Credentials:")
            print("   Email: test@studywiseai.com")
            print("   Password: testpassword123")
            
            response = input("\nStart the development server? (y/n): ")
            if response.lower() in ['y', 'yes']:
                start_server()
        else:
            print("\n⚠️  Database initialization failed.")
            print("   Please check your database configuration and try again.")
    else:
        print("\n📝 Manual steps to complete setup:")
        print("   1. Edit .env file")
        print("   2. Run: python -m app.core.init_db")
        print("   3. Run: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()