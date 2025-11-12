import streamlit as st
from config import customers_collection, queries_collection, packages_collection
from bson.objectid import ObjectId

st.set_page_config(page_title="Viabrhaman Travel Agency", page_icon="🌍", layout="wide")

st.title("🌍 Viabrhaman - Travel Agency Portal")

menu = st.sidebar.radio("Navigation", ["Home", "Add Customer", "View Customers", "Packages", "User Query"])

# --- Admin: Add Customer ---
if menu == "Add Customer":
    st.subheader("➕ Add Customer Data")

    unique_id = st.text_input("Customer ID")
    name = st.text_input("Full Name")
    mobile = st.text_input("Mobile Number")
    travel_dates = st.date_input("Travel Dates")
    package = st.text_input("Travel Package (e.g., 6D+7N Manali Tour)")

    if st.button("Save Customer"):
        if unique_id and name and mobile:
            data = {
                "unique_id": unique_id,
                "name": name,
                "mobile": mobile,
                "travel_dates": str(travel_dates),
                "package": package
            }
            customers_collection.insert_one(data)
            st.success(f"✅ Data for {name} saved successfully!")
        else:
            st.warning("Please fill all required fields.")

# --- Admin: View Customers ---
elif menu == "View Customers":
    st.subheader("📋 Customer List")
    data = list(customers_collection.find())
    if data:
        for cust in data:
            st.write(f"**ID:** {cust.get('unique_id')} | **Name:** {cust.get('name')} | **Mobile:** {cust.get('mobile')} | **Package:** {cust.get('package')} | **Dates:** {cust.get('travel_dates')}")
    else:
        st.info("No customer data available.")

# --- Admin: Packages Section ---
elif menu == "Packages":
    st.subheader("🏖️ Manage Travel Packages")

    pkg_name = st.text_input("Package Name")
    pkg_desc = st.text_area("Description")
    pkg_price = st.text_input("Price (INR)")

    if st.button("Add Package"):
        if pkg_name:
            packages_collection.insert_one({
                "package_name": pkg_name,
                "description": pkg_desc,
                "price": pkg_price
            })
            st.success(f"✅ Package '{pkg_name}' added.")
        else:
            st.warning("Please enter package name.")

    st.divider()
    st.subheader("Available Packages:")
    pkgs = list(packages_collection.find())
    if pkgs:
        for p in pkgs:
            st.write(f"**{p['package_name']}** — {p['description']} (₹{p['price']})")
    else:
        st.info("No packages added yet.")

# --- User: Query Form ---
elif menu == "User Query":
    st.subheader("💬 Submit Your Query")

    user_name = st.text_input("Your Name")
    user_email = st.text_input("Email")
    user_mobile = st.text_input("Mobile Number")
    user_query = st.text_area("Your Query")

    if st.button("Submit Query"):
        if user_name and user_email and user_query:
            queries_collection.insert_one({
                "name": user_name,
                "email": user_email,
                "mobile": user_mobile,
                "query": user_query
            })
            st.success("✅ Your query has been submitted! We'll contact you soon.")
        else:
            st.warning("Please fill in all required fields.")

# --- Home Page ---
else:
    st.write("""
    ## Welcome to Viabrhaman 🌏  
    Discover beautiful destinations and seamless travel experiences.  
    Use the sidebar to navigate:
    - Add or view customer data  
    - Manage packages  
    - Submit travel queries  
    """)
