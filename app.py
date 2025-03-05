import streamlit as st
import re
import random
import string
import pyperclip

def evaluate_password_strength(password):
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    # Check uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter")

    # Check lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter")

    # Check digits
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Include at least one digit")

    # Check special characters
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*)")

    # Check common patterns
    common_patterns = ['password', '123', 'qwerty', 'admin', 'letmein']
    if any(pattern in password.lower() for pattern in common_patterns):
        feedback.append("Avoid common words or sequences")

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, feedback

def generate_strong_password():
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = '!@#$%^&*'
    
    # Ensure at least one of each type
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill remaining characters
    all_chars = uppercase + lowercase + digits + special
    password += [random.choice(all_chars) for _ in range(10)]
    
    # Shuffle and convert to string
    random.shuffle(password)
    return ''.join(password)

# Streamlit UI
st.title("🔒 Password Strength Meter")
st.write("Check your password security and generate strong passwords")

# Password input
password = st.text_input("Enter your password:", type="password")

# Initialize session state for generated password
if 'generated_pw' not in st.session_state:
    st.session_state.generated_pw = ""

# Main logic
if password:
    strength, feedback = evaluate_password_strength(password)
    
    # Display strength with color
    col1, col2 = st.columns(2)
    with col1:
        if strength == "Strong":
            st.success(f"Strength: {strength} ✅")
        elif strength == "Moderate":
            st.warning(f"Strength: {strength} ⚠️")
        else:
            st.error(f"Strength: {strength} ❌")
    
    # Show feedback
    if strength != "Strong":
        with col2:
            st.subheader("Improvement Suggestions:")
            for item in feedback:
                st.write(f"- {item}")

# Password generator section
st.markdown("---")
st.subheader("Password Generator")

if st.button("Generate Strong Password 🔑"):
    st.session_state.generated_pw = generate_strong_password()

if st.session_state.generated_pw:
    st.code(st.session_state.generated_pw)
    if st.button("Copy to Clipboard 📋"):
        pyperclip.copy(st.session_state.generated_pw)
        st.success("Copied to clipboard!")

# Additional security tips
st.markdown("---")
st.subheader("Security Tips")
st.write("""
- Use at least 12 characters
- Combine unrelated words with numbers/symbols
- Avoid personal information
- Use a unique password for each account
- Consider using a password manager
""")

# To run the app:
# 1. Install required packages: pip install streamlit pyperclip
# 2. Run with: streamlit run password_strength.py