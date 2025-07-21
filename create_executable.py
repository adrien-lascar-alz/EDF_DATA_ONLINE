# Create Standalone Executable for Beacon Analyzer
# Run this script to create a .exe file that includes everything

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")

def create_executable():
    """Create standalone executable"""
    print("🔨 Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onedir",  # Create a directory with all dependencies
        "--windowed",  # Hide console window
        "--add-data", "EDFBeaconCaptures.db;.",  # Include database file
        "--name", "BeaconAnalyzer",
        "--icon", "📡",  # You can add an .ico file here
        "beacon_analyzer_app.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable created successfully!")
        print("📁 Find your executable in the 'dist/BeaconAnalyzer' folder")
        print("📋 You can share the entire 'BeaconAnalyzer' folder with others")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {e}")

if __name__ == "__main__":
    print("🚀 Beacon Analyzer - Executable Creator")
    print("=" * 50)
    
    install_pyinstaller()
    create_executable()
    
    print("\n📋 Next steps:")
    print("1. Find the 'dist/BeaconAnalyzer' folder")
    print("2. Zip the entire folder")
    print("3. Share the zip file with others")
    print("4. Recipients just need to run 'BeaconAnalyzer.exe'")
