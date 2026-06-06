# ♻️ EcoScan — QR-Based Plastic Waste Management Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A gamified plastic waste management system where users scan QR-tagged waste bags, earn reward points, and track their real-time environmental impact.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🌍 Overview

EcoScan is a full-stack Streamlit web application that incentivizes responsible plastic waste disposal through a QR-code-based reward system. Users scan QR codes attached to waste items, earn points based on waste type and weight, and monitor their cumulative environmental impact through an interactive analytics dashboard.

Designed with Indian urban environments in mind, EcoScan bridges the gap between citizen participation and waste collection infrastructure.

---

## ✨ Features

### 📱 QR Scanning
- **Live Camera Scanning** — Real-time QR detection via device camera
- **Image Upload** — Scan QR codes from uploaded images using OpenCV
- **Manual Entry** — Fallback text input for QR data
- **Sample QR Generator** — Built-in QR code generation for testing

### 🏆 Gamification & Rewards
- Point-based reward system with type-weighted multipliers
- Achievement badges (Eco Starter, Green Warrior, Planet Guardian, etc.)
- Progress tracker toward next reward tier
- Real-time leaderboard across registered users

### 📊 Analytics Dashboard
- Waste distribution pie chart by type
- Points earned over time (area chart)
- Weekly performance analysis (dual-axis bar chart)
- Environmental impact calculator (CO₂ saved, trees equivalent, energy saved)
- Detailed activity log with timestamps

### 🔐 User Management
- Secure registration and login with SHA-256 password hashing
- Per-user session state and waste history
- Personalized dashboard with daily/weekly stats

---

## 🎯 Demo

### Supported Waste Types & Point Multipliers

| Waste Type | Multiplier | Example (2kg) |
|---|---|---|
| 🔋 Batteries | 30 pts/kg | 60 pts |
| 📱 Electronics | 25 pts/kg | 50 pts |
| 🍶 Plastic Bottles | 15 pts/kg | 30 pts |
| 📦 Containers | 12 pts/kg | 24 pts |
| 🛍️ Plastic Bags | 10 pts/kg | 20 pts |
| 🥡 Food Packaging | 8 pts/kg | 16 pts |

### QR Code Format
```
WASTE:<type>:<weight_in_kg>

Example: WASTE:Plastic Bottles:2.5
```

### Demo Credentials
| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| User | `user1` | `password123` |

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ecoscan-waste-rewards.git
cd ecoscan-waste-rewards

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Dependencies

```txt
streamlit
pandas
opencv-python
numpy
plotly
qrcode[pil]
Pillow
streamlit-qrcode-scanner
```

---

## 🚀 Usage

### 1. Register / Login
Create an account or use the demo credentials to log in.

### 2. Scan Waste QR Codes
Navigate to the **QR Scanner** page and either:
- Allow camera access for live scanning
- Upload an image containing a QR code
- Use the Quick Scan buttons for demo testing
- Enter QR data manually

### 3. Earn Points
Points are instantly credited based on waste type and weight. Watch your balance update in real time.

### 4. Track Your Impact
Visit the **Statistics** page to see:
- Total waste collected and CO₂ prevented
- Point trends over time
- Weekly performance breakdown
- Your rank on the leaderboard

---

## 🏗️ Architecture

```
ecoscan-waste-rewards/
│
├── app.py                  # Main Streamlit application
│
├── Core Modules
│   ├── authenticate_user() # SHA-256 login & registration
│   ├── process_qr_waste()  # QR parsing & point calculation
│   ├── get_user_statistics()# Per-user stats aggregation
│   └── check_achievements()# Badge unlock logic
│
├── Pages
│   ├── login_page()        # Auth UI (login + register tabs)
│   ├── dashboard()         # User home with metrics & activity
│   ├── qr_scanner_page()   # Live + upload + manual QR scanning
│   └── statistics_page()   # Charts, impact, leaderboard
│
└── requirements.txt
```

### Data Flow

```
User scans QR  →  parse WASTE:type:weight
                        ↓
              Apply point multiplier
                        ↓
         Update session state (points + waste log)
                        ↓
         Reflect instantly on Dashboard & Statistics
```

---

## 🌱 Environmental Impact Metrics

EcoScan calculates real-world impact using standard conversion factors:

| Metric | Formula |
|---|---|
| CO₂ Prevented | `weight × 2.1 kg CO₂/kg plastic` |
| Trees Equivalent | `weight × 0.1 trees` |
| Energy Saved | `weight × 5.8 kWh/kg` |

---

## 📈 Roadmap

- [ ] Backend database (PostgreSQL / Firebase) for persistent storage
- [ ] REST API for mobile app integration
- [ ] Admin panel for waste collection centers
- [ ] GPS-tagged scan locations with map view
- [ ] Rewards marketplace (redeem points for coupons)
- [ ] Multi-language UI (Hindi, Tamil, Telugu, Bengali)
- [ ] IoT integration with smart waste bins

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/ecoscan-waste-rewards.git

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git commit -m "Add: your feature description"

# Push and open a Pull Request
git push origin feature/your-feature-name
```

Please follow PEP 8 for Python code and include docstrings for new functions.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) — rapid web app framework for Python
- [OpenCV](https://opencv.org/) — QR code detection from images
- [Plotly](https://plotly.com/) — interactive data visualizations
- [qrcode](https://github.com/lincolnloop/python-qrcode) — QR code generation

---

<div align="center">
  <b>Built to make recycling rewarding — one scan at a time. 🌏</b>
</div>
