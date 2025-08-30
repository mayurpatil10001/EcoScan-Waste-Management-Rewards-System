import streamlit as st
import pandas as pd
import hashlib
import cv2
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import time
import qrcode
from PIL import Image
import io
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="EcoScan - Plastic Waste Management",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: slideIn 0.8s ease-out;
    }
    
    .eco-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(17, 153, 142, 0.3);
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(252, 182, 159, 0.3);
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .points-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #2d3436;
        text-align: center;
        box-shadow: 0 15px 35px rgba(255, 234, 167, 0.4);
        margin-bottom: 2rem;
    }
    
    .scan-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(116, 185, 255, 0.4);
        margin-bottom: 2rem;
    }
    
    .success-card {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 184, 148, 0.3);
        margin: 1rem 0;
        animation: bounceIn 0.6s ease-out;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 0.75rem !important;
        transition: border-color 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Login Form Styling */
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Camera container */
    .camera-container {
        background: linear-gradient(135deg, #667eea22 0%, #764ba244 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed #667eea;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* QR Code display */
    .qr-display {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users_data' not in st.session_state:
    st.session_state.users_data = {}
if 'waste_records' not in st.session_state:
    st.session_state.waste_records = []
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'scan_success' not in st.session_state:
    st.session_state.scan_success = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Sample data for demonstration
def initialize_sample_data():
    if not st.session_state.users_data:
        st.session_state.users_data = {
            'admin': {
                'password': hashlib.sha256('admin123'.encode()).hexdigest(),
                'points': 250,
                'total_waste': 15.5,
                'registration_date': '2024-01-15'
            },
            'user1': {
                'password': hashlib.sha256('password123'.encode()).hexdigest(),
                'points': 180,
                'total_waste': 12.3,
                'registration_date': '2024-02-20'
            }
        }
    
    if not st.session_state.waste_records:
        st.session_state.waste_records = [
            {'user': 'admin', 'date': '2024-08-25', 'waste_type': 'Plastic Bottles', 'weight': 2.5, 'points': 37},
            {'user': 'admin', 'date': '2024-08-26', 'waste_type': 'Plastic Bags', 'weight': 1.2, 'points': 12},
            {'user': 'user1', 'date': '2024-08-24', 'waste_type': 'Containers', 'weight': 3.1, 'points': 37},
        ]

# Generate QR code for testing
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

# Authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    if username in st.session_state.users_data:
        stored_password = st.session_state.users_data[username]['password']
        if stored_password == hash_password(password):
            return True
    return False

def register_user(username, password):
    if username not in st.session_state.users_data:
        st.session_state.users_data[username] = {
            'password': hash_password(password),
            'points': 0,
            'total_waste': 0.0,
            'registration_date': datetime.now().strftime('%Y-%m-%d')
        }
        return True
    return False

# Enhanced waste processing
def process_qr_waste(qr_data, user):
    try:
        # Parse QR data (expected format: "WASTE:type:weight")
        if qr_data.startswith("WASTE:"):
            parts = qr_data.split(":")
            if len(parts) >= 3:
                waste_type = parts[1]
                weight = float(parts[2])
                
                # Enhanced point calculation based on waste type
                point_multipliers = {
                    'Plastic Bottles': 15,
                    'Plastic Bags': 10,
                    'Containers': 12,
                    'Food Packaging': 8,
                    'Electronics': 25,
                    'Batteries': 30
                }
                
                multiplier = point_multipliers.get(waste_type, 10)
                points = int(weight * multiplier)
                
                # Add record
                record = {
                    'user': user,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'waste_type': waste_type,
                    'weight': weight,
                    'points': points
                }
                st.session_state.waste_records.append(record)
                
                # Update user points and total waste
                st.session_state.users_data[user]['points'] += points
                st.session_state.users_data[user]['total_waste'] += weight
                
                return True, f"Success! Processed {weight}kg of {waste_type}. Earned {points} points!"
            else:
                return False, "Invalid QR code format. Expected: WASTE:type:weight"
        else:
            return False, "QR code does not contain waste data"
    except ValueError:
        return False, "Invalid weight value in QR code"
    except Exception as e:
        return False, f"Error processing QR code: {str(e)}"

# Statistics functions
def get_user_statistics(user):
    user_records = [r for r in st.session_state.waste_records if r['user'] == user]
    
    if not user_records:
        return {
            'total_scans': 0,
            'total_weight': 0,
            'total_points': 0,
            'recent_activity': []
        }
    
    df = pd.DataFrame(user_records)
    
    return {
        'total_scans': len(user_records),
        'total_weight': df['weight'].sum(),
        'total_points': df['points'].sum(),
        'recent_activity': user_records[-5:]
    }

def refresh_stats():
    st.session_state.last_refresh = datetime.now()
    time.sleep(0.5)
    st.success("Statistics refreshed successfully!")

# Enhanced Login Page
def login_page():
    # Animated header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 3rem; font-weight: 700;">🌍 EcoScan</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Smart Plastic Waste Management System</p>
        <p style="margin: 0.2rem 0 0 0; opacity: 0.8;">Scan • Earn • Save the Planet</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Register tabs with enhanced styling
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-container">
                <h3 style="text-align: center; margin-bottom: 2rem;">Welcome Back! 👋</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success("🎉 Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
    
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-container">
                <h3 style="text-align: center; margin-bottom: 2rem;">Join EcoScan! 🌱</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("register_form"):
                new_username = st.text_input("👤 Choose Username", placeholder="Create a username")
                new_password = st.text_input("🔒 Choose Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    register = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if register:
                    if new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif register_user(new_username, new_password):
                        st.success("🎉 Registration successful! Please login.")
                    else:
                        st.error("❌ Username already exists")
    
    # Demo credentials
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea22 0%, #764ba244 100%); 
                padding: 1.5rem; border-radius: 15px; margin-top: 2rem; text-align: center;
                border: 1px solid rgba(102, 126, 234, 0.3);">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🔑 Demo Credentials</h4>
        <div style="display: flex; justify-content: space-around;">
            <div>
                <p><strong>👨‍💼 Admin Account</strong></p>
                <p>Username: <code>admin</code></p>
                <p>Password: <code>admin123</code></p>
            </div>
            <div>
                <p><strong>👤 User Account</strong></p>
                <p>Username: <code>user1</code></p>
                <p>Password: <code>password123</code></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Dashboard
def dashboard():
    user = st.session_state.current_user
    user_data = st.session_state.users_data[user]
    
    # Animated welcome header
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 style="margin:0; font-size: 2.5rem;">Welcome back, {user}! 🌟</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Ready to make a difference today?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced points display
    st.markdown(f"""
    <div class="points-card pulse-animation">
        <h2 style="margin: 0; font-size: 3rem; font-weight: 700;">🏆 {user_data['points']}</h2>
        <h3 style="margin: 0.5rem 0; font-size: 1.3rem;">EcoScan Points</h3>
        <p style="margin: 0; opacity: 0.8;">Keep scanning to earn more!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    user_stats = get_user_statistics(user)
    today_scans = len([r for r in st.session_state.waste_records 
                      if r['user'] == user and r['date'] == datetime.now().strftime('%Y-%m-%d')])
    
    metrics_data = [
        ("📊 Total Scans", user_stats['total_scans'], "lifetime", "#667eea"),
        ("⚖️ Weight Collected", f"{user_data['total_waste']:.1f}", "kg", "#00b894"),
        ("🎯 Today's Scans", today_scans, "today", "#fdcb6e"),
        ("🌍 Impact Level", "Excellent" if user_data['points'] > 200 else "Great" if user_data['points'] > 100 else "Good", "rating", "#e17055")
    ]
    
    for col, (title, value, unit, color) in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}22 0%, {color}44 100%); 
                        border-left: 4px solid {color}; padding: 1.5rem; border-radius: 15px; 
                        text-align: center; margin-bottom: 1rem; transition: transform 0.3s ease;"
                 onmouseover="this.style.transform='translateY(-3px)'"
                 onmouseout="this.style.transform='translateY(0)'">
                <h4 style="margin: 0; color: #333; font-size: 0.9rem;">{title}</h4>
                <h2 style="margin: 0.5rem 0; color: {color}; font-size: 2rem; font-weight: 700;">{value}</h2>
                <p style="margin: 0; color: #666; font-weight: 500; font-size: 0.8rem;">{unit}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent activity and progress
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Recent Activity")
        user_records = [r for r in st.session_state.waste_records if r['user'] == user]
        
        if user_records:
            recent_df = pd.DataFrame(user_records[-5:])
            
            # Enhanced activity cards
            for _, row in recent_df.iterrows():
                emoji_map = {
                    'Plastic Bottles': '🍶',
                    'Plastic Bags': '🛍️', 
                    'Containers': '📦',
                    'Food Packaging': '🥡',
                    'Electronics': '📱',
                    'Batteries': '🔋'
                }
                emoji = emoji_map.get(row['waste_type'], '♻️')
                
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                           box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #667eea;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 1.5rem; margin-right: 1rem;">{emoji}</span>
                            <div>
                                <strong>{row['waste_type']}</strong><br>
                                <small style="color: #666;">{row['date']}</small>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #00b894; font-weight: 600;">+{row['points']} pts</div>
                            <div style="color: #666; font-size: 0.9rem;">{row['weight']}kg</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                        padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                <h3>🎯 Ready to Start?</h3>
                <p>No scanning activity yet. Use the QR Scanner to earn your first points!</p>
                <p style="opacity: 0.8;">💡 Each scan helps reduce plastic waste</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Progress Tracker")
        
        # Enhanced progress display
        next_level = ((user_data['points'] // 100) + 1) * 100
        progress = (user_data['points'] % 100) / 100
        
        st.progress(progress)
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <h4 style="color: #667eea; margin: 0;">{user_data['points']}/{next_level} points</h4>
            <p style="color: #666; margin: 0.5rem 0;">🏅 {100 - (user_data['points'] % 100)} points to next reward!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Achievement badges
        st.markdown("### 🏆 Achievements")
        achievements = check_achievements(user)
        
        if achievements:
            for achievement in achievements:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                           padding: 0.5rem; border-radius: 10px; margin: 0.3rem 0; text-align: center;
                           color: #2d3436; font-weight: 600;">
                    {achievement}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎯 Scan waste to unlock achievements!")
        
        # Quick action button - FIXED: Remove st.switch_page
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Quick Scan", use_container_width=True):
            st.session_state.current_page = "QR Scanner"
            st.rerun()

# Simple QR Scanner Page (Windows compatible)
def qr_scanner_page():
    st.markdown("""
    <div class="scan-card">
        <h1 style="margin:0; font-size: 2.5rem;">📱 QR Code Scanner</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Scan waste QR codes to earn instant points!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current points prominently
    user_data = st.session_state.users_data[st.session_state.current_user]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;">
            <h3 style="margin: 0; font-size: 2rem;">🏆 Current Points: {user_data['points']}</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Ready to earn more?</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced instructions
    with st.expander("📖 How to Use QR Scanner", expanded=True):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                   padding: 1.5rem; border-radius: 15px; color: #2d3436;">
            <h4 style="margin-top: 0;">🎯 Step-by-Step Guide:</h4>
            <ol style="margin-bottom: 0;">
                <li><strong>📸 Use Built-in Camera:</strong> Upload image or use sample QR codes</li>
                <li><strong>🔍 QR Detection:</strong> System automatically processes valid waste QR codes</li>
                <li><strong>💎 Earn Points:</strong> Points instantly added based on waste type and weight</li>
                <li><strong>📊 Track Progress:</strong> View updated stats in real-time</li>
            </ol>
            <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 10px;">
                <strong>💡 QR Format:</strong> <code>WASTE:type:weight</code><br>
                <strong>Example:</strong> <code>WASTE:Plastic Bottles:2.5</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Camera upload option
    st.markdown("### 📸 Upload QR Code Image")
    uploaded_file = st.file_uploader("Choose an image with QR code", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        try:
            # Process uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded QR Code", width=300)
            
            # Convert to OpenCV format
            open_cv_image = np.array(image)
            if len(open_cv_image.shape) == 3:
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            
            # For demo purposes, we'll use manual detection
            # In production, you'd use a proper QR detection library
            st.info("🔍 For this demo, please manually enter the QR code data below")
            
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    # Quick scan buttons with sample QR codes
    st.markdown("### 🧪 Quick Scan Options")
    st.markdown("Click any button below to simulate scanning that type of waste:")
    
    col1, col2, col3 = st.columns(3)
    
    sample_qrs = [
        ("🍶 Plastic Bottles\n(2.5kg = 37 pts)", "WASTE:Plastic Bottles:2.5", "#74b9ff"),
        ("🛍️ Plastic Bags\n(1.2kg = 12 pts)", "WASTE:Plastic Bags:1.2", "#00b894"),
        ("📦 Containers\n(3.0kg = 36 pts)", "WASTE:Containers:3.0", "#fdcb6e")
    ]
    
    for col, (label, qr_code, color) in zip([col1, col2, col3], sample_qrs):
        with col:
            if st.button(label, key=f"quick_scan_{qr_code}", use_container_width=True):
                success, message = process_qr_waste(qr_code, st.session_state.current_user)
                if success:
                    st.markdown(f"""
                    <div class="success-card">
                        <h3 style="margin: 0;">🎉 Scan Successful!</h3>
                        <p style="margin: 0.5rem 0 0 0;">{message}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                    # Show updated points with animation
                    updated_points = st.session_state.users_data[st.session_state.current_user]['points']
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                               padding: 1rem; border-radius: 15px; color: white; text-align: center; 
                               margin-top: 1rem; animation: bounceIn 0.6s ease-out;">
                        <h3 style="margin: 0;">💰 New Balance: {updated_points} Points! 🚀</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
    
    # More sample options
    col1, col2, col3 = st.columns(3)
    
    more_samples = [
        ("🥡 Food Packaging\n(1.5kg = 12 pts)", "WASTE:Food Packaging:1.5", "#e17055"),
        ("📱 Electronics\n(0.8kg = 20 pts)", "WASTE:Electronics:0.8", "#a29bfe"),
        ("🔋 Batteries\n(0.5kg = 15 pts)", "WASTE:Batteries:0.5", "#fd79a8")
    ]
    
    for col, (label, qr_code, color) in zip([col1, col2, col3], more_samples):
        with col:
            if st.button(label, key=f"quick_scan_2_{qr_code}", use_container_width=True):
                success, message = process_qr_waste(qr_code, st.session_state.current_user)
                if success:
                    st.success(message)
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
    
    # Manual QR input with enhanced styling
    st.markdown("### ✏️ Manual QR Code Entry")
    
    with st.form("manual_qr_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            qr_input = st.text_input(
                "Enter QR Code Data", 
                placeholder="WASTE:Plastic Bottles:2.5",
                help="Format: WASTE:type:weight"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_qr = st.form_submit_button("🔍 Process", use_container_width=True)
        
        if submit_qr and qr_input:
            success, message = process_qr_waste(qr_input, st.session_state.current_user)
            if success:
                st.markdown(f"""
                <div class="success-card">
                    <h3 style="margin: 0;">🎊 QR Processed Successfully!</h3>
                    <p style="margin: 0.5rem 0 0 0;">{message}</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error(message)
    
    # Generate and display sample QR codes
    st.markdown("### 🖼️ Sample QR Codes")
    st.markdown("Scan these with any QR reader app to test:")
    
    qr_col1, qr_col2, qr_col3 = st.columns(3)
    
    sample_qr_data = [
        ("Plastic Bottles", "WASTE:Plastic Bottles:2.5"),
        ("Electronics", "WASTE:Electronics:1.0"),
        ("Batteries", "WASTE:Batteries:0.3")
    ]
    
    for col, (name, data) in zip([qr_col1, qr_col2, qr_col3], sample_qr_data):
        with col:
            qr_img = generate_qr_code(data)
            st.markdown(f"""
            <div class="qr-display">
                <h5 style="text-align: center; margin-bottom: 1rem; color: #333;">{name}</h5>
                <img src="data:image/png;base64,{qr_img}" style="width: 100%; max-width: 200px;">
                <p style="text-align: center; margin-top: 0.5rem; font-size: 0.8rem; color: #666;">{data}</p>
            </div>
            """, unsafe_allow_html=True)

# Enhanced Statistics Page
def statistics_page():
    st.markdown("""
    <div class="eco-header">
        <h1 style="margin:0; font-size: 2.5rem;">📈 Statistics Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Track your environmental impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.current_user
    
    # Enhanced refresh section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔄 Refresh Stats", use_container_width=True):
            with st.spinner("🔄 Refreshing data..."):
                refresh_stats()
                time.sleep(1)
                st.rerun()
    
    with col3:
        if 'last_refresh' in st.session_state:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 0.5rem; border-radius: 10px; 
                       text-align: center; border: 1px solid #e0e0e0;">
                <small>🕒 Last refreshed: {st.session_state.last_refresh.strftime('%H:%M:%S')}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Filter records for current user
    user_records = [r for r in st.session_state.waste_records if r['user'] == user]
    
    if not user_records:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                   padding: 3rem; border-radius: 20px; color: white; text-align: center; margin: 2rem 0;">
            <h2 style="margin-bottom: 1rem;">🎯 Start Your Eco Journey!</h2>
            <p style="font-size: 1.1rem; margin-bottom: 1rem;">No data available yet. Scan your first QR code to see amazing statistics!</p>
            <p style="opacity: 0.9;">🌱 Every scan counts towards a greener planet</p>
            <div style="margin-top: 2rem;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Use the QR Scanner to get started →</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    df = pd.DataFrame(user_records)
    df['date'] = pd.to_datetime(df['date'])
    
    # Enhanced statistics overview
    stats = get_user_statistics(user)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats_cards = [
        ("📊 Total Scans", stats['total_scans'], "lifetime", "#667eea"),
        ("⚖️ Weight Collected", f"{stats['total_weight']:.1f}", "kg", "#00b894"),
        ("🏆 Points Earned", stats['total_points'], "total", "#fdcb6e"),
        ("🌍 CO2 Saved", f"{stats['total_weight'] * 2.1:.1f}", "kg", "#e17055")
    ]
    
    for col, (title, value, unit, color) in zip([col1, col2, col3, col4], stats_cards):
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}22 0%, {color}44 100%); 
                        border-left: 4px solid {color}; padding: 1.5rem; border-radius: 15px; 
                        text-align: center; margin-bottom: 1rem; transition: transform 0.3s ease;">
                <h4 style="margin: 0; color: #333; font-size: 0.9rem;">{title}</h4>
                <h2 style="margin: 0.5rem 0; color: {color}; font-size: 2.2rem; font-weight: 700;">{value}</h2>
                <p style="margin: 0; color: #666; font-weight: 500; font-size: 0.8rem;">{unit}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Waste Distribution")
        waste_by_type = df.groupby('waste_type')['weight'].sum().reset_index()
        
        fig_pie = px.pie(
            waste_by_type, 
            values='weight', 
            names='waste_type',
            title="Distribution of Waste Types",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Weight: %{value:.1f}kg<br>Percentage: %{percent}<extra></extra>"
        )
        fig_pie.update_layout(
            font=dict(size=14, family="Poppins"),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Points Trend")
        daily_points = df.groupby('date')['points'].sum().reset_index()
        
        fig_line = px.area(
            daily_points, 
            x='date', 
            y='points',
            title="Points Earned Over Time",
            line_shape="spline"
        )
        fig_line.update_traces(
            line=dict(color='#667eea', width=3),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.3)',
            hovertemplate="<b>Date:</b> %{x}<br><b>Points:</b> %{y}<extra></extra>"
        )
        fig_line.update_layout(
            font=dict(size=14, family="Poppins"),
            height=400,
            xaxis_title="Date",
            yaxis_title="Points Earned"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Environmental impact section
    st.markdown("### 🌍 Environmental Impact Calculator")
    
    total_weight = df['weight'].sum()
    co2_saved = total_weight * 2.1
    trees_equivalent = total_weight * 0.1
    energy_saved = total_weight * 5.8  # kWh saved per kg
    
    impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
    
    impact_metrics = [
        ("🌱 CO2 Prevented", f"{co2_saved:.1f}", "kg CO2", "#00b894"),
        ("🌳 Trees Saved", f"{trees_equivalent:.1f}", "equivalent", "#00a085"),
        ("⚡ Energy Saved", f"{energy_saved:.1f}", "kWh", "#fdcb6e"),
        ("🏭 Waste Diverted", f"{total_weight:.1f}", "kg plastic", "#667eea")
    ]
    
    for col, (title, value, unit, color) in zip([impact_col1, impact_col2, impact_col3, impact_col4], impact_metrics):
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}22 0%, {color}44 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center; 
                        border: 2px solid {color}33; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: {color}; font-size: 0.9rem;">{title}</h4>
                <h2 style="margin: 0.5rem 0; color: {color}; font-size: 2rem; font-weight: 700;">{value}</h2>
                <p style="margin: 0; color: #666; font-size: 0.8rem;">{unit}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Weekly performance chart
    st.markdown("### 📅 Weekly Performance Analysis")
    
    if len(df) > 0:
        df['week'] = df['date'].dt.isocalendar().week
        weekly_stats = df.groupby('week').agg({
            'weight': 'sum',
            'points': 'sum',
            'waste_type': 'count'
        }).rename(columns={'waste_type': 'scans'}).reset_index()
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Weight (kg)', 
            x=weekly_stats['week'], 
            y=weekly_stats['weight'],
            marker_color='rgba(102, 126, 234, 0.8)',
            hovertemplate="<b>Week %{x}</b><br>Weight: %{y:.1f}kg<extra></extra>",
            text=weekly_stats['weight'].round(1),
            textposition='auto'
        ))
        fig_bar.add_trace(go.Bar(
            name='Points', 
            x=weekly_stats['week'], 
            y=weekly_stats['points'], 
            yaxis='y2',
            marker_color='rgba(118, 75, 162, 0.8)',
            hovertemplate="<b>Week %{x}</b><br>Points: %{y}<extra></extra>",
            text=weekly_stats['points'],
            textposition='auto'
        ))
        
        fig_bar.update_layout(
            title='Weekly Waste Collection & Points Progress',
            xaxis=dict(title='Week Number'),
            yaxis=dict(title='Weight (kg)', side='left', color='#667eea'),
            yaxis2=dict(title='Points Earned', side='right', overlaying='y', color='#764ba2'),
            barmode='group',
            height=500,
            font=dict(size=14, family="Poppins"),
            hovermode='x unified'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Recent detailed activity
    st.markdown("### 📋 Recent Activity Log")
    
    if len(user_records) > 0:
        recent_df = pd.DataFrame(user_records).tail(10).sort_values('date', ascending=False)
        
        # Display as beautiful activity cards
        for i, row in enumerate(recent_df.itertuples(), 1):
            emoji_map = {
                'Plastic Bottles': '🍶',
                'Plastic Bags': '🛍️', 
                'Containers': '📦',
                'Food Packaging': '🥡',
                'Electronics': '📱',
                'Batteries': '🔋'
            }
            emoji = emoji_map.get(row.waste_type, '♻️')
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%); 
                       padding: 1.2rem; border-radius: 15px; margin: 0.8rem 0; 
                       box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                       border-left: 4px solid #667eea;
                       transition: transform 0.3s ease;"
                 onmouseover="this.style.transform='translateX(5px)'"
                 onmouseout="this.style.transform='translateX(0)'">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{emoji}</span>
                        <div>
                            <h4 style="margin: 0; color: #333;">{row.waste_type}</h4>
                            <p style="margin: 0; color: #666; font-size: 0.9rem;">📅 {row.date} • ⏰ {getattr(row, 'time', '00:00:00')}</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: #00b894; color: white; padding: 0.3rem 0.8rem; 
                                   border-radius: 20px; font-weight: 600; margin-bottom: 0.3rem;">
                            +{row.points} pts
                        </div>
                        <div style="color: #666; font-size: 0.9rem;">⚖️ {row.weight}kg</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Leaderboard section (if multiple users)
    if len(st.session_state.users_data) > 1:
        st.markdown("### 🏆 Leaderboard")
        
        leaderboard_data = []
        for username, user_info in st.session_state.users_data.items():
            leaderboard_data.append({
                'username': username,
                'points': user_info['points'],
                'total_waste': user_info['total_waste']
            })
        
        leaderboard_df = pd.DataFrame(leaderboard_data).sort_values('points', ascending=False)
        
        for i, row in enumerate(leaderboard_df.itertuples(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            highlight = "background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);" if row.username == user else "background: #f8f9fa;"
            
            st.markdown(f"""
            <div style="{highlight} padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                       border: 2px solid {'#fdcb6e' if row.username == user else '#e0e0e0'};">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 1.5rem; margin-right: 1rem;">{medal}</span>
                        <div>
                            <h4 style="margin: 0; color: #333;">{row.username}</h4>
                            <p style="margin: 0; color: #666; font-size: 0.9rem;">⚖️ {row.total_waste:.1f}kg total</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="margin: 0; color: #667eea;">{row.points} pts</h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Achievement system
def check_achievements(user):
    user_data = st.session_state.users_data[user]
    user_records = [r for r in st.session_state.waste_records if r['user'] == user]
    
    achievements = []
    
    if user_data['points'] >= 50:
        achievements.append("🥉 Eco Starter")
    if user_data['points'] >= 100:
        achievements.append("🥈 Green Warrior")
    if user_data['points'] >= 250:
        achievements.append("🥇 Planet Guardian")
    if user_data['total_waste'] >= 10:
        achievements.append("🌍 Earth Protector")
    if len(user_records) >= 10:
        achievements.append("🔥 Scan Master")
    if len(user_records) >= 5:
        achievements.append("⭐ Rising Star")
    
    return achievements

# Enhanced Navigation
def sidebar_navigation():
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: white;">
        <h2 style="margin: 0;">♻️ EcoScan</h2>
        <p style="margin: 0.5rem 0; opacity: 0.9;">Waste Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        user_data = st.session_state.users_data[st.session_state.current_user]
        
        # Enhanced user info in sidebar
        st.sidebar.markdown(f"""
        <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; 
                   margin-bottom: 1.5rem; color: white; text-align: center;
                   backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
            <h3 style="margin: 0; font-size: 1.3rem;">👤 {st.session_state.current_user}</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">🏆 {user_data['points']} Points</p>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">⚖️ {user_data['total_waste']:.1f}kg collected</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu with icons
        st.sidebar.markdown("### 🗺️ Navigation")
        
        if st.sidebar.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        
        if st.sidebar.button("📱 QR Scanner", use_container_width=True):
            st.session_state.current_page = "QR Scanner"
            st.rerun()
        
        if st.sidebar.button("📊 Statistics", use_container_width=True):
            st.session_state.current_page = "Statistics"
            st.rerun()
        
        # Quick stats in sidebar
        st.sidebar.markdown("### 📈 Quick Stats")
        today_scans = len([r for r in st.session_state.waste_records 
                          if r['user'] == st.session_state.current_user 
                          and r['date'] == datetime.now().strftime('%Y-%m-%d')])
        
        st.sidebar.metric("🎯 Today's Scans", today_scans)
        st.sidebar.metric("🌱 This Week", len([r for r in st.session_state.waste_records 
                                            if r['user'] == st.session_state.current_user]))
        
        # Achievements in sidebar
        achievements = check_achievements(st.session_state.current_user)
        if achievements:
            st.sidebar.markdown("### 🏆 Latest Achievement")
            st.sidebar.markdown(f"""
            <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 10px; 
                       text-align: center; color: white;">
                {achievements[-1]}
            </div>
            """, unsafe_allow_html=True)
        
        # Logout button
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.current_page = 'Dashboard'
            st.rerun()
        
        # Return current page
        return st.session_state.get('current_page', 'Dashboard')
    else:
        return "Login"

# Enhanced sample QR codes display
def show_sample_qr_codes():
    if st.session_state.logged_in:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🧪 Sample QR Codes")
        st.sidebar.markdown("*Copy these codes for testing:*")
        
        sample_codes = [
            ("🍶 Bottles", "WASTE:Plastic Bottles:2.5"),
            ("🛍️ Bags", "WASTE:Plastic Bags:1.2"),
            ("📦 Containers", "WASTE:Containers:3.1"),
            ("🥡 Packaging", "WASTE:Food Packaging:0.8"),
            ("📱 Electronics", "WASTE:Electronics:1.5"),
            ("🔋 Batteries", "WASTE:Batteries:0.3")
        ]
        
        for emoji_type, code in sample_codes:
            with st.sidebar.expander(emoji_type):
                st.code(code, language="text")

# Main application
def main():
    initialize_sample_data()
    
    # Route to appropriate page
    page = sidebar_navigation()
    
    if page == "Login":
        login_page()
    elif page == "Dashboard":
        dashboard()
    elif page == "QR Scanner":
        qr_scanner_page()
    elif page == "Statistics":
        statistics_page()

if __name__ == "__main__":
    show_sample_qr_codes()
    main()