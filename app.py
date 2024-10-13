import streamlit as st
import pandas as pd
import requests
import time
from urllib.parse import urlparse

# Set up the Streamlit app title and description
st.title("Domain Keyword Ranking Checker")
st.write("Find the rank of any webpage within a given domain for specified keywords using Google Custom Search API.")

# Input fields for domain and keywords
domain = st.text_input("Enter Domain (e.g., example.com):", "")
keywords = st.text_area("Enter Keywords (one per line):")

# Google Custom Search API details

GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"

# Helper function to check if the URL belongs to the domain
def is_url_in_domain(url, domain):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    netloc = netloc.replace('www.', '')  # Remove 'www.' if present
    return domain in netloc

# Button to trigger the rank checking
if st.button("Get Results"):
    if domain and keywords:
        keyword_list = [keyword.strip() for keyword in keywords.splitlines() if keyword.strip()]
        
        # Limit the number of keywords per query to avoid rate limits
        max_keywords = 10
        if len(keyword_list) > max_keywords:
            st.warning(f"Limiting to the first {max_keywords} keywords due to API constraints.")
            keyword_list = keyword_list[:max_keywords]
        
        results = []
        
        # Loop through each keyword and find the ranking
        for keyword in keyword_list:
            found = False
            st.write(f"### Searching for keyword: {keyword}")
            for start in range(1, 101, 10):
                st.write(f"Requesting results {start} to {start + 9}...")

                params = {
                    "key": API_KEY,
                    "cx": CX,
                    "q": keyword,
                    "num": 10,  
                    "start": start
                }
                
                try:
                    response = requests.get(GOOGLE_CSE_URL, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Debugging: Show raw data for each query
                    st.write("**Raw API Response:**")
                    st.json(data)
                    
                    # Parse and check each result for domain match
                    for idx, item in enumerate(data.get("items", [])):
                        url = item.get("link")
                        title = item.get("title", "No title")
                        
                        # Debugging: Display each URL and title retrieved
                        st.write(f"Result {start + idx}: Title - {title}, URL - {url}")

                        if is_url_in_domain(url, domain):
                            st.write(f"**Domain match found at rank {start + idx}:** {url}")
                            results.append({
                                "Keyword": keyword,
                                "Rank": start + idx,
                                "URL": url
                            })
                            found = True
                            break
                    
                    if found:
                        break
                    
                    # Delay to avoid hitting rate limits
                    time.sleep(1)
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching data for keyword: {keyword} - {e}")
                    break
            
            if not found:
                st.write(f"No match found for '{keyword}' within the first 100 results.")
                results.append({
                    "Keyword": keyword,
                    "Rank": "Not Found",
                    "URL": ""
                })
        
     # Display final results table
        if results:
            df = pd.DataFrame(results)
            st.write("### Keyword Ranking Results")
            st.table(df)
        else:
            st.write("No results found for the given domain and keywords.")
    else:
        st.warning("Please enter both a domain and keywords to proceed.")
