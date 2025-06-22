import datetime
import pandas as pd
import sf_price_fetcher
from currency_converter import CurrencyConverter

# Converts the currency
def convert_currency(card_details, default_symbol):
    while True:
        symbol = input("Please input the currency's symbol"
            "you want to convert to, (e.g NZD, EUR, AUD), leave empty to skip (Currently USD): ").upper()

        # If they skip convertion then it just uses default symbol
        if symbol.strip() == "":
            symbol = default_symbol
            break

        try:
            # Throw a test convert to check if symbol exists
            CurrencyConverter().convert(1, default_symbol, symbol) 
            break

        except:
            print("Please input a valid symbol")
            continue

    # For each card in dict, convert the price.
    for key, value in card_details.items():
        converted_price = CurrencyConverter(decimal=True).convert(value, default_symbol, symbol)
        rounded_converted_price = round(converted_price, 2)

        card_details.update({key : rounded_converted_price})

    # Update and print data frame
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=[''])

    # Sum all prices and insert into data frame
    prices_list = list(card_details.values())
    total_prices = sum(prices_list)
    return total_prices, card_names_and_prices_data_frame, symbol

# It writes the dataframe to a file
def write_to_file(data_frame, total_price_string):
    # Get datetime for file name
    today = datetime.datetime.now()
    file_name_date = today.strftime("%d_%m_%Y")

    file_name = f"card_prices_{file_name_date}"
    write_to = f"{file_name}.txt"
    text_file = open(write_to, "w+")


    # Write in the data frame + total price
    text_file.write(str(data_frame))
    text_file.write(total_price_string)
    text_file.close()

    print(f"File made at: /{write_to}")

# Removes the number from card name
def extract_number_and_name(card_name, index):
    number_of_copies = card_name.split()[index]
    card_name = card_name.split()
    card_name.pop(index)
    card_name = " ".join(card_name)
    return int(number_of_copies), card_name

# Main Routine
def main():
    # Key = card's name, value = card's price
    card_details = {}

    card_amount = {}

    # Default currency
    DEFAULT_SYMBOL = 'USD'

    while True:
        while True:
            card_name = input("Card name (leave blank if done): ").lower().strip()

            if card_name == "":
                break

            number_of_copies = 1

            if card_name.split()[-1].isdigit():
                number_of_copies, card_name = extract_number_and_name(card_name, -1)

            elif card_name.split()[0].isdigit():
                number_of_copies, card_name = extract_number_and_name(card_name, 0)
                
            # Try except is after extracting because it strips out the amount from string
            try:
                # If cannot fetch card price (or if card_name != "") it will loop
                card_price = sf_price_fetcher.fetcher.get(card_name)
                break

            except sf_price_fetcher.SFException:
                print("Uhoh! It looks like your card doesn't exist, "
                    "please check your spelling and re-enter.")
                continue

        # Checks if user meant to finish
        if card_name == "":
            break

        # Checks if card is already inputted and adds more if repeat copy
        if card_name in card_amount:
            number_of_copies = int(card_amount.get(card_name)) + number_of_copies

        # update dict with name and price
        card_amount[card_name] = number_of_copies
        card_price *= number_of_copies
        
        # Format string after putting into card_amount dict otherwise it breaks
        # sometimes price_fetcher returns a string
        card_details[card_name] = float(card_price)

    # Converting Currency
    total_price, card_names_and_prices_data_frame, symbol = convert_currency(card_details, DEFAULT_SYMBOL)
    card_names_and_prices_data_frame.insert(loc=1, column=" ", value=list(card_amount.values()))

    total_price_string = f"\nTotal price: {symbol}${total_price}"

    print(card_names_and_prices_data_frame)
    print(total_price_string)

    # Writing to file
    while True:
        try:
            answer = input("Export a list of the prices? (y/n): ").lower()
            break
        except:
            print("Please enter either y or n")
            continue

    if answer == "y" or answer == "yes":
        write_to_file(card_names_and_prices_data_frame, total_price_string)

main()