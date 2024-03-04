from datetime import datetime
import pandas as pd
from sf_price_fetcher import fetcher
from currency_converter import CurrencyConverter

# Converts the currency
def convert_currency(card_details, default_symbol):
    while True:
        try:
            symbol = input("Please input the currency's symbol "
                "you want to convert to, (e.g NZD, EUR, AUD), leave empty to skip: ").upper()
            
            # If they skip convertion then it just uses default symbol
            if symbol.strip() == "":
                symbol = default_symbol

            CurrencyConverter().convert(1, default_symbol, symbol) # Throw a test convert to check if symbol exists
            break
        except:
            print("Please input a valid currency symbol!")
            continue

    # For each card in the dict, it converts the currency.
    for key, value in card_details.items():
        # Convert then round the price to 2dp
        converted_price = CurrencyConverter(decimal=True).convert(value, default_symbol, symbol)
        rounded_converted_price = round(converted_price, 2)

        # Update the dictionary
        card_details.update({key : rounded_converted_price})

    # Update and print data frame
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=[''])

    # Sum all prices and insert into data frame
    prices_list = list(card_details.values())
    total_prices = sum(prices_list)
    return total_prices, card_names_and_prices_data_frame, symbol

# It writes to the file
def write_to_file(data_frame, total_price_string):
    # Get datetime for file name
    today = datetime.now()
    file_name_date = today.strftime("%d_%m_%Y")

    file_name = f"card_price_list_{file_name_date}"
    write_to = f"{file_name}.txt"
    text_file = open(write_to, "w+")

    # Write in the data frame + total price
    text_file.write(str(data_frame))
    text_file.write(total_price_string)
    text_file.close()

# Main Routine
def main():
    # Key = card's name, value = card's price
    card_amount = {}
    card_details = {}

    # Default currency
    default_symbol = 'USD'

    # Default error message
    error_message = "Please enter either y or n"

    while True:
        while True:
            try:
                card_name = input("Card name (leave blank if done): ").lower().strip()

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

        # If the card doesn't already exist it creates new item
        number_of_copies = 1

        # Checks if card is already inputted at least once and adds more if repeat copy
        if card_name in card_amount:
            number_of_copies = card_amount.get(card_name) + 1

        # update dict with name and price
        card_amount[card_name] = number_of_copies
        float(card_price)
        card_price *= number_of_copies
        
        # Format string after putting into card_amount dict otherwise it breaks
        card_details[card_name] = card_price
        # card_name = f"{card_name} {number_of_copies}"

    # Create data frame and total_price and inserts the amount of each card
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=[""])
    card_names_and_prices_data_frame.insert(loc=1, column=" ", value=list(card_amount.values()))
    
    print(card_names_and_prices_data_frame)

    # Create card_prices list
    card_prices = card_details.values()
    card_prices = [float(price) for price in card_prices]

    total_price = round(sum(card_prices), 2) if card_prices else 0.0

    # Main loop done


    # Converting Currency
    converted_symbol = "USD"
    total_price, card_names_and_prices_data_frame, converted_symbol = convert_currency(card_details, default_symbol)
    # Insert card amounts into dataframe again as they get removed by convert_currency(), there's a better way to do this but I don't have time to mull it over
    card_names_and_prices_data_frame.insert(loc=1, column=" ", value=list(card_amount.values()))
    symbol = converted_symbol

    total_price_string = f"\nTotal price: {symbol}${total_price}"

    print(card_names_and_prices_data_frame)
    print(total_price_string)

    # Writing to file
    while True:
        try:
            answer = input("Export a list of the prices? (y/n): ").lower()
            break
        except:
            print(error_message)
            continue

    if answer == "y" or answer == "yes":
        write_to_file(card_names_and_prices_data_frame, total_price_string)

main()