#!/usr/bin/env python3
"""
Quick test script to verify your Streamlit app setup
"""
import sys
import subprocess
import importlib.util

def test_import(module_name):
    """Test if a module can be imported"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {module_name} - OK")
            return True
        else:
            print(f"❌ {module_name} - NOT FOUND")
            return False
    except ImportError:
        print(f"❌ {module_name} - IMPORT ERROR")
        return False

def test_streamlit_command():
    """Test if streamlit command works"""
    try:
        result = subprocess.run([sys.executable, "-m", "streamlit", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Streamlit command - OK (version: {result.stdout.strip()})")
            return True
        else:
            print(f"❌ Streamlit command - FAILED")
            return False
    except Exception as e:
        print(f"❌ Streamlit command - ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Beacon Analyzer Dependencies")
    print("=" * 50)
    
    # Test required modules
    modules = ["streamlit", "pandas", "matplotlib", "plotly", "sqlite3", "tempfile", "os"]
    all_good = True
    
    for module in modules:
        if not test_import(module):
            all_good = False
    
    print()
    
    # Test streamlit command
    if not test_streamlit_command():
        all_good = False
    
    print()
    
    if all_good:
        print("🎉 All tests passed! Your app should work correctly.")
        print("💡 You can now run: python -m streamlit run beacon_analyzer_app.py")
    else:
        print("⚠️  Some issues detected. Please install missing dependencies.")
        print("💡 Run: python -m pip install streamlit plotly matplotlib pandas")
