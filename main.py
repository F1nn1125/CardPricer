import pandas as pd
from sf_price_fetcher import fetcher

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
            card_details.update({card_name : card_price})
        
        loop = input("More inputs? (y/n) ").lower().strip() == "y"

    # Create dataframe
    card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index')

    print("\nDisclaimer: All prices are in USD at the moment")
    print(card_names_and_prices_dataframe)

main()