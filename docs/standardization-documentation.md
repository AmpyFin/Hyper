# Data Standardization Documentation

## Current Price Standard
- **Type:** float
- **Precision:** Rounded to 2 decimal places
- **Description:** All current price adapters must return the latest available price as a float rounded to 2 decimal places.

## Historical Data Standard
- **Type:** List of dictionaries (or pandas DataFrame)
- **Columns:**
  - `DateTime` (datetime)
  - `open` (float, rounded to 2 decimal places)
  - `close` (float, rounded to 2 decimal places)
  - `high` (float, rounded to 2 decimal places)
  - `low` (float, rounded to 2 decimal places)
  - `volume` (int, rounded)
- **Description:** All historical data adapters must return a list of records (or DataFrame) with the above columns. All price columns must be floats rounded to 2 decimal places, and volume must be an int.

## Implementation Notes
- Adapters should handle rounding and type conversion internally before returning data.
- If a column is missing from the source, it should be set to None or omitted.
- All adapters must use logging for errors and info, not print statements.
