import streamlit as st
import pandas as pd
import requests
import time

# Set up the Streamlit app title and description
st.title("Domain Keyword Ranking Checker")
st.write("Find the rank of any webpage within a given domain for specified keywords using Google Custom Search API.")

# Input fields for domain and keywords
domain = st.text_input("Enter Domain (e.g., example.com):", "")
keywords = st.text_area("Enter Keywords (one per line):")

# Google Custom Search API details
API_KEY = "AIzaSyDj2krchXWyXkWWmkCk1jqoWCEc_OPAVeQ"
CX = "34c3745f38a364043"
GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"

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
                "key": API_KEY,
                "cx": CX,
                "q": keyword,
                "num": 10  # Adjust the number of search results to retrieve, max is 10
            }
            
            try:
                # Make the request to Google Custom Search API
                response = requests.get(GOOGLE_CSE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Parse the data to find ranking information for any page under the domain
                domain_results = [
                    {
                        "Keyword": keyword,
                        "Rank": idx + 1,
                        "URL": item.get("link")
                    }
                    for idx, item in enumerate(data.get("items", []))
                    if domain in item.get("link", "")
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
