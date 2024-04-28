# TransactionManager Class

A class for processing data from a file of fixed-width format. 

## Attributes

- `data`: list
  - A list containing all data from the file.
- `file`: str
  - The name of the file being processed.
- `total_counter`: int
  - The counter of all records of transactions.
- `control_sum`: float
  - The control sum of all transaction amounts.
- `closed_for_changes`: list
  - A list of fields that are closed for changes.
- `commited`: bool
  - A flag indicating whether the last changes were committed.

## Methods

### `read_data(file: str)`

Read data from the given file.

### `display_header()`

Display the header of the file.

### `display_transactions(index: int = 0)`

Display the transactions data from the file.

### `add_transaction()`

Add a new transaction record to the data.

### `change_transaction(index: int)`

Change a transaction record in the data.

### `change_header(index: int)`

Change a header of a file.

### `validate_new_header_val(val, max_len, min_len = 0)`

Validate user input for the header of a file.

### `take_and_validate_amount() -> str`

Take and validate the amount for a transaction.

### `take_and_validate_currency() -> str`

Take and validate the currency for a transaction.

### `commit_changes()`

Commit the changes to the file.

### `format_counter(column: str) -> str`

Format a counter column by aligning it to the right.

### `format_amount(column: str) -> str`

Format an amount column by aligning it to the right and inserting a decimal point.

### `user_interface()`

Launch a command-line interface for interacting with the data manager.

### `interface_of_show()`

Launch a command-line interface for displaying transactions and header information.

### `interface_of_change()`

Launch a command-line interface for changing transactions and header information.

### `interface_for_close_field()`

Launch a command-line interface for closing fields for changes.
