"""
Authentication module for Dashboard SPPG BGN
Uncomment and use this if you want to add password protection
"""

import streamlit as st
import hashlib

def make_hash(password):
    """Create hash from password"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_password):
    """Check if password matches hash"""
    return make_hash(password) == hashed_password

# Default credentials (CHANGE THESE!)
# Username: admin, Password: admin123
CREDENTIALS = {
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
    # Add more users: "username": "hashed_password"
}

def login():
    """Login form"""
    st.markdown("## 🔐 Login Dashboard SPPG BGN")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username in CREDENTIALS:
                if check_hash(password, CREDENTIALS[username]):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
            else:
                st.error("❌ Username tidak ditemukan!")
    
    st.markdown("---")
    st.info("""
    **Demo Credentials:**
    - Username: `admin`
    - Password: `admin123`
    
    ⚠️ **PENTING:** Ganti credentials di file `auth.py` sebelum deploy!
    """)

def logout():
    """Logout function"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def require_authentication(main_function):
    """
    Decorator to require authentication before running main function
    
    Usage:
    from auth import require_authentication
    
    @require_authentication
    def main():
        # Your dashboard code
        pass
    
    if __name__ == "__main__":
        main()
    """
    def wrapper():
        if not is_authenticated():
            login()
        else:
            # Show logout button in sidebar
            with st.sidebar:
                st.markdown("---")
                st.markdown(f"👤 **User:** {st.session_state.get('username', 'Unknown')}")
                if st.button("🚪 Logout"):
                    logout()
            
            # Run main function
            main_function()
    
    return wrapper

# Generate hash for new password
def generate_hash_cli():
    """CLI tool to generate password hash"""
    import sys
    if len(sys.argv) > 1:
        password = sys.argv[1]
        print(f"Password: {password}")
        print(f"Hash: {make_hash(password)}")
        print(f"\nAdd to CREDENTIALS dict:")
        print(f'"username": "{make_hash(password)}"')
    else:
        print("Usage: python auth.py <password>")

if __name__ == "__main__":
    generate_hash_cli()
