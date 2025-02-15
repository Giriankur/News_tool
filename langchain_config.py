from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# Set API keys
groq_api_key = "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"
newsapi_key = "d65ccd2c2bf340b4b4f480f078f9b8c4"

# Initialize Groq LLM
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-8b-8192")

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=newsapi_key)

# Function to fetch news articles
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language="en", sort_by="relevancy")
    return articles["articles"]

# Function to extract and summarize article descriptions
def summarize_articles(articles):
    summaries = [article["description"] for article in articles if article["description"]]
    return " ".join(summaries)

# Function to get summarized news for LangChain input
def get_summary(query):
    articles = get_news_articles(query)
    summary = summarize_articles(articles)
    return summary

# Define the LLM prompt
template = """
You are an AI assistant helping an equity research analyst. 
Given the following query and the provided news article summaries, provide an overall summary.

Query: {query}
Summaries: {summaries}
"""
prompt = PromptTemplate(template=template, input_variables=["query", "summaries"])

# Create the LangChain LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm)
