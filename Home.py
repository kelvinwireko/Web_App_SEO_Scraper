import streamlit as st
from tools import scraper


st.title("Codename: Analyzer")
description = """Get the content outline of the first 10 results on Google. 
"""
description2 = """And incorporate them into your content brief."""
st.subheader(description)
st.write(description2)

user_input = st.text_input(label="Enter Your Keyword", placeholder="Enter your keyword...", key="keyword")

st.button("Get Outline", key="get_outline")

data = scraper.page_source(user_input)
serp_results = scraper.scrape_serp_results(data)
headings = scraper.scrape_headings()
related_results = scraper.search_related_results(data)
questions = scraper.scrape_paa(user_input)

if bool(headings):
    st.header("Content Outline")
    st.table(headings)

if bool(questions):
    st.header("People Also Ask")
    st.table(questions)

if bool(related_results):
    st.header("Related Search Results")
    st.table(related_results)
