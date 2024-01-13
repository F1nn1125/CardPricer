from datetime import datetime
import pandas as pd
from sf_price_fetcher import fetcher
from currency_converter import CurrencyConverter

# Get date for file_name
today = datetime.now()

day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Converts the currency
def convert_currency(card_details, default_symbol):
    while True:
        try:
            symbol = input("Please input the currency's symbol "
                "you want to convert to, (e.g NZD, EUR, AUD): ").upper()

            CurrencyConverter().convert(
                1,
                default_symbol,
                symbol) # Throw a test convert to check if symbol exists
            
            break
        except:
            print("Please input a valid currency symbol!")
            continue

    # For each card in the dict, it converts the currency.
    for key, value in card_details.items():
        # Convert then round the price to 2dp
        converted_price = CurrencyConverter(decimal=True).convert(value, default_symbol, symbol)

        # Update the dictionary
        card_details.update({key : round(converted_price, 2)})

    # Update and print data frame
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(
        card_details,
        orient='index',
        columns=[''])

    # Sum all prices and insert into data frame
    return sum(list(card_details.values())), card_names_and_prices_data_frame, symbol

# It writes to the file
def write_to_file(data_frame, total_price_string):
    file_name = f"card_price_list_{day}_{month}_{year}"
    write_to = f"{file_name}.txt"
    text_file = open(write_to, "w+")
    text_file.write(f"{file_name}\n\n")

    # Write in the data frame + total price
    text_file.write(str(data_frame))
    text_file.write(total_price_string)

    # Close the text_file
    text_file.close()

# Main Routine
def main():
    # Key = card's name, value = card's price
    card_details = {}
    repeat_copies = 1

    # Default currency
    default_symbol = 'USD'

    # Default error message
    error_message = "Please enter either y or n"

    while True:
        while True:
            try:
                card_name = input("Card name (leave blank if done): ").lower()

                # If cannot fetch card price (or if card_name != "") it will loop
                if card_name != "":
                    card_price = fetcher.get(card_name)

                break
            except:
                print("Uhoh! It looks like your card doesn't exist, "
                    "please check your spelling and re-enter.")
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

    # Create data frame and total_price
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(
        card_details,
        orient='index',
        columns=[''])
    
    print(card_names_and_prices_data_frame)

    # Create card_prices list
    card_prices = card_details.values()
    list(card_prices)

    total_price = round(sum(card_prices), 2)

    # Main loop done

    symbol = default_symbol

    while True:
        try:
            convert = input("Convert currency? (y/n): ").lower()
            break
        except:
            print(error_message)
            continue

    if convert == "y" or convert == "yes":
        total_price, card_names_and_prices_data_frame, converted_symbol = convert_currency(
            card_details,
            default_symbol)

        symbol = converted_symbol

    total_price_string = f"\nTotal price of cards: {symbol}${total_price}"

    print(card_names_and_prices_data_frame)
    print(total_price_string)

    # Writing to file stuff
    while True:
        try:
            answer = input("Do you want to export a list of the prices? (y/n): ").lower()
            break
        except:
            print(error_message)
            continue

    if answer == "y" or answer == "yes":
        write_to_file(
            card_names_and_prices_data_frame,
            total_price_string)

main()