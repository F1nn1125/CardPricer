# CardPricer
Gets Magic The Gathering card price and name and totals in a pandas dataframe

The correct way to input multiple cards is by putting:

```[amount] [card name] [amount]```

**(Note that you can specify the amount either before or after the card name)**

Feel free to contribute and fix up things, my code is the furtherest thing from perfect! I also do not intend to make this code user-friendly to read, be ready for jank.

This is just a personal project for myself that you're free to use as well!

**PIP packages used in project:**
- Pulls latest pricing from scryfall using https://pypi.org/project/sf-price-fetcher/
- Converts Currency using https://pypi.org/project/CurrencyConverter/ library (not 100% up to date but pretty close).
