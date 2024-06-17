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
def write_to_file(data_frame, total_price_string, output_format='txt'):
    today = datetime.now()
    file_name_date = today.strftime("%d_%m_%Y-%H_%M")
    file_name = f"card_price_list_{file_name_date}.{output_format}"
    if output_format == "csv":
        data_frame.to_csv(file_name)
    else:
        with open(file_name, "w") as text_file:
            text_file.write(data_frame.to_string())
            text_file.write(total_price_string)

    print(f"File saved as {file_name}")

# Function to import card data from a file or pasted text
def import_card_data():
    card_details = {}
    
    while True:
        import_choice = input("Do you want to import cards from a file or paste the data? (file/paste): ").lower()
        
        if "file" in import_choice.lower() or "paste" in import_choice.lower():
            break
        else:
            print("Invalid choice. Please input 'file' or 'paste'.")

    if "file" in import_choice.lower():
        while True:
            file_path = input("Please enter the file path: ")
            try:
                with open(file_path, 'r') as file:
                    card_data = file.read()
                    break
            except FileNotFoundError:
                print("File not found. Please check the file path.")
                continue

    else:
        print("Please paste the card data (press Enter twice to finish):")
        card_data = ""
        while True:
            line = input()
            if line == "":
                break
            card_data += line + "\n"
    
    importeddata = [line.split(" ") for line in card_data.split("\n")]

    for card in importeddata:
        if card[0].startswith("#"):
            continue
        if len(card) >= 2:
            card_name = ' '.join(card[1:]).strip()
            try:
                number_of_copies = int(card[0].strip())
            except ValueError:
                print(f"Invalid number of copies for card '{card_name}'. Skipping this entry.")
                continue
            if card_name in card_details:
                card_details[card_name]['copies'] += number_of_copies
            else:
                card_details[card_name] = {'copies': number_of_copies, 'total_price': 0.0}
    
    return card_details

# Main function
def main():
    card_details = {}

    while True:
        choice = input("Do you want to enter cards manually or import? (manual/import): ").lower()
        
        if "import" in choice.lower():
            imported_card_details = import_card_data()
            if imported_card_details:
                card_details.update(imported_card_details)
            break  # Exit loop after importing
        elif "manual" in choice.lower():
            break  # Exit loop to start manual entry
        else:
            print("Invalid choice. Please input 'manual' or 'import'.")

    while True:
        if "manual" in choice.lower():
            card_name = input("Please input the card name (enter to finish): ").strip()
            if card_name == "":
                break

            try:
                card_price = fetcher.get(card_name)
            except Exception as ex:
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
        elif "import" in choice.lower():
            for card_name, card_data in list(card_details.items()):  # Create a copy of the items
                try:
                    card_price = fetcher.get(card_name)
                except Exception as ex:
                    print(f"Card lookup error: {str(ex)}")
                    continue
                
                if card_price is None:
                    print(f"No prices found for the card '{card_name}'.")
                    card_price = 0.0
                
                card_price = round(float(card_price), 2)
                card_details[card_name]['total_price'] = card_price * card_data['copies']
        break

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
            exportData = input("Export a list of the prices? (y/n): ").lower()
            if "y" in exportData or "yes" in exportData:
                while True: 
                    output_format = input("Please input the output format (txt/csv): ").lower()
                    if output_format == "txt" or output_format == "csv":
                        write_to_file(card_names_and_prices_data_frame, total_price_string, output_format)
                        break
                    else:
                        print("Invalid output format. Please input 'txt' or 'csv'.")
                break
            elif "n" in exportData or "no" in exportData:
                break
            else:
                continue
    else:
        print("No cards were added.")

if __name__ == "__main__":
    main()