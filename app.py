import streamlit as st
#import pymongo
from datetime import date

# ---------------------- APP CONFIG ----------------------
st.set_page_config(page_title="Viabrhaman Travel Agency", page_icon="🌍", layout="wide")

st.title("🌍 Viabrhaman - Tour & Travel Agency Portal")

# Load MongoDB connection from Streamlit Secrets
# Make sure you add this in Streamlit Cloud > Settings > Secrets:
# MONGO_URI = "your_mongo_connection_string"
try:
    MONGO_URI = st.secrets["MONGO_URI"]
except KeyError:
    st.error("❌ MongoDB URI not found! Please add it in Streamlit Secrets.")
    st.stop()

# ---------------------- DATABASE CONNECTION ----------------------
client = pymongo.MongoClient(MONGO_URI)
db = client["viabrhaman_db"]

customers = db["customers"]
packages = db["packages"]
queries = db["queries"]

# ---------------------- SIDEBAR MENU ----------------------
menu = st.sidebar.radio(
    "📍 Navigation",
    ["Home", "Add Customer", "View Customers", "Add Packages", "View Packages", "User Query"]
)

# ---------------------- HOME PAGE ----------------------
if menu == "Home":
    st.markdown("""
    ## ✨ Welcome to Viabrhaman 🌏
    Manage your travel agency easily:
    - ➕ Add new customers  
    - 👀 View customer details  
    - 🏝️ Add or view travel packages  
    - 💬 Receive customer queries  
    """)

# ---------------------- ADD CUSTOMER ----------------------
elif menu == "Add Customer":
    st.subheader("➕ Add New Customer")

    with st.form("add_customer_form"):
        unique_id = st.text_input("Customer Unique ID")
        name = st.text_input("Full Name")
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email")
        travel_start = st.date_input("Travel Start Date", date.today())
        travel_end = st.date_input("Travel End Date", date.today())
        selected_package = st.text_input("Package (e.g. 6D+7N Manali Tour)")

        submit = st.form_submit_button("💾 Save Customer")

        if submit:
            if unique_id and name and mobile:
                customers.insert_one({
                    "unique_id": unique_id,
                    "name": name,
                    "mobile": mobile,
                    "email": email,
                    "travel_start": str(travel_start),
                    "travel_end": str(travel_end),
                    "package": selected_package
                })
                st.success(f"✅ Customer '{name}' added successfully!")
            else:
                st.warning("⚠️ Please fill required fields (ID, Name, Mobile).")

# ---------------------- VIEW CUSTOMERS ----------------------
elif menu == "View Customers":
    st.subheader("👥 Customer Details")
    data = list(customers.find())

    if data:
        for cust in data:
            st.markdown(f"""
            **🆔 ID:** {cust.get('unique_id')}  
            **👤 Name:** {cust.get('name')}  
            **📞 Mobile:** {cust.get('mobile')}  
            **📧 Email:** {cust.get('email')}  
            **📅 Travel:** {cust.get('travel_start')} → {cust.get('travel_end')}  
            **🎒 Package:** {cust.get('package')}
            ---
            """)
    else:
        st.info("No customers found yet. Add one from 'Add Customer' page.")

# ---------------------- ADD PACKAGES ----------------------
elif menu == "Add Packages":
    st.subheader("🏝️ Add New Travel Package")

    with st.form("add_package_form"):
        pkg_name = st.text_input("Package Name")
        pkg_desc = st.text_area("Package Description")
        pkg_price = st.text_input("Price (INR)")
        pkg_duration = st.text_input("Duration (e.g. 6D+7N)")
        add_pkg = st.form_submit_button("➕ Add Package")

        if add_pkg:
            if pkg_name:
                packages.insert_one({
                    "package_name": pkg_name,
                    "description": pkg_desc,
                    "price": pkg_price,
                    "duration": pkg_duration
                })
                st.success(f"✅ Package '{pkg_name}' added successfully!")
            else:
                st.warning("⚠️ Please enter a package name.")

# ---------------------- VIEW PACKAGES ----------------------
elif menu == "View Packages":
    st.subheader("📦 Available Packages")

    pkgs = list(packages.find())
    if pkgs:
        for p in pkgs:
            st.markdown(f"""
            **🏷️ Package:** {p.get('package_name')}  
            **🕒 Duration:** {p.get('duration')}  
            **💰 Price:** ₹{p.get('price')}  
            **📄 Description:** {p.get('description')}
            ---
            """)
    else:
        st.info("No packages available yet. Add some first!")

# ---------------------- USER QUERY ----------------------
elif menu == "User Query":
    st.subheader("💬 Submit Your Query")

    with st.form("user_query_form"):
        q_name = st.text_input("Your Name")
        q_email = st.text_input("Email")
        q_mobile = st.text_input("Mobile Number")
        q_msg = st.text_area("Your Query or Travel Request")

        send = st.form_submit_button("📨 Submit Query")

        if send:
            if q_name and q_email and q_msg:
                queries.insert_one({
                    "name": q_name,
                    "email": q_email,
                    "mobile": q_mobile,
                    "query": q_msg
                })
                st.success("✅ Your query has been submitted successfully!")
            else:
                st.warning("⚠️ Please fill all required fields.")

