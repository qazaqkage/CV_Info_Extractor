import streamlit as st
import requests

BASE_URL = "http://backend:5000"  # Flask backend URL

# Ensure a logged-in state using Streamlit's session state
if "token" not in st.session_state:
    st.session_state["token"] = None

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Login successful!")
            token = response.json().get("access_token")
            st.session_state["token"] = token  # Store the token in session state
            st.session_state["logged_in"] = True
        else:
            st.error(response.json().get("error"))

def register():
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password, "name": name})
        if response.status_code == 201:
            st.success("Registration successful! You can now log in.")
        else:
            st.error(response.json().get("error"))

def upload_cv():
    if not st.session_state.get("token"):  # Check if the user is logged in
        st.warning("Please log in to upload your CV.")
        return

    st.title("Upload Your CV")

    # Display personalized greeting
    if st.session_state.get("name"):
        st.write(f"Hello, {st.session_state['name']}!")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.success(f"File selected: {uploaded_file.name}")

    if st.button("Upload CV"):
        if uploaded_file is not None:
            # Prepare the file for upload
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}

            # Send the file to the backend
            response = requests.post(f"{BASE_URL}/upload_cv", files=files, headers=headers)

            # Handle the response
            if response.status_code == 200:
                st.success("CV uploaded successfully!")
            else:
                error_message = response.json().get('error', 'Unknown error')
                error_details = response.json().get('details', '')
                st.error(f"Upload failed: {error_message}")
                if error_details:
                    st.error(f"Details: {error_details}")
        else:
            st.error("Please select a file to upload.")



# Navigation options
PAGES = {
    "Login": login,
    "Register": register,
    "Upload CV": upload_cv,
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Restrict access to "Upload CV" if not logged in
    if selection == "Upload CV" and not st.session_state.get("token"):
        st.warning("You need to log in to access this page.")
        selection = "Login"

    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
