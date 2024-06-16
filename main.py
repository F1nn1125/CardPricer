import pandas as pd
from datetime import datetime
from sf_price_fetcher import fetcher
from currency_converter import CurrencyConverter

# Default currency
DEFAULT_SYMBOL = 'USD'

# Converts the currency
def convert_currency(card_details):
    while True:
        symbol = input(
            "Please input the currency's symbol you want to convert to (e.g. NZD, EUR, AUD) (enter to skip): ").upper()
        
        if symbol.strip() == "":
            symbol = DEFAULT_SYMBOL
        
        try:
            CurrencyConverter().convert(1, symbol)  # Test conversion to check if symbol exists
            break
        except ValueError:
            print("Please input a valid currency symbol!")

    # Convert currency for each card in the dictionary
    for key, value in card_details.items():
        converted_price = CurrencyConverter(decimal=True).convert(value['total_price'], symbol)
        rounded_converted_price = round(converted_price, 2)
        card_details[key]['total_price'] = rounded_converted_price

    # Create DataFrame from updated card details
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=['total_price', 'copies'])
    card_names_and_prices_data_frame.rename(columns={'total_price': 'Price', 'copies': 'Copies'}, inplace=True)
    
    # Sum all prices
    total_prices = sum(item['Price'] for item in card_names_and_prices_data_frame.to_dict('records'))
    return total_prices, card_names_and_prices_data_frame, symbol

# It writes to the file
def write_to_file(data_frame, total_price_string):
    today = datetime.now()
    file_name_date = today.strftime("%d_%m_%Y")
    file_name = f"card_price_list_{file_name_date}.txt"

    with open(file_name, "w") as text_file:
        text_file.write(data_frame.to_string())
        text_file.write(total_price_string)
    print(f"File saved as {file_name}")

# Main function
def main():
    card_details = {}

    while True:
        card_name = input("Please input card name (enter to continue): ")
        if not card_name:
            break
        
        try:
            card_price = fetcher.get(card_name)
        except Exception as ex:
            if 'invalid card name' in str(ex).lower():
                print("Invalid card name.")
                continue
            elif 'failed to establish a new connection' in str(ex).lower():
                print("Internet connectivity error.")
                continue
            else:
                print(f"Card lookup error: {str(ex)}")
                continue
            
        if card_price is None:
            print("No prices found for the card.")
            continue
        
        while True:
            try:
                number_of_copies = int(input("Please input number of copies: "))
                break
            except ValueError:
                print("Please input a valid number.")
        
        card_price = round(float(card_price), 2)
        if card_name in card_details:
            card_details[card_name]['total_price'] += card_price * number_of_copies
            card_details[card_name]['copies'] += number_of_copies
        else:
            card_details[card_name] = {
                'total_price': card_price * number_of_copies,
                'copies': number_of_copies
            }

    if card_details:
        card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=['total_price', 'copies'])
        card_names_and_prices_data_frame.rename(columns={'total_price': 'Price', 'copies': 'Copies'}, inplace=True)

        print(card_names_and_prices_data_frame)

        total_price = round(sum(item['total_price'] for item in card_details.values()), 2)
        
        total_price, card_names_and_prices_data_frame, symbol = convert_currency(card_details)
        
        total_price_string = f"\nTotal price: {symbol} ${total_price}"

        print(card_names_and_prices_data_frame)
        print(total_price_string)

        while True:
            answer = input("Export a list of the prices? (y/n): ").lower()
            if answer in {"y", "yes"}:
                write_to_file(card_names_and_prices_data_frame, total_price_string)
                break
            elif answer in {"n", "no"}:
                break
            else:
                continue
    else:
        print("No cards were added.")

if __name__ == "__main__":
    main()