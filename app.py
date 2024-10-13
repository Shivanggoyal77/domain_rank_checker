import streamlit as st
import pandas as pd
import requests
import time

# Set up the Streamlit app title and description
st.title("Domain Keyword Ranking Checker")
st.write("Find the rank of any webpage within a given domain for specified keywords.")

# Input fields for domain and keywords
domain = st.text_input("Enter Domain (e.g., example.com):", "")
keywords = st.text_area("Enter Keywords (one per line):")

# API details for SerpApi
SERP_API_KEY = "746fb325f4e230733e1c703e96f42cb71955e0c8f2d04d67aa916cef74950ea6"
SERP_API_URL = "https://serpapi.com/search.json"

# Button to trigger the rank checking
if st.button("Get Results"):
    # Check if user has entered domain and keywords
    if domain and keywords:
        keyword_list = [keyword.strip() for keyword in keywords.splitlines() if keyword.strip()]
        
        # Limit the number of keywords per query to avoid rate limits (example: 10 keywords)
        max_keywords = 10
        if len(keyword_list) > max_keywords:
            st.warning(f"Limiting to the first {max_keywords} keywords due to API constraints.")
            keyword_list = keyword_list[:max_keywords]
        
        results = []
        
        # Loop through each keyword and find the ranking
        for keyword in keyword_list:
            params = {
                "engine": "google",
                "q": keyword,
                "api_key": SERP_API_KEY
            }
            
            try:
                # Make the request to SerpApi
                response = requests.get(SERP_API_URL, params=params)
                response.raise_for_status()
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
                
                # Small delay to avoid hitting rate limits
                time.sleep(1)
            
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data for keyword: {keyword} - {e}")
        
        # Display the results in a table
        if results:
            df = pd.DataFrame(results)
            st.write("Keyword Ranking Results:")
            st.table(df)
        else:
            st.write("No results found for the given domain and keywords.")
    else:
        st.warning("Please enter both a domain and keywords to proceed.")
