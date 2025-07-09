# 🚀 Career Compass AI 🚀

An AI-powered job search application that helps you find your dream opportunities using SerpAPI and Groq LLM, with a beautiful, modern Streamlit interface.

## ✨ Features

### 🎯 **Intelligent Job Matching**
- AI-powered job recommendations based on your query
- Real-time job search using SerpAPI (Google Jobs)
- Smart filtering: location, job type, experience, salary, industry, remote options
- Personalized, easy-to-read job results

### 🔍 **Advanced Search Capabilities**
- **Role-based Search**: Find specific job titles and positions
- **Location-based Search**: Search by city, state, or remote options
- **Salary-based Search**: Filter by minimum salary requirements
- **Experience Level**: Entry, Mid, Senior, or Executive positions
- **Job Type**: Full-time, Part-time, Contract, or Internship
- **Industry Focus**: Technology, Healthcare, Finance, etc.
- **Remote Options**: Remote, Hybrid, or On-site work

### 🎨 **Modern UI**
- Beautiful gradient-based design
- Interactive statistics dashboard
- Hover effects and smooth animations
- Responsive layout
- Professional job card presentation

### 📚 **Search History**
- View your recent job searches and results

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API Key ([Get from Groq Console](https://console.groq.com/))
- SerpAPI Key ([Get from SerpAPI](https://serpapi.com/))

### Installation

1. **Clone the repository and install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Keys**
   - You will be prompted to enter your Groq API key and SerpAPI key in the Streamlit sidebar when running the app.

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage Guide

### Basic Job Search
1. **Enter your Groq API key** and **SerpAPI key** in the sidebar
2. **Type your job search query** in the main input field (e.g., "Software Engineer in New Delhi with Python experience, $120k+ salary")
3. **Click 'Search Jobs'** to see results

### Advanced Search Filters
1. **Click 'Advanced Search Filters'** to expand options
2. **Set your preferences**:
   - **Location**: City or region
   - **Job Type**: Full-time, part-time, contract, internship
   - **Experience Level**: Entry, mid, senior, executive
   - **Salary Range**: Minimum salary
   - **Industry**: e.g., Technology, Healthcare
   - **Remote Work**: Remote, hybrid, or on-site

### Pro Tips for Better Results
- **Be Specific**: Include job title, location, and key skills
- **Use Keywords**: Add relevant technologies or certifications
- **Salary Expectations**: Include salary range for better matches
- **Experience Level**: Specify your experience level
- **Industry Focus**: Mention specific industries

## 🌟 Sample Queries
- "Senior Software Engineer Python React New Delhi $150k+"
- "Data Scientist Machine Learning Remote"
- "Marketing Manager Digital Marketing Remote $80k+"
- "Product Manager SaaS B2B Bengaluru"
- "Business Analyst SQL Tableau Mumbai"

## 🛠️ Technical Details

### Main Tools Used
- **Streamlit**: Modern web application framework
- **LangChain**: LLM orchestration
- **Groq LLM**: Fast and powerful language model
- **SerpAPI**: Real-time job search (Google Jobs)
- **python-dotenv**: For environment variable management

### Dependencies
See `requirements.txt` for the full list. Only the following are required:
- streamlit
- python-dotenv
- langchain
- langchain-community
- langchain-groq
- google-search-results

## 🛠️ Troubleshooting

### Common Issues
- **API Key Error**: Ensure your Groq and SerpAPI keys are valid
- **No Results**: Try broader search terms or different locations
- **Import Errors**: Install all required dependencies with `pip install -r requirements.txt`

## 📞 Support
- Review the troubleshooting section above
- Ensure all dependencies are installed
- Verify your API keys are valid

---

## App Images

![img 1](screenshots/js_1.png)

![img 2](screenshots/js_2.png)

![img 3](screenshots/js_3.png)

![img 4](screenshots/js_4.png)

![img 5](screenshots/js_5.png)

## 🛠️ Troubleshooting

### Common Issues
1. **API Key Error**: Ensure your Groq API key is valid
2. **No Results**: Try broader search terms or different locations
3. **Slow Loading**: Check your internet connection
4. **Import Errors**: Install all required dependencies

### Performance Tips
- Use specific search terms for faster results
- Limit location searches to specific cities
- Use salary ranges to narrow down results
- Save frequently used searches

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review the sample queries for inspiration
- Ensure all dependencies are properly installed
- Verify your API keys are valid

### Contributing
- Report bugs and issues
- Suggest new features
- Improve documentation
- Share your success stories
