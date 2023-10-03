import pandas as pd

def main():
    # Key = name, value = price
    card_details = {}

    loop = True

    while loop:
        repeats = int(input("how many cards? "))

        for i in range(repeats):
            card_name = input("Card name: ")
            card_price = float(input("Card price (USD): "))

            # update dict with name and price
            card_details.update({card_name : card_price})
        
        loop = input("More inputs? (y/n) ").lower().strip() == "y"

    # Create dataframe
    card_names_and_prices_dataframe = pd.DataFrame.from_dict(card_details, orient='index')

    print(card_names_and_prices_dataframe)

main()