import datetime
import pandas as pd
import sf_price_fetcher
from currency_converter import CurrencyConverter

DEFAULT_SYMBOL = 'USD'


def convert_currency(card_details, default_symbol):
    """returns the converted total price, the converted data frame, and the currency symbol used"""
    while True:
        symbol = input("Input the currency's symbol "
            f"you want to convert to, (e.g NZD, EUR, AUD), leave empty to skip (Currently {default_symbol}): ").strip().upper()

        # If user skips convertion, use default symbol
        if symbol == "":
            symbol = default_symbol
            break

        # Check symbol validity
        if symbol not in CurrencyConverter().currencies:
            print(f"{symbol} is not a supported currency.")
            continue

        break

    # For each card in dict, convert the price.
    for key, value in card_details.items():
        converted_price = CurrencyConverter(decimal=True).convert(value, default_symbol, symbol)
        rounded_converted_price = round(converted_price, 2)

        card_details.update({key : rounded_converted_price})

    # Update data frame
    card_names_and_prices_data_frame = pd.DataFrame.from_dict(card_details, orient='index', columns=[''])

    # Sum all prices
    prices_list = list(card_details.values())
    total_price = sum(prices_list)

    return total_price, card_names_and_prices_data_frame, symbol


def write_to_file(data_frame, total_price_string):
    """Writes the dataframe to a file"""
    today = datetime.datetime.now()
    file_name_date = today.strftime("%d_%m_%Y")

    file_name = f"card_prices_{file_name_date}.txt"
    text_file = open(file_name, "w")

    # Write in the data frame + total price
    text_file.write(str(data_frame))
    text_file.write(total_price_string)
    text_file.close()

    print(f"File created: /{file_name}")


def extract_number_and_name(card_name):
    """returns the number of copies in the card name and the card name without the number of copies"""
    try:
        if int(card_name.split()[-1]):
            number_of_copies = int(card_name.split()[-1])
            index = -1
        elif int(card_name.split()[0]):
            number_of_copies = int(card_name.split()[0])
            index = 0
    except ValueError:
        return 1, card_name

    card_name = card_name.split()
    card_name.pop(index)
    card_name = " ".join(card_name)
    return number_of_copies, card_name


def get_card_name_and_copies():
    """returns the card's name and the number of copies the user inputs"""
    card_details = {} # Key = card's name, value = card's price
    card_amount = {}

    while True:
        while True:
            card_name = input("Card name (leave blank if done): ").lower().strip()

            if card_name == '':
                break

            number_of_copies, card_name = extract_number_and_name(card_name)

            if number_of_copies <= 0:
                print(f"{number_of_copies} is an invalid amount.")
                continue

            try:
                '''
                weird quirk with the sf_price_fetcher (I'm pretty sure),
                sometimes the first api pull of a price (if it hasn't been pulled in a while I'm assuming),
                the formatting is completely messed up.
                So I always pull the price twice.
                '''
                sf_price_fetcher.fetcher.get(card_name)
                break

            except sf_price_fetcher.SFException:
                print(f"Uh-oh! It looks like the card {card_name} doesn't exist :(")
                continue

        if card_name == '':
            break

        card_price = sf_price_fetcher.fetcher.get(card_name)

        # Checks if card is already inputted and adds more if repeat copy
        if card_name in card_amount:
            number_of_copies = int(card_amount.get(card_name)) + number_of_copies

        card_amount[card_name] = number_of_copies

        # avoid floating point math errors
        card_price = int(card_price * 100)
        card_price *= number_of_copies
        card_price = float(card_price / 100)

        card_details[card_name] = card_price

    return card_details, card_amount

def main():
    """Main routine"""

    # Get user input and return card names, prices, and copy amount
    card_details, card_amount = get_card_name_and_copies()

    # Converting Currency
    total_price, card_names_and_prices_data_frame, symbol = convert_currency(card_details, DEFAULT_SYMBOL)
    card_names_and_prices_data_frame.insert(loc=1, column=" ", value=list(card_amount.values()))

    total_price_string = f"\nTotal price: {symbol}${total_price}"

    # Print final dataframe and price
    print(card_names_and_prices_data_frame)
    print(total_price_string)

    # Writing to file
    answer = input("Export a list of the prices? (y/N): ").lower()

    if answer == "y" or answer == "yes":
        write_to_file(card_names_and_prices_data_frame, total_price_string)

main()