# Copyright (c) [2025] [huggingface/smolagents]
# Licensed under the MIT License
# Source: [https://github.com/huggingface/smolagents/blob/cfe599c54a81412ea334e1f9d1f17189772428ef/examples/multiple_tools.py]

from dria_agent.tools.tool import tool
from typing import Optional
import requests
import os


@tool
def get_weather(location: str, celsius: Optional[bool] = False) -> str:
    """
    Get the current weather at the given location using the WeatherStack API.

    Args:
        location: The location (city name).
        celsius: Whether to return the temperature in Celsius (default is False, which returns Fahrenheit).

    Returns:
        A string describing the current weather at the location.
    """
    api_key = os.environ.get(
        "WEATHERSTACK_API_KEY", None
    )  # Replace with your API key from https://weatherstack.com/
    if not api_key:
        raise EnvironmentError("WeatherStack API key not found.")
    units = "m" if celsius else "f"  # 'm' for Celsius, 'f' for Fahrenheit

    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}&units={units}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        if data.get("error"):  # Check if there's an error in the response
            return (
                f"Error: {data['error'].get('info', 'Unable to fetch weather data.')}"
            )

        weather = data["current"]["weather_descriptions"][0]
        temp = data["current"]["temperature"]
        temp_unit = "°C" if celsius else "°F"

        return f"The current weather in {location} is {weather} with a temperature of {temp} {temp_unit}."

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Converts a specified amount from one currency to another using the ExchangeRate-API.

    Args:
        amount: The amount of money to convert.
        from_currency: The currency code of the currency to convert from (e.g., 'USD').
        to_currency: The currency code of the currency to convert to (e.g., 'EUR').

    Returns:
        str: A string describing the converted amount in the target currency, or an error message if the conversion fails.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the ExchangeRate-API.
    """
    api_key = os.environ.get(
        "EXCHANGERATE_API_KEY", None
    )  # Replace with your actual API key from https://www.exchangerate-api.com/
    if not api_key:
        raise EnvironmentError("ExchangeRate-API key not found.")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        exchange_rate = data["conversion_rates"].get(to_currency)

        if not exchange_rate:
            return f"Error: Unable to find exchange rate for {from_currency} to {to_currency}."

        converted_amount = amount * exchange_rate
        return f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."

    except requests.exceptions.RequestException as e:
        return f"Error fetching conversion data: {str(e)}"


@tool
def get_news_headlines() -> str:
    """
    Fetches the top news headlines from the News API for the United States.
    This function makes a GET request to the News API to retrieve the top news headlines
    for the United States. It returns the titles and sources of the top 5 articles as a
    formatted string. If no articles are available, it returns a message indicating that
    no news is available. In case of a request error, it returns an error message.
    Returns:
        str: A string containing the top 5 news headlines and their sources, or an error message.
    """
    api_key = os.environ.get(
        "newsapi_API_KEY", None
    )  # Replace with your actual API key from https://newsapi.org/
    if not api_key:
        raise EnvironmentError("NewsAPI key not found.")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        articles = data["articles"]

        if not articles:
            return "No news available at the moment."

        headlines = [
            f"{article['title']} - {article['source']['name']}"
            for article in articles[:5]
        ]
        return "\n".join(headlines)

    except requests.exceptions.RequestException as e:
        return f"Error fetching news data: {str(e)}"


@tool
def get_joke() -> str:
    """
    Fetches a random joke from the JokeAPI.
    This function sends a GET request to the JokeAPI to retrieve a random joke.
    It handles both single jokes and two-part jokes (setup and delivery).
    If the request fails or the response does not contain a joke, an error message is returned.
    Returns:
        str: The joke as a string, or an error message if the joke could not be fetched.
    """
    url = "https://v2.jokeapi.dev/joke/Any?type=single"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if "joke" in data:
            return data["joke"]
        elif "setup" in data and "delivery" in data:
            return f"{data['setup']} - {data['delivery']}"
        else:
            return "Error: Unable to fetch joke."

    except requests.exceptions.RequestException as e:
        return f"Error fetching joke: {str(e)}"


@tool
def get_time_in_timezone(location: str) -> str:
    """
    Fetches the current time for a given location using the World Time API.
    Args:
        location: The location for which to fetch the current time, formatted as 'Region/City'.
    Returns:
        str: A string indicating the current time in the specified location, or an error message if the request fails.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    url = f"http://worldtimeapi.org/api/timezone/{location}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        current_time = data["datetime"]

        return f"The current time in {location} is {current_time}."

    except requests.exceptions.RequestException as e:
        return f"Error fetching time data: {str(e)}"


@tool
def get_random_fact() -> str:
    """
    Fetches a random fact from the "uselessfacts.jsph.pl" API.
    Returns:
        str: A string containing the random fact or an error message if the request fails.
    """
    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        return f"Random Fact: {data['text']}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching random fact: {str(e)}"


@tool
def search_wikipedia(query: str) -> str:
    """
    Fetches a summary of a Wikipedia page for a given query.
    Args:
        query: The search term to look up on Wikipedia.
    Returns:
        str: A summary of the Wikipedia page if successful, or an error message if the request fails.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        title = data["title"]
        extract = data["extract"]

        return f"Summary for {title}: {extract}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching Wikipedia data: {str(e)}"
