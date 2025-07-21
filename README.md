# 📡 Beacon Data Analyzer

A powerful web application for analyzing beacon sensor data with interactive visualizations.

![Beacon Analyzer](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **📊 Interactive Data Visualization** - Dynamic plots with Plotly
- **🎛️ Real-time Filtering** - Filter by date, time, and beacons
- **📈 Multi-sensor Analysis** - Temperature and RSSI data
- **🔍 Data Exploration** - Summary statistics and insights
- **📱 Responsive Design** - Works on desktop and mobile

## 🚀 Live Demo

**[🌐 Try the Live App Here](https://your-app-name.streamlit.app)**

> 📚 **New to deployment?** Check out our [Deployment Guide](DEPLOYMENT.md) for step-by-step instructions!

## 📸 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Interactive Plots
![Plots](screenshots/plots.png)

## 🏃‍♂️ Quick Start

### Option 1: Online (Recommended)
Just visit the [live app](https://your-app-name.streamlit.app) and upload your database file!

### Option 2: Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/beacon-analyzer.git
   cd beacon-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run beacon_analyzer_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Option 3: Windows Quick Start
- Download and extract the zip file
- Double-click `setup_and_run.bat`
- The app will open automatically!

## 📋 Requirements

- Python 3.9+
- Streamlit
- Plotly
- Pandas
- Matplotlib

## 📁 Project Structure

```
beacon-analyzer/
├── beacon_analyzer_app.py      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── setup_and_run.bat          # Windows setup script
├── setup_and_run.ps1          # PowerShell setup script
├── test_setup.py              # Test dependencies
├── Dockerfile                 # Docker deployment
├── EDFBeaconCaptures.db       # Sample database (optional)
└── README.md                  # This file
```

## 🎯 How to Use

1. **Upload Database**: Drop your SQLite database file (.db, .sqlite, .sqlite3)
2. **Select Beacons**: Choose which beacons to analyze
3. **Set Time Range**: Pick your date and time filters
4. **Analyze**: Click "Analyze Data" to generate interactive plots
5. **Explore**: Hover over plots, zoom, and explore your data

## 🔧 Database Schema

Your database should have these tables:
- `Beacon` - Beacon information with Description
- `BeaconEvent` - Event data with DateTime, ExternalSensorTemperature, RSSI, etc.

## 🐳 Docker Deployment

Build and run with Docker:

```bash
docker build -t beacon-analyzer .
docker run -p 8501:8501 beacon-analyzer
```

Or use our pre-built GitHub Container Registry image:

```bash
docker pull ghcr.io/YOUR_USERNAME/edf_test:latest
docker run -p 8501:8501 ghcr.io/YOUR_USERNAME/edf_test:latest
```

## 🚀 Deployment Options

| Platform | Difficulty | Cost | Best For |
|----------|------------|------|----------|
| **Streamlit Cloud** | ⭐ Easy | Free | Quick demos, personal projects |
| **Docker + Cloud** | ⭐⭐ Medium | Varies | Production apps |
| **GitHub Pages** | ⭐⭐⭐ Hard | Free | Static hosting only |

📋 **Quick Deploy:** See our detailed [Deployment Guide](DEPLOYMENT.md) for all options!

## 📊 Data Format

The app expects SQLite database with:
- **DateTime**: Timestamp of the measurement
- **BeaconDescription**: Name/ID of the beacon
- **ExternalSensorTemperature**: Temperature readings (°C)
- **ExternalSensorTemperatureExt1**: Additional temperature sensor
- **RSSI**: Signal strength (dBm)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Data analysis with [Pandas](https://pandas.pydata.org/)

## 📞 Support

If you encounter any issues or have questions:
- 🐛 [Report bugs](https://github.com/yourusername/beacon-analyzer/issues)
- 💡 [Request features](https://github.com/yourusername/beacon-analyzer/issues)
- 📧 Email: your.email@example.com

---

⭐ If you found this project helpful, please consider giving it a star!
