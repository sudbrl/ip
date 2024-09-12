import streamlit as st
import pandas as pd
import socket

# Title of the app
st.title("Domain to IP Address Resolver")

# Option 1: File upload
st.header("Upload Excel File")
uploaded_file = st.file_uploader("Upload an Excel file with domain names", type=["xlsx"])

# Option 2: Manual domain search
st.header("Or Enter Domains Manually")
manual_domains = st.text_area("Enter website domains (one per line):")

# Function to resolve IP addresses (multiple IPs handled)
def resolve_ips(domain_list):
    results = []
    for domain in domain_list:
        try:
            # Use gethostbyname_ex to get all IP addresses
            host_info = socket.gethostbyname_ex(domain)
            ip_addresses = host_info[2]  # This contains all IP addresses
            ip_address_str = ', '.join(ip_addresses)  # Join IPs with commas
            results.append({'Domain': domain, 'IP Address': ip_address_str})
        except socket.gaierror:
            results.append({'Domain': domain, 'IP Address': 'Unable to resolve'})
    return pd.DataFrame(results)

# Process file upload
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    # Assuming the domain names are in the second column of the uploaded file
    domain_list = df.iloc[:, 1].tolist()  # Extract domains from the second column
    result_df = resolve_ips(domain_list)
    
    st.write("IP Addresses from the uploaded file:")
    st.write(result_df)
    
    # Allow the user to download the results as a CSV file
    st.download_button("Download Results as CSV", result_df.to_csv(index=False), "domain_ips.csv", "text/csv")

# Process manual domain input
if st.button("Get IP Addresses for Manual Input") and manual_domains:
    domain_list = manual_domains.splitlines()  # Split user input into a list of domains
    result_df = resolve_ips(domain_list)
    
    st.write("IP Addresses for manual input:")
    st.write(result_df)
    
    # Allow the user to download the results as a CSV file
    st.download_button("Download Results as CSV", result_df.to_csv(index=False), "domain_ips_manual.csv", "text/csv")

# Add a note for the user if neither method is used
if not uploaded_file and not manual_domains:
    st.info("Please either upload a file or enter domains manually to get started.")
