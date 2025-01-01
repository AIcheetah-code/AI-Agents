# Financial Analysis Multi-Agent System

## 🚀 Overview
A sophisticated multi-agent system built using Phidata Framework that combines web search capabilities with financial analysis tools. The system utilizes Groq's LLM models to provide comprehensive market insights and financial analysis.

## WorkFlow

![Screenshot 2025-01-01 141612](https://github.com/user-attachments/assets/0af2a2c1-37d1-4f57-8755-58768c007e98)


## 🌟 Features

### 🔍 Web Search Agent
- Real-time web information retrieval
- Credible source verification
- News article and blog analysis
- DuckDuckGo integration for search capabilities
- Markdown-formatted output

### 💹 Financial Agent
- Real-time stock price tracking
- Analyst recommendations analysis
- Company financial fundamentals
- Stock-related news monitoring
- YFinance integration for financial data
- Tabulated data presentation

### 🤝 Multi-Agent Collaboration
- Seamless integration of web and financial data
- Comprehensive market analysis
- Real-time information synthesis
- Enhanced decision-making support

## 🛠️ Technical Stack
- **Language**: Python
- **LLM Model**: Groq (llama3-groq-70B-8192-tool-use-preview)
- **Framework**: Phidata Framework
- **Tools Integration**:
  - YFinance (Financial data)
  - DuckDuckGo (Web search)

## 📋 Prerequisites
- Python 3.8+
- Groq API key
- Required Python packages (phidata, python-dotenv, yfinance, packaging, duckduckgo-search,groq)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/AIcheetah-code/AI-Agents/tree/main/Financial-agent
cd financial-analysis-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add:
```
GROQ_API_KEY=your_groq_api_key_here
```

## 💻 Usage

Basic usage example:
```python
from financial_agent import multi_agent

# Get analysis for a specific stock
multi_agent.print_response("Summarize analyst recommendations and share the latest news for NVDA stock", stream=True)
```

## 🚦 Agent Capabilities

### Web Search Agent
- Real-time web crawling
- News article summarization
- Source verification
- Trend analysis

### Financial Agent
- Stock price monitoring
- Financial metrics analysis
- Analyst recommendation tracking
- Company news aggregation

## 📊 Output Format
- Markdown-formatted responses
- Tabulated financial data
- Source-cited information
- Structured analysis reports

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgments
- Phi Framework team
- Groq LLM team
