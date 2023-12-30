import pandas as pd
from sf_price_fetcher import fetcher
from currency_converter import CurrencyConverter

# Converts the currency
def convert_currency(card_details, default_symbol):
    symbol = input("Please input the currency's symbol you want to convert to, (e.g NZD, EUR, AUD): ")

    # For each card in the dict, it converts the currency.
    for key, value in card_details.items():

        # Convert then round the price to 2dp
        converted_price = CurrencyConverter(decimal=True).convert(value, default_symbol, symbol)

        # Update the dictionary
        card_details.update({key : round(converted_price, 2)})

    # Update and print dataframe
    card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index', columns=[''])

    # Sum all prices and insert into dataframe
    return sum(list(card_details.values())), card_names_and_prices_dataframe, symbol

# Main Routine
def main():
    # Key = card's name, value = card's price
    card_details = {}

    repeat_copies = 1

    # Default currency
    default_symbol = 'USD'

    while True:
        while True:
            card_name = input("Card name (leave blank if done): ").lower()

            try:
                # If cannot fetch card price (or if card_name != "") it will loop
                if card_name != "":
                    card_price = fetcher.get(card_name)
                break
            except:
                print("Uhoh! It looks like your card doesn't exist, please check your spelling and re-enter.")
                continue

        # Checks if user meant to break loop
        if card_name == "":
            break

        # Checks if card is already inputted at least once
        if card_name in card_details:
            repeat_copies += 1
            card_name = f"{card_name} ({repeat_copies})"

        # update dict with name and price
        float(card_price)
        card_details.update({card_name : card_price})

    # Create dataframe and total_price
    card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index', columns=[''])
    total_price = round(sum(card_details.values()), 2)

    # Main loop done

    convert = input("Convert currency? (y/n): ").lower().strip() == "y"

    if convert:
        total_price, card_names_and_prices_dataframe, converted_symbol = convert_currency(card_details, default_symbol)
        symbol = converted_symbol
    
    else:
        symbol = default_symbol

    print(card_names_and_prices_dataframe)
    print(f"Total price of cards: {symbol}${total_price}\n")

main()