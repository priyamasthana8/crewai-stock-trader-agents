# import yfinance as yf
# from crewai.tools import tool


# @tool("Live Stock Information Tool")
# def get_stock_price(stock_symbol: str) -> str:
#     """
#     Retrieves the latest stock price and other relevant info for a given stock symbol using Yahoo Finance.

#     Parameters:
#         stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT).

#     Returns:
#         str: A summary of the stock's current price, daily change, and other key data.
#     """
#     stock = yf.Ticker(stock_symbol)
#     info = stock.info

#     current_price = info.get("regularMarketPrice")
#     change = info.get("regularMarketChange")
#     change_percent = info.get("regularMarketChangePercent")
#     currency = info.get("currency", "USD")

#     if current_price is None:
#         return f"Could not fetch price for {stock_symbol}. Please check the symbol."

#     return (
#         f"Stock: {stock_symbol.upper()}\n"
#         f"Price: {current_price} {currency}\n"
#         f"Change: {change} ({round(change_percent, 2)}%)"
#     )




# import yfinance as yf
# from crewai.tools import tool


# @tool("Live Stock Information Tool")
# def get_stock_price(stock_symbol: str) -> str:
#     """
#     Retrieves the latest stock price and other relevant info for a given stock symbol using Yahoo Finance.

#     Parameters:
#         stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT).

#     Returns:
#         str: A summary of the stock's current price, daily change, and other key data.
#     """
#     stock = yf.Ticker(stock_symbol)
#     info = stock.info

#     current_price = info.get("regularMarketPrice")
#     change = info.get("regularMarketChange")
#     change_percent = info.get("regularMarketChangePercent")
#     currency = info.get("currency", "USD")

#     if current_price is None:
#         return f"Could not fetch price for {stock_symbol}. Please check the symbol."

#     return (
#         f"Stock: {stock_symbol.upper()}\n"
#         f"Price: {current_price} {currency}\n"
#         f"Change: {change} ({round(change_percent, 2)}%)"
#     )






# import yfinance as yf
# from crewai.tools import tool


# @tool("Live Stock Information Tool")
# def get_stock_price(stock_symbol: str) -> str:
#     """Retrieve the latest available Yahoo Finance quote and daily market indicators.
#     Accepts ticker symbols such as AAPL, MSFT, TSLA, or RELIANCE.NS.
#     """
#     try:
#         symbol = stock_symbol.strip().upper()

#         if not symbol:
#             return "Error: Please provide a valid stock ticker symbol."

#         stock = yf.Ticker(symbol)
#         info = stock.info
#         fast_info = stock.fast_info

#         price = info.get("regularMarketPrice")
#         if price is None:
#             price = fast_info.get("last_price")

#         previous_close = info.get("regularMarketPreviousClose")
#         if previous_close is None:
#             previous_close = fast_info.get("previous_close")

#         currency = info.get("currency", "Unknown")
#         volume = info.get("regularMarketVolume")
#         day_high = info.get("regularMarketDayHigh")
#         day_low = info.get("regularMarketDayLow")

#         if price is None:
#             return (
#                 f"No price data found for {symbol}. "
#                 "Check the ticker symbol or try again later."
#             )

#         change = None
#         change_percent = None

#         if previous_close and previous_close != 0:
#             change = price - previous_close
#             change_percent = (change / previous_close) * 100

#         if volume is None:
#             volume = fast_info.get("last_volume")

#         def fmt(value, decimals=2):
#             if value is None:
#                 return "Unavailable"
#             return f"{value:,.{decimals}f}"

#         return (
#             f"Stock: {symbol}\n"
#             f"Price: {fmt(price)} {currency}\n"
#             f"Previous Close: {fmt(previous_close)}\n"
#             f"Daily Change: {fmt(change)} {currency}\n"
#             f"Daily Change %: {fmt(change_percent)}%\n"
#             f"Trading Volume: {fmt(volume, 0)}\n"
#             f"Day High: {fmt(day_high)}\n"
#             f"Day Low: {fmt(day_low)}\n"
#             "Source: Yahoo Finance"
#         )

#     except Exception as e:
#         return (
#             f"Could not retrieve market data for {stock_symbol}. "
#             f"Error: {type(e).__name__}: {e}"
#         )





from datetime import datetime

import pandas as pd
import yfinance as yf
from crewai.tools import tool


@tool("Live Stock Information Tool")
def get_stock_price(stock_symbol: str) -> str:
    """
    Fetch recent stock-market data, daily price change, trading volume,
    10-session average volume, and the 5-session price trend.
    """

    try:
        symbol = stock_symbol.strip().upper()

        # Convert common company names into Yahoo Finance ticker symbols.
        aliases = {
            "TESLA": "TSLA",
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT",
            "NVIDIA": "NVDA",
            "AMAZON": "AMZN",
            "GOOGLE": "GOOGL",
            "ALPHABET": "GOOGL",
            "META": "META",
        }
        symbol = aliases.get(symbol, symbol)

        ticker = yf.Ticker(symbol)
        history = ticker.history(
            period="1mo",
            interval="1d",
            auto_adjust=False
        )

        if history.empty or len(history) < 2:
            return f"Insufficient market data found for {symbol}."

        history = history.dropna(subset=["Close"])

        if len(history) < 2:
            return f"Insufficient closing-price data found for {symbol}."

        # Latest available daily candle; it may be incomplete during
        # an active trading session.
        latest = history.iloc[-1]
        previous_close = float(history["Close"].iloc[-2])
        latest_close = float(latest["Close"])

        daily_change = latest_close - previous_close
        daily_change_pct = (
            (daily_change / previous_close) * 100
            if previous_close else 0
        )

        # Exclude today's candle from historical averages if today's
        # session is present, because its volume may still be incomplete.
        market_tz = history.index.tz
        if market_tz is not None:
            market_today = pd.Timestamp.now(tz=market_tz).date()
        else:
            market_today = datetime.now().date()

        latest_date = history.index[-1].date()

        if latest_date == market_today:
            completed_history = history.iloc[:-1]
        else:
            completed_history = history

        # Average volume over the latest 10 completed trading sessions.
        last_10_sessions = completed_history.tail(10)
        average_volume = (
            float(last_10_sessions["Volume"].mean())
            if not last_10_sessions.empty
            else None
        )

        # Price movement across the latest 5 completed sessions.
        trend_data = completed_history.tail(6)
        if len(trend_data) >= 6:
            start_price = float(trend_data["Close"].iloc[0])
            end_price = float(trend_data["Close"].iloc[-1])

            trend_change_pct = (
                ((end_price - start_price) / start_price) * 100
                if start_price else 0
            )
            trend_start_date = trend_data.index[0].date()
            trend_end_date = trend_data.index[-1].date()
        else:
            trend_change_pct = None
            trend_start_date = None
            trend_end_date = None

        day_high = float(latest["High"])
        day_low = float(latest["Low"])
        latest_volume = int(latest["Volume"])

        lines = [
            f"Stock: {symbol}",
            "Source: Yahoo Finance",
            f"Latest available daily bar date: {latest_date}",
            f"Latest available price: ${latest_close:,.2f} USD",
            f"Previous close: ${previous_close:,.2f} USD",
            f"Daily change: ${daily_change:+,.2f} USD "
            f"({daily_change_pct:+.2f}%)",
            f"Latest daily-bar volume: {latest_volume:,}",
            f"Daily high: ${day_high:,.2f} USD",
            f"Daily low: ${day_low:,.2f} USD",
        ]

        if average_volume is not None:
            lines.append(
                f"Average volume over {len(last_10_sessions)} "
                f"completed sessions: {average_volume:,.0f}"
            )
        else:
            lines.append("10-session average volume: Not available")

        if trend_change_pct is not None:
            lines.append(
                f"Price change from {trend_start_date} to "
                f"{trend_end_date}: {trend_change_pct:+.2f}%"
            )
        else:
            lines.append("5-session price trend: Insufficient data")

        lines.append(
            "Data note: If the market is currently open, the latest "
            "daily-bar price and volume may be incomplete."
        )
        lines.append(
            "Limitation: This data alone does not establish a reliable "
            "buy or sell signal."
        )

        return "\n".join(lines)

    except Exception as error:
        return (
            f"Unable to retrieve stock data for '{stock_symbol}'. "
            f"Error: {type(error).__name__}: {error}"
        )
