import streamlit as st
import pandas as pd
import requests

# Set up the Streamlit app title and description
st.title("Domain Keyword Ranking Checker")
st.write("Find the rank of a webpage in a given domain for specified keywords.")

# Input fields for domain and keywords
domain = st.text_input("Enter Domain (e.g., example.com):", "")
keywords = st.text_area("Enter Keywords (one per line):")

# API details for SerpApi
SERP_API_KEY = "YOUR_SERPAPI_KEY"
SERP_API_URL = "https://serpapi.com/search.json"

# Check if user has entered domain and keywords
if domain and keywords:
    keyword_list = [keyword.strip() for keyword in keywords.splitlines() if keyword.strip()]
    
    results = []
    
    # Loop through each keyword and find the ranking
    for keyword in keyword_list:
        params = {
            "engine": "google",
            "q": keyword,
            "domain": domain,
            "api_key": SERP_API_KEY
        }
        
        # Make the request to SerpApi
        response = requests.get(SERP_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Parse the data to find the ranking information
            for result in data.get("organic_results", []):
                rank = result.get("position")
                url = result.get("link")
                
                if domain in url:
                    results.append({
                        "Keyword": keyword,
                        "Rank": rank,
                        "URL": url
                    })
                    break
            else:
                results.append({
                    "Keyword": keyword,
                    "Rank": "Not Found",
                    "URL": ""
                })
        else:
            st.error(f"Error fetching data for keyword: {keyword}")
    
    # Display the results in a table
    df = pd.DataFrame(results)
    st.write("Keyword Ranking Results:")
    st.table(df)
else:
    st.info("Please enter both a domain and keywords to proceed.")

