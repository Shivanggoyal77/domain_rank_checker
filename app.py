import streamlit as st
import pandas as pd
import requests

# Set up the Streamlit app title and description
st.title("Domain Keyword Ranking Checker")
st.write("Find the rank of any webpage within a given domain for specified keywords.")

# Input fields for domain and keywords
domain = st.text_input("Enter Domain (e.g., example.com):", "")
keywords = st.text_area("Enter Keywords (one per line):")

# API details for SerpApi
SERP_API_KEY = "2558b996729035d96163571675531344574c4d3a4cc2cf5ddab822a461884bba"
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
            "api_key": SERP_API_KEY
        }
        
        # Make the request to SerpApi
        response = requests.get(SERP_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Parse the data to find ranking information for any page under the domain
            domain_results = [
                {
                    "Keyword": keyword,
                    "Rank": result.get("position"),
                    "URL": result.get("link")
                }
                for result in data.get("organic_results", [])
                if domain in result.get("link", "")
            ]
            
            # Add to the results, or show 'Not Found' if none match the domain
            if domain_results:
                results.extend(domain_results)
            else:
                results.append({
                    "Keyword": keyword,
                    "Rank": "Not Found",
                    "URL": ""
                })
        else:
            st.error(f"Error fetching data for keyword: {keyword}")
    
    # Display the results in a table
    if results:
        df = pd.DataFrame(results)
        st.write("Keyword Ranking Results:")
        st.table(df)
    else:
        st.write("No results found for the given domain and keywords.")
else:
    st.info("Please enter both a domain and keywords to proceed.")
