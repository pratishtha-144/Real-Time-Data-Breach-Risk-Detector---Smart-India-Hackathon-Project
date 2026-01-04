# 🛡️ Real-Time Data Breach Risk Detector

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![License](https://img.shields.io/badge/license-MIT-green)

**A hackathon-ready cybersecurity project for Smart India Hackathon**

*Detect potential data breach risks using rule-based analysis and real-time monitoring*

</div>

---

## 📋 Problem Statement

Organizations face increasing security threats from data breaches. Many breaches occur due to:
- **Misconfigurations** (exposed APIs, default credentials)
- **Failed authentication attempts** (brute force attacks)
- **Suspicious access patterns** (unusual login times, multiple IPs)

This project provides a **beginner-friendly, real-time risk detection system** that analyzes logs and identifies potential vulnerabilities before they become breaches.

---

## ✨ Features

### 🔍 **Security Detectors**
- **Authentication Detector**: Identifies brute force attempts and suspicious login patterns
- **API Security Detector**: Finds missing authentication on sensitive endpoints
- **Misconfiguration Detector**: Detects default credentials and public endpoint exposures

### 📊 **Risk Scoring Engine**
- Calculates numerical risk scores (0-100+)
- Categorizes risk levels: LOW, MEDIUM, HIGH, CRITICAL
- Provides weighted scoring based on issue severity

### 🚨 **Real-Time Alerts**
- Color-coded severity levels (Critical, Warning, Info)
- Timestamp tracking for all alerts
- Detailed issue descriptions

### 📈 **Interactive Dashboard**
- Modern, glassmorphism design with smooth animations
- Real-time risk level visualization
- Comprehensive security recommendations
- Responsive layout for all devices

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ with FastAPI |
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Data Storage** | JSON file-based database |
| **API Documentation** | Swagger/OpenAPI (auto-generated) |
| **Server** | Uvicorn ASGI server |

---

## 📁 Project Structure

```
data-breach-detector/
├── backend/
│   ├── app.py                      # Main FastAPI application
│   ├── config/
│   │   └── settings.py             # Configuration and thresholds
│   ├── collectors/
│   │   ├── log_collector.py        # Reads authentication & API logs
│   │   └── api_collector.py        # Simulates API endpoint scanning
│   ├── detectors/
│   │   ├── auth_detector.py        # Detects brute force & suspicious logins
│   │   ├── api_detector.py         # Detects API security issues
│   │   └── misconfig_detector.py   # Detects misconfigurations
│   ├── risk_engine/
│   │   └── risk_score.py           # Calculates risk scores
│   ├── alerts/
│   │   └── alert_manager.py        # Manages security alerts
│   ├── routes/
│   │   └── dashboard_routes.py     # REST API endpoints
│   └── database/
│       └── db.py                   # JSON file database helpers
├── frontend/
│   ├── dashboard.html              # Main dashboard UI
│   ├── css/
│   │   └── style.css               # Modern styling with gradients
│   └── js/
│       └── dashboard.js            # API integration & UI updates
├── sample_logs/
│   ├── auth_logs.json              # Sample authentication logs
│   └── api_logs.json               # Sample API request logs
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🚀 How to Run

### **Step 1: Prerequisites**
Make sure you have Python 3.8 or higher installed:
```bash
python3 --version
```

### **Step 2: Install Dependencies**
```bash
cd data-breach-detector
pip install -r requirements.txt
```

### **Step 3: Start the Backend Server**
```bash
cd backend
python app.py
```

You should see:
```
🚀 Data Breach Risk Detector - Backend Started
📡 Server running on: http://127.0.0.1:8000
📚 API Documentation: http://127.0.0.1:8000/docs
```

### **Step 4: Open the Dashboard**
Open `frontend/dashboard.html` in your web browser (Chrome/Firefox recommended)

### **Step 5: Run a Security Scan**
Click the **"Run Security Scan"** button and watch the system analyze your sample data!

---

## 🎯 Demo Scenario for Judges

### **Scenario: Detecting a Security Incident**

**Step 1: Initial State**
- Dashboard shows "No scans yet"
- Risk level: UNKNOWN

**Step 2: Run Security Scan**
- Click "Run Security Scan" button
- System analyzes sample logs in real-time

**Step 3: Issues Detected**
The system detects:
1. ⚠️ **Brute Force Attack**: User 'admin' had 4 failed login attempts
2. 🚨 **Exposed Endpoints**: `/api/admin/settings` and `/api/database/dump` publicly accessible
3. ⚠️ **Suspicious Access**: Login at 3:15 AM (suspicious hour)
4. ℹ️ **Default Credentials**: Username 'admin' is a common default

**Step 4: Risk Calculation**
- Risk Score: **115** (automatically calculated)
- Risk Level: **HIGH** (color-coded red/orange)

**Step 5: Recommendations**
System provides actionable recommendations:
- 🔒 Implement account lockout after failed attempts
- 🔒 Add authentication to sensitive API endpoints
- 🔒 Set up alerts for off-hours access
- 🔒 Change default usernames and passwords

---

## 🔬 How It Works

### **1. Data Collection**
```python
# Collects authentication and API logs from JSON files
log_collector.collect_auth_logs()
log_collector.collect_api_logs()
```

### **2. Rule-Based Detection**
```python
# Example: Brute Force Detection
if failed_login_count > MAX_THRESHOLD:
    flag_as_brute_force_attack()
```

### **3. Risk Scoring**
```python
# Each issue type has a weight
score = Σ(issue_weight × issue_count)

# Risk levels based on score:
# 0-29: LOW
# 30-59: MEDIUM  
# 60-89: HIGH
# 90+: CRITICAL
```

### **4. Alert Generation**
```python
# Creates timestamped alerts with severity
alert = {
    "severity": "CRITICAL",
    "description": "Exposed endpoint detected",
    "timestamp": "2026-01-04T03:51:00"
}
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scan` | Run complete security scan |
| `GET` | `/api/risk` | Get current risk score |
| `GET` | `/api/alerts` | Get all security alerts |
| `GET` | `/api/status` | System health check |

**Example API Call:**
```bash
curl -X POST http://127.0.0.1:8000/api/scan
```

---

## 🎨 Dashboard Features

- **Glassmorphism UI**: Modern, translucent design with blur effects
- **Color-Coded Alerts**: Red (Critical), Orange (High), Yellow (Medium), Green (Low)
- **Smooth Animations**: Fade-ins, slide-ins, hover effects
- **Real-Time Updates**: Instant display of scan results
- **Responsive Design**: Works on desktop, tablet, and mobile

---

## ⚠️ Important Disclaimers

### **For Hackathon Judges:**
1. ✅ This is a **proof-of-concept** using rule-based detection
2. ✅ Uses **simulated sample data** (not real hacking)
3. ✅ Demonstrates **cybersecurity concepts** in a safe environment
4. ❌ Does **NOT** claim 100% security coverage
5. ❌ Does **NOT** perform actual penetration testing
6. ❌ Should **NOT** be deployed in production without hardening

### **Educational Purpose:**
This project is designed for:
- Learning cybersecurity fundamentals
- Understanding threat detection logic
- Demonstrating data analysis skills
- Building hackathon presentations

---

## 🔮 Future Scope

### **Phase 2 Enhancements**
- [ ] Machine Learning integration for anomaly detection
- [ ] Integration with real SIEM systems (Splunk, ELK Stack)
- [ ] Email/SMS notifications for critical alerts
- [ ] Historical trend analysis and reporting
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)

### **Advanced Features**
- [ ] Real-time log streaming
- [ ] Threat intelligence feed integration
- [ ] Automated incident response workflows
- [ ] Multi-tenant support for enterprises
- [ ] Advanced visualization with charts/graphs
- [ ] Export reports as PDF

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Author

**[Your Name]**  
*Smart India Hackathon 2026*  
*Cybersecurity Track*

---

## 🙏 Acknowledgments

- Sample log structures inspired by real-world security systems
- UI design influenced by modern security dashboards
- Built with ❤️ for the cybersecurity community

---

<div align="center">

### 🛡️ Stay Secure!

**If you found this project helpful, please ⭐ star the repository!**

</div>
