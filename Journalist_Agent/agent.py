import streamlit as st
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.groq import Groq
from phi.tools.newspaper4k import Newspaper4k
import logging

logging.basicConfig(level=logging.DEBUG)

# Setting up Streamlit app
st.title("AI Startup Trend Analysis Agent 📈")
st.caption("Get the latest trend analysis and startup opportunities based on your topic of interest in a click!.")

topic = st.text_input("Enter the area of interest for your Startup:")
groq_api_key = "your_groq_api_key"

if st.button("Generate Analysis"):
    if not groq_api_key:
        st.warning("Please enter the required API key.")
    else:
        with st.spinner("Processing your request..."):
            try:
                # Initialize groq model
                groq_model = Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key)

                # Define News Collector Agent - DuckDuckGo search tool for collecting articles
                search_tool = DuckDuckGo(search=True, news=True, fixed_max_results=5)

                news_collector = Agent(
                    name="News Collector",
                    role="Searches the web for the most recent articles related to the user's specified startup topic. It gathers news from credible sources and filters out irrelevant or outdated information. It will return detailed article titles, links, and short descriptions to ensure that only relevant articles are passed for summarization.",
                    tools=[search_tool],
                    model=groq_model,
                    instructions=[
                        "Search DuckDuckGo for the most recent news articles related to the specified topic.",
                        "Filter the articles based on relevance and publication date, ensuring the articles reflect current trends and information.",
                        "Collect at least 5 articles, ensuring that each article provides meaningful insights into the topic.",
                        "Return detailed information about each article, including the title, source, and a brief description of the content."
                    ],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Define Summary Writer Agent - Newspaper4k tool for summarizing articles
                news_tool = Newspaper4k(read_article=True, include_summary=True)

                summary_writer = Agent(
                    name="Summary Writer",
                    role="Reads and extracts key insights from the collected news articles. Summarizes each article in a concise, yet informative way, ensuring all important points are highlighted. It should focus on extracting actionable data related to trends, startup opportunities, and relevant statistics.",
                    tools=[news_tool],
                    model=groq_model,
                    instructions=[
                        "Read the articles collected by the News Collector agent thoroughly.",
                        "Summarize each article clearly and concisely, focusing on the key points, data, and trends. Extract relevant insights on emerging startup opportunities, new business ideas, market trends, or any disruptive innovations mentioned in the articles.",
                        "Ensure that the summary provides actionable insights that could be used by an entrepreneur to understand the latest market dynamics in the specified area.",
                        "Provide a well-structured summary for each article, including key takeaways, insights into market behavior, and potential startup ideas."
                    ],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Define Trend Analyzer Agent - Analyzes trends from the summaries
                trend_analyzer = Agent(
                    name="Trend Analyzer",
                    role="Analyzes the summaries from the Summary Writer Agent to identify emerging trends and startup opportunities. It should assess the collected data, identify patterns, and make recommendations for entrepreneurs about market gaps and growth opportunities. It will provide a detailed, structured analysis of trends.",
                    model=groq_model,
                    instructions=[
                        "Analyze the summaries provided by the Summary Writer agent to extract key emerging trends and startup opportunities.",
                        "Focus on identifying patterns in the market, such as new technologies, market disruptions, consumer behavior changes, and new business models.",
                        "Assess the viability of each identified trend as a potential startup opportunity. Consider market demand, scalability, competition, and innovation.",
                        "Provide a detailed report that outlines each identified trend, its potential impact, and the types of startups that could thrive in these emerging areas.",
                        "Structure the report clearly and offer actionable insights that an entrepreneur can follow to tap into these opportunities."
                    ],
                    show_tool_calls=True,
                    markdown=True,
                )

                # The multi-agent Team setup for trend analysis
                agent_team = Agent(
                    agents=[news_collector, summary_writer, trend_analyzer],
                    instructions=[
                        "Start by searching for recent news articles on the topic provided by the user using DuckDuckGo.",
                        "After gathering the articles, pass them to the Summary Writer agent. Ensure that each article is summarized in a way that highlights the trends and startup opportunities.",
                        "The Summary Writer will condense the information and pass the summaries to the Trend Analyzer agent for analysis.",
                        "The Trend Analyzer will thoroughly review the summaries, identify key trends, and present actionable startup opportunities in a detailed report format.",
                        "Ensure that the entire process from collecting articles to generating the trend report flows seamlessly. The output should be informative, structured, and helpful for entrepreneurs looking to enter the market."
                    ],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Executing the multi-agent workflow
                # Step 1: Collect news
                news_response = news_collector.run(f"Collect recent news on {topic}")
                articles = news_response.content

                # Step 2: Summarize articles
                summary_response = summary_writer.run(f"Summarize the following articles:\n{articles}")
                summaries = summary_response.content

                # Step 3: Analyze trends
                trend_response = trend_analyzer.run(f"Analyze trends from the following summaries:\n{summaries}")
                analysis = trend_response.content


                st.subheader("Trend Analysis and Potential Startup Opportunities")
                st.write(analysis)

            except Exception as e:
                st.error(f"An error occurred: {e}")
