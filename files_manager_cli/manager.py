class TransactionManager:
    """
    A class for processing data from a file.

    This class provides methods for reading data from a file, modifying transaction records,
    and committing changes back to the file. 
    ...

    Attributes
    ----------
    file : str
        name of a file containing transaction data 

    Methods
    -------
    read_data(file: str)
        Read data from the given file.
    show_header()
        Display the header of the file.
    show_data(index: int = 0)
        Display the data from the file.
    show_transactions(index: int = 0)
        Display the transactions from the file.
    add_transaction()
        Add a new record to the data.
    change_transaction(index: int)
        Change a transaction record in the data.
    take_and_validate_amount() -> str
        Take and validate the amount for a transaction.
    take_and_validate_currency() -> str
        Take and validate the currency for a transaction.
    commit_changes()
        Commit the changes to the file.
    format_counter(column: str) -> str
        Format a counter column by aligning it to the right.
    format_amount(column: str) -> str
        Format an amount column by aligning it to the right and inserting a decimal point.
    user_interface():
        Manage user input.
    show_transactions_interface():
        Manage user input.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the person TransactionManager.

        Parameters
        ----------
            data : List[str]
                List containing all data from file
            file : str
                Name of a file
            total_counter : int
                Counter of all records of transactions
            control_sum : int
                Control sum of all transactions amounts
            closed_for_changes : List[str]
                List for fields that are closed for changes
            commited : bool
                Check if user commited last changes 
        """
        self.data = []               
        self.file = ""               
        self.total_counter = 0           
        self.control_sum = 0         
        self.closed_for_changes = [] 
        self.commited = False           

    def read_data(self, file: str):
        """
        Read data from the specified file.

        Parameters
        ----------
        file : str
            The path to the file to be read.

        Returns
        -------
        int
            Returns 0 if the data is successfully read from the file without any issues.
            Returns 1 if an error occurs during file reading, such as file not found,
            invalid file structure, or an error while reading the file.
        """
        self.file = file 

        try:
            with open(self.file, "r") as file:
                for line in file:
                    if len(line) != 120:
                        print("Invalid file structure: not all lines are 120 symbols width")
                        return 1 
                    else:
                        self.data.append(line)

        except FileNotFoundError:
            print("File not found.")
            return 1

        except IOError as e:
            print("An error occurred while reading the file:", e)
            return 1

        else:
            if self.data[0][:2] != "01" or self.data[-1][0:2] != "03":
                print("Invalid file structure: there is no header or footer")
                return 1
            
            else:
                self.total_counter = int(self.data[-1][2:8].lstrip("0"))
                ctr_sum = self.data[-1][8:20].lstrip("0")
                if len(ctr_sum) != 0:
                    self.control_sum = float(ctr_sum[:-2] + "." + ctr_sum[-2:])
                else:
                    self.control_sum = 0.0

                self.data.pop(-1)
        
        return 0

    def show_header(self):
        """
        Display the header of the file.

        This method prints the header of the file in a formatted manner. It assumes that the data
        has already been read from the file and stored in the `data` attribute.

        If there is no data available (i.e., `data` is empty), it prints a message indicating
        that there is no data to display and returns without further action.

        The header is expected to have the following structure:
            - The first two characters represent the identifier.
            - The next 28 characters represent the name.
            - The following 30 characters represent the surname.
            - The subsequent 30 characters represent the patronymic.
            - The remaining characters represent the address.

        Returns
        -------
        None
            This method does not return any value.
        """

        if not self.data:
            print("No data available. Please read data from the file first.")
            return
        
        header = [self.data[0][:2],
                  self.data[0][2:30],
                  self.data[0][30:60],
                  self.data[0][60:90],
                  self.data[0][91:].strip('\n')]
        
        # Header sign
        print("#" * 135)
        print("#" + " " * 63 + "HEADER" + " " * 64 + "#")
        print("#" * 135)

        # Column names 
        col_names = [" ID "
                    ," " * 13 + "NAME" + " " * 13
                    ," " * 12 + "SURNAME" + " " * 13
                    ," " * 11 + "PATRONYMIC" + " " * 11
                    ," " * 12 + "ADDRESS" + " " * 12]
        for i in range(len(header)):
            print(f"#{col_names[i]}", end = "")
        print("#")

        # Header data
        print("#" * 135)
        for i in range(len(header)):
            print(f"# {header[i]} ", end = "")
        print("#")
        print("#" * 135)
        
    def show_transactions(self, index=0):
        """
        Display the data from the file.

        This method prints the data from the file in a formatted manner. It assumes that the data
        has already been read from the file and stored in the `data` attribute.

        Parameters
        ----------
        index : int, optional
            The index of the record in the data user want to see. Default is 0 and it means that 
            all records will be shown. If a non-zero index is provided, only the record at that 
            index will be displayed.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Header sign
        print("#" * 136)
        print("#" + " " * 65 + "DATA" + " " * 65 + "#")
        print("#" * 136)
        
        # Column names 
        col_names = ["ID"
                    ," " * 1 + "CNT" + " " * 2
                    ," " * 3 + "AMOUNT" + " " * 4
                    ,"CUR"
                    ," " * 44 + "RESERVED" + " " * 44]
        
        for i in range(len(col_names)):
            print(f"# {col_names[i]} ", end = "")
        print("#")
        print("#" * 136)

        if index == 0:
            start = 1
            end = len(self.data)
        else:
            start = index
            end = index + 1

        for i in range(start, end):
            line = [self.data[i][:2],
                    self.format_counter(self.data[i][2:8]),
                    self.format_amount(self.data[i][8:20]),
                    self.data[i][20:23],
                    self.data[i][23:].strip('\n')]
                    
            for i in range(len(col_names)):
                print(f"# {line[i]} ", end = "")
            print("#")
        print("#" * 136)

    def add_transaction(self):
        """
        Add a new record to the data.

        Returns
        -------
        None
            This method does not return any value.
        """

        field_id = "02"

        self.total_counter += 1
        counter = "0" * (6 - len(str(self.total_counter))) + str(self.total_counter)

        amount = self.take_and_validate_amount()

        currency = self.take_and_validate_currency()

        reserevd = " " * 96

        self.data.append(field_id + counter + amount + currency + reserevd + "\n")

    def change_transaction(self, index):
        """
        Change a transaction record in the data.

        This method modifies an existing transaction record in the data list at the specified index.
        It allows changing the amount and currency fields of the transaction, if not closed for changes.

        Parameters
        ----------
        index : int
            The index of the transaction record to be changed.

        Returns
        -------
        None
            This method does not return any value.
        """
        line = [self.data[index][:2],
                self.data[index][2:8],
                self.format_amount(self.data[index][8:20]),
                self.data[index][20:23],
                self.data[index][23:].strip('\n')]
        
        if "amount" not in self.closed_for_changes:
            print(f"OLD amount: {line[2]}")
            new_amount = self.take_and_validate_amount()

        if "currency" not in self.closed_for_changes:
            print(f"OLD currency: {line[3]}")
            new_currency = self.take_and_validate_currency()

        self.data[index] = line[0] + line[1] + new_amount + new_currency + line[4] + "\n"

    def take_and_validate_amount(self):
        """
        Take and validate the amount for a transaction.

        This method prompts the user to input an amount for a transaction and validates it.
        The amount must be a positive number, rounded to two decimal places, and not exceed
        9999999999.99. If the input is invalid, appropriate error messages are displayed,
        and the user is prompted to enter a valid amount.

        Returns
        -------
        str
            A string representing the validated and formatted amount for the transaction.
        """
        while True:
            try:
                amount = float(input("Amount: "))
                if amount <= 0:
                    print("Amount must be a positive number.")
                elif amount != round(amount, 2):
                    print("Invalid input. Please enter a valid amount.")
                elif amount > 9999999999.99:
                    print("Amount is to big")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        self.control_sum += amount
        amount = "{:.2f}".format(amount)
        amount = amount.replace(".", "")
        amount = "0" * (12 - len(amount)) + amount

        return amount

    def take_and_validate_currency(self):
        """
        Take and validate the currency for a transaction.

        This method prompts the user to input a currency code for a transaction and validates it.
        The currency code must be a three-letter code representing a valid currency.
        A list of possible currency codes is provided for reference.
        If the input is invalid, appropriate error messages are displayed, and the user is prompted
        to enter a valid currency code.

        Returns
        -------
        str
            A string representing the validated currency code for the transaction.
        """
        possible_currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD", "KRW", "SGD", "NOK",
                               "MXN", "INR", "RUB", "ZAR", "HKD", "BRL", "TRY", "IDR", "TWD", "PLN", "THB", "SAR", "AED", 
                               "CLP", "COP", "PHP", "MYR", "CZK", "ILS", "EGP", "QAR", "ARS", "HUF", "VND", "UAH", "BDT", 
                               "NGN", "PKR", "RON", "KES", "DZD", "KWD", "MAD", "IQD", "HRK", "PEN", "LKR", "OMR", "BHD", 
                               "JOD", "TND", "VND", "GTQ", "CRC", "UYU", "IRR", "DOP", "HNL", "SYP", "MUR", "XAF", "XOF", 
                               "XCD", "XPF", "ZMW", "AOA", "MZN", "GHS", "BND", "BYN", "CDF", "BWP", "CUP", "KZT", "UZS", 
                               "SBD", "TOP", "PGK", "LBP", "TTD", "SOS", "GEL", "NAD", "BBD", "NPR", "AZN", "MWK", "RSD", 
                               "SCR", "AFN", "MNT", "YER", "LSL", "BAM", "GYD", "KHR", "CVE", "NIO", "SDG", "GMD", "MKD", 
                               "MVR", "GNF", "MWK", "ETB", "MOP", "XAF", "XOF", "XPF", "XDR", "XAG", "XAU", "XPD", "XPT"]

        while True:
            currency = input("Currency: ").upper()
            if currency in possible_currencies:
                break
            else:
                print("Invalid input. Please enter a valid currency (e.g., USD, EUR, JPY).")

        return currency

    def commit_changes(self):
        """
        Commit the changes to the file.

        This method finalizes the changes made to the data and writes the updated data to the file.
        It creates the last line of the file, which includes the field identifier, counter,
        control sum, and reserved fields. The updated data is then written back to the file.

        Returns
        -------
        None
            This method does not return any value.
        """
        #create last line
        field_id = "03"
        counter = "0" * (6 - len(str(self.total_counter))) + str(self.total_counter)

        ctr_sum = "{:.2f}".format(self.control_sum)
        ctr_sum = ctr_sum.replace(".", "")
        control = "0" * (12 - len(ctr_sum)) + ctr_sum

        reserevd = " " * 100

        self.data.append(field_id + counter + control + reserevd)

        with open(self.file, "w") as file:
            file.writelines(self.data)
        
    def format_counter(self, column):
        """
        Format a counter column by aligning it to the right.

        Parameters
        ----------
        column : str
            The string representing the counter column.

        Returns
        -------
        str
            The formatted counter column, aligned to the right.
        """
        n = len(column)
        column = column.lstrip('0')
        if len(column) == 0:
            column = "0"

        n -= len(column)

        return " " * n + column
    
    def format_amount(self, column):
        """
        Format an amount column by aligning it to the right and inserting a decimal point.

        Parameters
        ----------
        column : str
            The string representing the amount column.

        Returns
        -------
        str
            The formatted amount column, aligned to the right with a decimal point.
        """
        n = len(column)
        column = column.lstrip('0')
        if len(column) == 0:
            column = "000"

        n -= len(column)
        column = column[:-2] + "." + column[-2:]

        return " " * (n) + column

    def user_interface(self):
        while True:
            print("\nOptions:")
            print("1. Show transactions")
            print("2. Add transaction")
            print("3. Change transaction")
            print("4. Commit changes")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.show_transactions_interface()
            elif choice == "2":
                self.add_transaction()
            elif choice == "3":
                index = int(input("Write transaction counter: "))

                if index > 0 and index <= self.total_counter:
                    self.change_transaction(index)
                else:
                    print()
                    print("Invalid transaction counter!")
                
            elif choice == "4":
                self.commit_changes()
            elif choice == "5":
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
    
    def show_transactions_interface(self):
        while True:
            print("\nOptions:")
            print("1. Show choosen transasction")
            print("2. Show all")
            print("3. Go back...")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                index = int(input("Write transaction counter: "))
                if index > 0 and index <= self.total_counter:
                    self.show_transactions(index=index)

                else:
                    print()
                    print("Invalid transaction counter!")

            elif choice == "2":
                self.show_transactions()
            elif choice == "3":
                print("Going back")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")
    
        