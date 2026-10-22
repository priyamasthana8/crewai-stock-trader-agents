from crewai import Task
from agents.analyst_agent import analyst_agent


get_stock_analysis = Task(
    description=(
    "Analyze the recent performance of the stock: {stock}. Use the "
    "Live Stock Information Tool to retrieve the latest available price, "
    "previous close, daily percentage change, trading volume, daily high "
    "and low, 10-session average volume, and 5-session price trend when "
    "available. Summarize the stock's performance using the available "
    "data. Highlight key observations, compare volume with its average, "
    "and identify missing information. Do not invent market trends, news, "
    "or metrics that are not provided by the tool."
    ),
    expected_output=(
        "A clear, bullet-pointed stock analysis containing:\n"
        "- Stock symbol and latest available price\n"
        "- Previous close and daily price change with percentage\n"
        "- Latest reported volume and daily high/low\n"
        "- 10-session average volume, if available\n"
        "- 5-session price trend, if available\n"
        "- Key observations and data limitations"
    ),
    agent=analyst_agent
)