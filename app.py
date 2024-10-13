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
API_KEY = "AIzaSyDj2krchXWyXkWWmkCk1jqoWCEc_OPAVeQ"
CX = "34c3745f38a364043"
GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"

# Helper function to check if the URL belongs to the domain
def is_url_in_domain(url, domain):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    # Remove 'www.' if present
    netloc = netloc.replace('www.', '')
    # Compare domain with the normalized URL
    return domain in netloc

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
            found = False
            for start in range(1, 101, 10):  # Increment by 10 for pagination up to 100 results
                params = {
                    "key": API_KEY,
                    "cx": CX,
                    "q": keyword,
                    "num": 10,  # Number of results per request
                    "start": start
                }
                
                try:
                    # Make the request to Google Custom Search API
                    response = requests.get(GOOGLE_CSE_URL, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Parse the data to find ranking information for any page under the domain
                    for idx, item in enumerate(data.get("items", [])):
                        url = item.get("link")
                        if is_url_in_domain(url, domain):
                            results.append({
                                "Keyword": keyword,
                                "Rank": start + idx,
                                "URL": url
                            })
                            found = True
                            break
                    
                    # Stop further requests if rank is found for this keyword
                    if found:
                        break
                    
                    # Delay to avoid hitting rate limits
                    time.sleep(1)
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching data for keyword: {keyword} - {e}")
                    break

            # If no results for domain found within 100 results, mark as "Not Found"
            if not found:
                results.append({
                    "Keyword": keyword,
                    "Rank": "Not Found",
                    "URL": ""
                })
        
        # Display the results in a table
        if results:
            df = pd.DataFrame(results)
            st.write("Keyword Ranking Results:")
            st.table(df)
        else:
            st.write("No results found for the given domain and keywords.")
    else:
        st.warning("Please enter both a domain and keywords to proceed.")
