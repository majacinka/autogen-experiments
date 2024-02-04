import pandas as pd
import requests


def klarna_search(query):
    # Set default values for other parameters
    size = 5
    min_price = 0
    max_price = 1000000
    base_url = "https://www.klarna.com/us/shopping/public/openai/v0/products"
    params = {
        "countryCode": "US",
        "q": query,
        "size": size,
        "min_price": min_price,
        "max_price": max_price,
    }

    # Send the request and parse the response
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        products = data["products"]
        # Process the products
        rows = []
        for product in products:
            rows.append([product["name"], product["price"], product["url"], product["attributes"]])
        description = (
            "The response is a dataframe with the following columns: name, price, url, attributes. "
            "The attributes column is a list of tags. "
            "The price is in the format of $xx.xx."
        )
        return pd.DataFrame(rows, columns=["name", "price", "url", "attributes"]), description
    else:
        return None, str(response.status_code)



