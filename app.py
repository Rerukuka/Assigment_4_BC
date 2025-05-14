import streamlit as st
import requests
import ollama

def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    return requests.get(url).json()

def get_market_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    return requests.get(url).json()

def get_news(coin):
    return [f"Latest news about {coin}", f"Another update on {coin}"]

def generate_ai_response(coin, price, market_data, news_list):
    prompt = f"""Give a short summary for:
    - Coin: {coin}
    - Price: ${price}
    - Market Cap: {market_data['market_data']['market_cap']['usd']}
    - Ranking: {market_data['market_cap_rank']}
    - News: {"; ".join(news_list)}"""

    response = ollama.chat(model="llama3", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']

st.title("🤖 AI Crypto Assistant (Ollama-powered)")
coin_input = st.text_input("Enter coin name (e.g., ethereum):")

if coin_input:
    try:
        price_data = get_price(coin_input)
        market_data = get_market_data(coin_input)
        news = get_news(coin_input)

        if coin_input in price_data:
            ai_response = generate_ai_response(
                coin_input,
                price_data[coin_input]["usd"],
                market_data,
                news
            )
            st.success(ai_response)
        else:
            st.error("Invalid coin name. Try using ids like 'bitcoin', 'solana', etc.")
    except Exception as e:
        st.error(f"Error occurred: {e}")
