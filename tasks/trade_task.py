# from crewai import Task
# from agents.trader_agent import trader_agent

# trade_decision = Task(
#     description=(
#         "Use live market data and stock performance indicators for {stock} to make a strategic trading decision. "
#         "Assess key factors such as current price, daily change percentage, volume trends, and recent momentum. "
#         "Based on your analysis, recommend whether to **Buy**, **Sell**, or **Hold** the stock."
#     ),
#     expected_output=(
#         "A clear and confident trading recommendation (Buy / Sell / Hold), supported by:\n"
#         "- Current stock price and daily change\n"
#         "- Volume and market activity observations\n"
#         "- Justification for the trading action based on technical signals or risk-reward outlook"
#     ),
#     agent=trader_agent
# )





from crewai import Task
from agents.trader_agent import trader_agent
from tasks.analyse_task import get_stock_analysis


trade_decision = Task(
    description=(
    "Evaluate the stock {stock} using the market data and findings "
    "from the preceding stock analysis task. Consider the latest "
    "available price, daily change, volume, day range, 10-session "
    "average volume, and 5-session price trend when available. "
    "Recommend Buy, Sell, or Hold with a clear, evidence-based "
    "justification. Identify missing information, avoid unsupported "
    "assumptions, and explain the key risks. If the available data "
    "is insufficient for a confident decision, state its limitations "
    "and explain what additional evidence is needed. Do not invent "
    "financial metrics or market news."
    ),
    expected_output=(
        "A structured trading report containing:\n"
        "- Stock symbol and latest available price\n"
        "- Daily change and percentage\n"
        "- Volume and volatility observations, if supported by data\n"
        "- 10-session average volume and 5-session trend, if available\n"
        "- Recommendation: Buy, Sell, or Hold\n"
        "- Evidence supporting the recommendation\n"
        "- Key risks and limitations"
    ),
    agent=trader_agent,
    context=[get_stock_analysis]
)
