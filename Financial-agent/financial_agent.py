from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import groq

import os
from dotenv import load_dotenv
load_dotenv()
groq.api_key = os.getenv("GROQ_API_KEY")

# Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information",
    model=Groq(id="llama3-groq-70B-8192-tool-use-preview"),
    description=(
        "A dedicated agent designed to search and retrieve the latest information "
        "from the web. Specializes in finding up-to-date news and online data "
        "using various web-based tools. The agent leverages the DuckDuckGo search engine "
        "to gather web information efficiently and is focused on returning relevant, "
        "credible sources, ensuring that results are trustworthy. Ideal for retrieving "
        "news articles, blogs, and real-time updates on a broad range of topics."
    ),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include sources to ensure reliability.",
        "Provide concise summaries of the information found, including essential details."
    ],
    show_tools_calls=True,
    markdown=True,
)

# Financial Agent
financial_agent = Agent(
    name="Financial Agent",
    model=Groq(id="llama3-groq-70B-8192-tool-use-preview"),
    description=(
        "An expert financial analysis agent focused on retrieving and presenting key "
        "financial data. This agent uses tools like YFinance to pull in stock-related "
        "information such as current stock prices, analyst recommendations, company "
        "financial fundamentals, and related news. It specializes in presenting this "
        "information in easy-to-read tables, making it ideal for investors and analysts. "
        "This agent is also capable of delivering company performance metrics, including "
        "profitability ratios, market movements, and shareholder insights. It helps users "
        "quickly assess market conditions and stock potential."
    ),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=[
        "Use tables to display stock prices, analyst recommendations, and key financial data.",
        "Provide clear and well-organized summaries of any financial news or updates."
    ],
    show_tools_calls=True,
    markdown=True,
)

# Multi Agent
multi_agent = Agent(
    team=[web_search_agent, financial_agent],
    instructions=[
        "Always include sources to ensure reliability.",
        "Use tables to display stock prices and financial data whenever applicable.",
        "Provide clear summaries combining both financial data and web-retrieved news."
    ],
    model=Groq(id="llama3-groq-70B-8192-tool-use-preview"),
    description=(
        "A collaborative agent team combining the expertise of both the Web Search Agent and "
        "the Financial Agent. The Web Search Agent provides up-to-date news and real-time "
        "information from online sources, while the Financial Agent retrieves stock data, "
        "analyst recommendations, and company fundamentals. This multi-agent setup ensures "
        "comprehensive coverage of both web and financial insights, making it ideal for use cases "
        "that require detailed market analysis as well as real-time news updates."
    ),
    show_tools_calls=True,
    markdown=True,
)

# Running the multi-agent for NVDA stock summary
multi_agent.print_response("Summarize analyst recommendations and share the latest news for NVDA stock and detailed report also", stream=True)
