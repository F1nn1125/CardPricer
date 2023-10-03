# CardPricer
Gets MTG card price and name and totals in a pandas dataframe

Pulls latest pricing from scryfall using https://pypi.org/project/sf-price-fetcher/ library and totals the cards prices.

(NOTE: Cannot take two of the same card atm as it will just replace the same one already in the dict, someone is welcome to fix this!)

Converts Currency using https://pypi.org/project/CurrencyConverter/ library (not live prices I'm pretty sure).

Feel free to contribute and fix up things, my code is the furtherest thing from perfect! I also do not intend to make this code user-friendly to read, be ready for jank.

This is just a personal project for myself that you're free to use as well!
