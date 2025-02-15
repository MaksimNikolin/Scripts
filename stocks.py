import requests
import yfinance as yf
import tkinter as tk

def get_moex_stock_price(symbol):
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{symbol}.json'
    try:
        response = requests.get(url)
        data = response.json()
        if 'marketdata' in data and 'data' in data['marketdata'] and len(data['marketdata']['data']) > 0:
            price = data['marketdata']['data'][0][9]
            return price
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_yahoo_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[0]
        return None
    except Exception as e:
        print(f"Uvays")
        return None

def round_price(price):
    if price >= 10000: return price
    elif price >= 1000: return price
    elif price >= 100: return round(price, 1)
    elif price >= 10: return round(price, 2)
    else: return round(price, 3)

def get_stock_price(symbol):
    if symbol in ["AFLT", "ENPG", "IRAO", "LENT", "VKCO"]:
        return get_moex_stock_price(symbol)
    else:
        return get_yahoo_stock_price(symbol)

def format_price(price):
    if price >= 1000: return f"{price:.0f}"
    elif price >= 100: return f"{price:.1f}"
    elif price >= 10: return f"{price:.2f}"
    elif price < 10: return f"{price:.3f}"
    return str(price)

symbols = ["AFLT", "ENPG", "IRAO", "LENT", "VKCO", "META", "NTES"]
russian_symbols = ["AFLT", "ENPG", "IRAO", "LENT", "VKCO"]

root = tk.Tk()
root.title("Stocks")
num_of_symbols = len(symbols)
height = 25 * num_of_symbols + 10

root.geometry(f"150x{height}+10+500")
root.config(bg="gray")

labels = {}

for i, symbol in enumerate(symbols):
    price = get_stock_price(symbol)
    if price:
        formatted_price = format_price(price)
        if symbol in russian_symbols:
            label_text = f"{symbol}: {formatted_price} ₽"
        else:
            label_text = f"{symbol}: {formatted_price} $"
    else:
        label_text = f"{symbol}: Uvays"
    
    labels[symbol] = tk.Label(root, text=label_text, font=("Arial", 11, "bold"), bg="gray", fg="black")
    labels[symbol].pack(pady=2)

root.mainloop()



