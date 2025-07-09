import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import random

# Load environment variables
load_dotenv()

# Custom CSS for artistic design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #2980b9 100%);
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2980b9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        min-width: 150px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2980b9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .sidebar-header h3 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
    }
    
    .job-card {
        background: linear-gradient(135deg, #e3f0ff 0%, #b3c6e6 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid #2980b9;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .job-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        font-size: 1.1rem;
        color: #2980b9;
        margin-bottom: 0.5rem;
    }
    
    .job-location {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 1rem;
    }
    
    .job-description {
        color: #34495e;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .job-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #ecf0f1;
    }
    
    .job-type {
        background: linear-gradient(135deg, #1e3c72 0%, #2980b9 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    
    .job-salary {
        color: #2980b9;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .search-container {
        background: linear-gradient(135deg, #e3f0ff 0%, #b3c6e6 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .search-input {
        background: white;
        border: 2px solid #2980b9;
        border-radius: 25px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        width: 100%;
        max-width: 500px;
        margin: 1rem 0;
    }
    
    .search-button {
        background: linear-gradient(135deg, #1e3c72 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .search-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    }
    
    .filter-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .filter-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #e3f0ff 0%, #b3c6e6 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: #1e3c72;
        font-weight: bold;
    }
    
    .error-message {
        background: linear-gradient(135deg, #b3c6e6 0%, #1e3c72 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: #fff;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Custom Job Search function using SerpAPI
def search_jobs_serpapi(query, serpapi_key, max_results=5):
    try:
        serpapi = SerpAPIWrapper(serpapi_api_key=serpapi_key)
        results = serpapi.run(query)
        # If results is a string, try to split and keep only the first 5 jobs
        if isinstance(results, str):
            lines = results.strip().split('\n')
            job_blocks = []
            current_block = []
            for line in lines:
                if line.strip() == '' and current_block:
                    job_blocks.append('\n'.join(current_block))
                    current_block = []
                else:
                    current_block.append(line)
            if current_block:
                job_blocks.append('\n'.join(current_block))
            top_5_jobs = '\n\n'.join(job_blocks[:max_results])
            return top_5_jobs
        return results
    except Exception as e:
        return f"SerpAPI error: {str(e)}"

# Main header with artistic design
st.markdown("""
<div class="main-header">
    <h1>🚀 Career Compass AI 🚀</h1>
    <p>Your AI-powered job search companion for finding dream opportunities</p>
</div>
""", unsafe_allow_html=True)

# Statistics section
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-number">10M+</div>
        <div class="stat-label">Jobs Available</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">500+</div>
        <div class="stat-label">Companies</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">50+</div>
        <div class="stat-label">Industries</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">AI Support</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Creative description
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <p style="font-size: 1.2rem; color: #666; font-style: italic; line-height: 1.6;">
        "Transform your career journey with AI-powered job discovery. 
        From entry-level positions to executive roles, find opportunities that match your skills, 
        experience, and aspirations. Let our intelligent assistant guide you to your next big break!"
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with artistic design
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>⚙️ Search Controls</h3>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        "🔑 Enter your Groq API Key:",
        type="password",
        help="Your AI assistant key for intelligent job matching"
    )
    serpapi_key = st.text_input(
        "🔑 Enter your SerpAPI Key:",
        type="password",
        help="Required for job search via SerpAPI"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h4>🎯 Search Features</h4>
        <p>• AI-Powered Job Matching</p>
        <p>• Real-time Job Updates</p>
        <p>• Salary Insights</p>
        <p>• Company Information</p>
        <p>• Location-based Search</p>
        <p>• Skill-based Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h4>💡 Pro Tips</h4>
        <p>• Be specific with job titles</p>
        <p>• Include location preferences</p>
        <p>• Mention required skills</p>
        <p>• Specify experience level</p>
        <p>• Add salary expectations</p>
    </div>
    """, unsafe_allow_html=True)

# Search interface
st.markdown("""
<div class="search-container">
    <h2 style="color: #2c3e50; margin-bottom: 1rem;">🔍 Find Your Dream Job</h2>
    <p style="color: #7f8c8d; margin-bottom: 2rem;">
        Tell me what you're looking for, and I'll help you discover the perfect opportunities!
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "job_search_history" not in st.session_state:
    st.session_state["job_search_history"] = []

# Job search input
job_query = st.text_input(
    "🎯 What job are you looking for?",
    placeholder="e.g., Software Engineer in New Delhi with Python experience",
    help="Be specific about role, location, skills, and salary expectations"
)

# Search filters
with st.expander("🔧 Advanced Search Filters", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("📍 Location", placeholder="e.g., New Delhi, ND")
        job_type = st.selectbox("💼 Job Type", ["Any", "Full-time", "Part-time", "Contract", "Internship"])
        experience_level = st.selectbox("📈 Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
    
    with col2:
        salary_min = st.number_input("💰 Minimum Salary ($)", min_value=0, value=50000, step=5000)
        industry = st.text_input("🏢 Industry", placeholder="e.g., Technology, Healthcare")
        remote_option = st.selectbox("🏠 Remote Work", ["Any", "Remote", "Hybrid", "On-site"])

# Search button
if st.button("🚀 Search Jobs", type="primary"):
    if api_key and serpapi_key and job_query:
        try:
            # Build comprehensive search query
            search_query = job_query
            if location:
                search_query += f" in {location}"
            if job_type != "Any":
                search_query += f" {job_type}"
            if experience_level != "Any":
                search_query += f" {experience_level} level"
            if industry:
                search_query += f" {industry} industry"
            if remote_option != "Any":
                search_query += f" {remote_option}"
            search_query += f" salary ${salary_min}+"

            # Show search status
            with st.status("🔍 Searching for your dream job...", expanded=True) as status:
                # Use SerpAPI for job search
                response = search_jobs_serpapi(search_query, serpapi_key)
                if "error" in response.lower():
                    st.error(response)
                    status.update(label="❌ Search failed", state="error")
                    st.stop()
                # Format the job search results with AI
                llm = ChatGroq(
                    groq_api_key=api_key,
                    model_name="Llama3-8b-8192",
                    streaming=True
                )
                formatted_response = llm.invoke(
                    f"Format the following job search results in a clear, structured way. "
                    f"Organize by job title, company, location, and key details. "
                    f"Make it easy to read and professional:\n\n{response}"
                ).content
                response = formatted_response
                status.update(label="✅ Jobs found!", state="complete")

            # Add to search history
            st.session_state.job_search_history.append({
                'query': search_query,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            # Display results
            st.markdown("""
            <div class="success-message">
                🎉 Found amazing opportunities for you! Here are the results:
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                        padding: 2rem; border-radius: 20px; margin: 2rem 0;">
                <h3 style="color: #2c3e50; text-align: center; margin-bottom: 2rem;">
                    💼 Job Opportunities
                </h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(response)
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                ❌ Oops! Something went wrong: {str(e)}
            </div>
            """, unsafe_allow_html=True)
            st.info("Please check your API keys and try again.")
    else:
        st.warning("🔑 Please provide your Groq API key, SerpAPI key, and a job search query!")

# Search history
if st.session_state.job_search_history:
    st.markdown("---")
    st.markdown("""
    <h3 style="color: #2c3e50; text-align: center; margin: 2rem 0;">
        📚 Recent Searches
    </h3>
    """, unsafe_allow_html=True)
    
    for i, search in enumerate(reversed(st.session_state.job_search_history[-5:]), 1):
        with st.expander(f"🔍 Search #{i}: {search['query'][:50]}... ({search['timestamp']})"):
            st.write(search['response'])

# Footer with creative message
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; margin-top: 3rem; color: white;">
    <h3 style="margin-bottom: 1rem;">🌟 Your Career Journey Starts Here 🌟</h3>
    <p style="font-size: 1.1rem; margin-bottom: 1rem;">
        "Every job search is a step toward your dream career. 
        Let AI be your compass in this exciting journey!"
    </p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Powered by Google Jobs API & Groq | Crafted with career passion
    </p>
</div>
""", unsafe_allow_html=True) 
