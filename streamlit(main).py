import re
import random
import string
import streamlit as st

page_bg_img = """
<style>
# body {
#     background-image: url("lock.jpg"); /* Replace with your image */
#     background-size: cover;
#     background-position: center;
#     background-attachment: fixed;
# }

.main {
    background-color: rgba(255, 255, 255, 0.8); /* White background */
    # padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Light shadow for contrast */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# List of common weak passwords
COMMON_PASSWORDS = {"password", "123456", "password123", "qwerty", "abc123", "letmein", "admin", "welcome", "12345678"}

# Function to generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Function to check password strength with weighted scoring
def check_password_strength(password):
    score = 0
    reasons = []

    # Length Check (Weight: 2)
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        reasons.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check (Weight: 1)
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        reasons.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check (Weight: 1)
    if re.search(r"\d", password):
        score += 1
    else:
        reasons.append("❌ Add at least one number (0-9).")

    # Special Character Check (Weight: 2)
    if re.search(r"[!@#$%^&*]", password):
        score += 2
    else:
        reasons.append("❌ Include at least one special character (!@#$%^&*).")

    # Common Password Check (Automatic Rejection)
    if password.lower() in COMMON_PASSWORDS:
        return 0, ["❌ This password is too common and insecure."]

    return score, reasons

# Streamlit UI
st.markdown('<div class="main">', unsafe_allow_html=True)  # Start container

# st.image("password_image.png", use_column_width=True)  # Add logo or header image if needed
st.title("🔒 Password Strength Checker")

# User Input
password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = check_password_strength(password)
    
    # Provide feedback
    if score >= 5:
        st.success("✅ Strong Password!")
    elif score >= 3:
        st.warning("⚠ Moderate Password - Consider making it stronger.")
    else:
        st.error("❌ Weak Password - Improve it using the suggestions below.")
    
    # Show detailed feedback
    for msg in feedback:
        st.write(msg)

    # Suggest a strong password
    if score < 5:
        st.info(f"🔑 Suggested Strong Password: {generate_password()}")

st.markdown('</div>', unsafe_allow_html=True)  