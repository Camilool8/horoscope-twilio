# 🌟 Daily Horoscope Sender

A containerized application that sends daily Spanish horoscopes for Cancer and Aquarius via email and SMS. Perfect for showing love through personalized daily messages! 💕

## ✨ Features

- 📧 **Email delivery** with beautifully formatted horoscopes
- 📱 **SMS delivery** via Twilio to both you and your girlfriend
- 🌐 **RapidAPI integration** for reliable horoscope data
- 🌍 **Google Translate integration** for accurate Spanish translations
- 🏗️ **Containerized** with Docker for easy deployment
- ☸️ **Kubernetes ready** with full manifests
- 🕰️ **Scheduled delivery** at configurable times
- 🌍 **Personalized Spanish horoscopes** for Cancer ♋ and Aquarius ♒
- 🔒 **Secure** with non-root containers and secrets management
- 📊 **Health checks** and monitoring ready

## 🚀 Quick Start

### Setup

### Prerequisites

- Docker and Docker Compose
- Gmail account with App Password enabled
- Twilio account (for SMS)
- RapidAPI account with Horoscope API access
- Kubernetes cluster (for production)

### 1. Clone and Setup

```bash
# Clone the repository (or copy the files)
mkdir horoscope-sender && cd horoscope-sender

# Copy the environment template
cp .env.template .env

# Edit with your credentials
nano .env
```

### 2. Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `EMAIL_PASSWORD`

### 3. RapidAPI Setup

1. Sign up at [RapidAPI.com](https://rapidapi.com)
2. Subscribe to the "Horoscope Astrology" API
3. Get your API key from the dashboard
4. Add the key to your `.env` file as `RAPIDAPI_KEY`

### 4. Twilio Setup

1. Sign up at [Twilio.com](https://twilio.com)
2. Get your Account SID and Auth Token from the dashboard
3. Buy a phone number or use the trial number
4. Add these to your `.env` file

### 5. Local Testing

```bash
# Test your API connections first
python3 test_rapidapi.py

# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Test immediate delivery
docker-compose exec horoscope-sender python -c "
from horoscope_sender import HoroscopeService
service = HoroscopeService()
service.send_daily_horoscopes()
"

# Stop the service
docker-compose down
```

### 6. Kubernetes Deployment

```bash

# Rename the file to horoscope-deployment.yaml
mv horoscope-deployment.yaml.template horoscope-deployment.yaml

# Update the image in horoscope-deployment.yaml
sed -i 's/your-registry/your-actual-registry/g' horoscope-deployment.yaml

# Build and push your image
docker build -t your-registry/horoscope-sender:latest .
docker push your-registry/horoscope-sender:latest

# Deploy to Kubernetes
kubectl apply -f horoscope-deployment.yaml

# Update secrets with your actual values
kubectl -n horoscope-app edit secret horoscope-secrets

# Check deployment
kubectl -n horoscope-app get pods
kubectl -n horoscope-app logs -f deployment/horoscope-sender
```

## 📁 Project Structure

```
horoscope-sender/
├── horoscope_sender.py                     # Main application with Google Translate
├── healthcheck.py                          # Health check endpoint
├── test_rapidapi.py                        # API + Translation testing script
├── requirements.txt                        # Python dependencies (includes googletrans)
├── Dockerfile                              # Container configuration
├── horoscope-deployment.yaml.template      # Kubernetes deployment template
├── .env.template                           # Environment variables template
└── README.md                               # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable              | Description                           | Required |
| --------------------- | ------------------------------------- | -------- |
| `EMAIL_USER`          | Gmail address                         | Yes      |
| `EMAIL_PASSWORD`      | Gmail app password                    | Yes      |
| `RECIPIENT_EMAIL`     | Girlfriend's email                    | Yes      |
| `RECIPIENT_PHONE`     | Girlfriend's phone (+country code)    | Yes      |
| `TWILIO_ACCOUNT_SID`  | Twilio account identifier             | Yes      |
| `TWILIO_AUTH_TOKEN`   | Twilio authentication token           | Yes      |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number              | Yes      |
| `RAPIDAPI_KEY`        | RapidAPI key for horoscope data       | Yes      |
| `SMTP_SERVER`         | SMTP server (default: smtp.gmail.com) | No       |
| `SMTP_PORT`           | SMTP port (default: 587)              | No       |
| `SEND_ON_STARTUP`     | Send immediately on start (testing)   | No       |
| `TZ`                  | Timezone (default: UTC)               | No       |

### Scheduling

- **Default**: 8:00 AM daily
- **Kubernetes CronJob**: Alternative scheduling method included
- **Timezone**: Configurable via environment variables

## 🏗️ Deployment Options

### Option 1: Kubernetes Deployment (Persistent service)

```bash
kubectl apply -f k8s-manifests.yaml
```

### Option 2: Cloud Functions/Lambda

The code can be adapted for serverless platforms:

- AWS Lambda with EventBridge
- Google Cloud Functions with Cloud Scheduler
- Azure Functions with Timer Trigger

## 🔧 Customization

### Adding More Signs

Edit `horoscope_sender.py` and add signs to the `spanish_horoscopes` dictionary:

```python
spanish_horoscopes = {
    'cancer': [...],
    'aquarius': [...],
    'leo': ['Nuevo horóscopo para Leo...'],  # Add new signs here
}
```

### Changing Schedule

Modify the schedule in `horoscope_sender.py`:

```python
# Change time (24-hour format)
schedule.every().day.at("09:30").do(service.send_daily_horoscopes)

# Multiple times per day
schedule.every().day.at("08:00").do(service.send_daily_horoscopes)
schedule.every().day.at("20:00").do(service.send_daily_horoscopes)
```

### Custom Messages

Modify the message templates in the `send_daily_horoscopes()` method to personalize the content.

## 🔍 Monitoring

### Health Checks

- **HTTP**: `GET /health` returns application status
- **Kubernetes**: Liveness and readiness probes configured
- **Docker**: Built-in health check included

### Logging

```bash
# Kubernetes
kubectl -n horoscope-app logs -f deployment/horoscope-sender

# Follow live logs
kubectl -n horoscope-app logs -f -l app=horoscope-sender
```

## 🛠️ Troubleshooting

### Common Issues

1. **Gmail Authentication Failed**

   - Ensure 2FA is enabled
   - Use App Password, not regular password
   - Check "Less secure app access" if needed

2. **Twilio SMS Not Sending**

   - Verify phone numbers include country codes
   - Check Twilio account balance
   - Ensure phone number is verified in trial mode

3. **Kubernetes Deployment Issues**

   - Check image registry and credentials
   - Verify secret values are base64 encoded correctly
   - Check resource quotas and limits

4. **Scheduling Not Working**
   - Verify timezone settings
   - Check container time vs host time
   - Review logs for schedule execution

### Debug Mode

Set environment variables for verbose logging:

```bash
export PYTHONUNBUFFERED=1
export LOG_LEVEL=DEBUG
```

## 🎯 Production Recommendations

### Security

- Use Kubernetes secrets or external secret management
- Enable Pod Security Standards
- Regular security scanning of container images
- Network policies for traffic restriction

### Reliability

- Set up proper monitoring and alerting
- Configure backup strategies for logs
- Implement circuit breakers for external APIs
- Add retry logic with exponential backoff

### Scaling

- Consider using cloud-managed services (SES, SNS)
- Implement proper rate limiting
- Use message queues for high-volume scenarios

## 💝 Romantic Touches

### Message Personalization

- Add pet names and inside jokes
- Include daily affirmations
- Add relevant emojis and symbols
- Reference shared memories or future plans

### Timing Optimization

- Send at her preferred wake-up time
- Add special messages on important dates
- Include weekend vs weekday variations

### Content Enhancement

- Add daily love quotes
- Include weather-based outfit suggestions
- Add motivational messages based on her schedule

## 📜 License

This project is open source. Use it to spread love and joy! 💕

## 🤝 Contributing

Feel free to submit issues and enhancement requests. Let's make this even more romantic and reliable!

---

_Made with ❤️ for sending daily love through the stars_ ✨
