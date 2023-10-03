import pandas as pd
from sf_price_fetcher import fetcher
from currency_converter import CurrencyConverter

def main():
    # Key = name, value = price
    card_details = {}

    loop = True

    while loop:
        repeats = int(input("how many cards? "))

        for i in range(repeats):
            while True:
                card_name = input("Card name: ").lower()

                try:
                    # If cannot fetch card price it will loop
                    card_price = fetcher.get(card_name)
                    break
                except:
                    print("Uhoh! It looks like your card doesn't exist! Please check your spelling and re-enter.")
                    continue

            # update dict with name and price
            float(card_price)
            card_details.update({card_name : card_price})
        
        loop = input("More inputs? (y/n) ").lower().strip() == "y"

    # Create dataframe
    card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index')

    # Sum all prices and insert into dataframe
    total_price = round(sum(card_details.values()), 2)

    print("\nDisclaimer: All prices are in USD at the moment")
    print(card_names_and_prices_dataframe)
    print(f"Total price of cards: {total_price}")

    # Main loop done

    convert = input("Convert currency? (y/n) ").lower().strip() == "y"

    if convert:
        symbol = input("Please input the currency's symbol you want to convert to, (e.g NZD, EUR, AUD): ")

        for key, value in card_details.items():

            # Convert then round the price to 2dp
            converted_price = CurrencyConverter(decimal=True).convert(value, 'USD', symbol)

            # Update the dictionary
            card_details.update({key : round(converted_price, 2)})

        print("Disclaimer: Currencies might not be fully up to date/live prices")
        # Update and print dataframe
        card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index')
        print(card_names_and_prices_dataframe)

        # Sum all prices and insert into dataframe
        total_price = sum(card_details.values())
        print(f"Total price of cards: {total_price}\n")


main()