# 🚀 Deployment Guide

This guide explains how to deploy the Beacon Data Analyzer application on various platforms.

## 📋 Deployment Options

### 1. Streamlit Cloud (Recommended - Free)

The easiest way to deploy your app:

1. **Push to GitHub**: Ensure your code is in a public GitHub repository
2. **Visit Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io)
3. **Connect Repository**: Sign in with GitHub and select your repository
4. **Deploy**: Streamlit will automatically detect and deploy your app
5. **Access**: Your app will be available at `https://your-app-name.streamlit.app`

**Requirements for Streamlit Cloud:**
- Public GitHub repository
- `requirements.txt` file in root
- Main app file (already set up as `beacon_analyzer_app.py`)

### 2. Docker Container

Deploy using the included Dockerfile:

```bash
# Build the image
docker build -t beacon-analyzer .

# Run the container
docker run -p 8501:8501 beacon-analyzer
```

The app will be available at `http://localhost:8501`

### 3. GitHub Container Registry

Automatically builds and publishes Docker images:

1. The GitHub Action workflow will automatically build and push to GitHub Container Registry
2. Pull and run the latest image:
   ```bash
   docker pull ghcr.io/YOUR_USERNAME/edf_test:latest
   docker run -p 8501:8501 ghcr.io/YOUR_USERNAME/edf_test:latest
   ```

### 4. Local Development

For local development and testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run beacon_analyzer_app.py
```

## 🔧 Configuration

### Environment Variables

- `STREAMLIT_SERVER_PORT`: Port to run on (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Address to bind to (default: 0.0.0.0)

### Sample Database

The application comes with a sample database (`EDFBeaconCaptures.db`) for testing purposes.

## 🚦 CI/CD Pipeline

The repository includes GitHub Actions workflows:

- **`deploy.yml`**: Runs tests and validates the app
- **`docker-deploy.yml`**: Builds and publishes Docker images

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Run `python test_setup.py` to check dependencies
2. **Port Conflicts**: Change the port using `--server.port=8502`
3. **Database Issues**: Ensure the database file is accessible

### Logs and Debugging

For Docker deployments, check logs with:
```bash
docker logs [container_id]
```

## 🌐 Production Considerations

### Security
- Use HTTPS in production
- Consider authentication for sensitive data
- Validate uploaded database files

### Performance
- Monitor memory usage for large datasets
- Consider caching for frequently accessed data
- Use appropriate database indexing

### Scaling
- For high traffic, consider load balancing
- Use container orchestration (Kubernetes)
- Implement proper monitoring and alerting

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the application logs
3. Create an issue in the GitHub repository
