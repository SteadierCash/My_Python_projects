class TransactionManager:
    def __init__(self, file: str):
        self.data = []
        self.file = file
        self.total_counter = 0
        self.control_sum = 0 

        self.read_data()

    def read_data(self):
            try:
                with open(self.file, "r") as file:
                    for line in file:
                      self.data.append(line)

            except FileNotFoundError:
                print("File not found.")

            except IOError as e:
                print("An error occurred while reading the file:", e)

            if self.data[0][:2] != "01" or self.data[-1][0:2] != "03":
                raise ValueError("Invalid file format")
            
            else:
                self.total_counter = int(self.data[-1][2:8].lstrip("0"))
                ctr_sum = self.data[-1][8:20].lstrip("0")
                if len(ctr_sum) != 0:
                    self.control_sum = float(ctr_sum[:-2] + "." + ctr_sum[-2:])
                else:
                    self.control_sum = 0.0

                self.data.pop(-1)

    def commit_changes(self):
            
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

    def create_transaction(self):
        field_id = "02"

        self.total_counter += 1
        counter = "0" * (6 - len(str(self.total_counter))) + str(self.total_counter)

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

        reserevd = " " * 96

        self.data.append(field_id + counter + amount + currency + reserevd + "\n")

    def change_data(self):
        pass

    def show_header(self):
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
        
    def show_transactions(self):
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

        # Header data
        for i in range(1, len(self.data)):
            line = [self.data[i][:2],
                    self.format_counter(self.data[i][2:8]),
                    self.format_amount(self.data[i][8:20]),
                    self.data[i][20:23],
                    self.data[i][23:].strip('\n')]
                    
            for i in range(len(col_names)):
                print(f"# {line[i]} ", end = "")
            print("#")
        print("#" * 136)

    def format_counter(self, column):
        n = len(column)
        column = column.lstrip('0')
        if len(column) == 0:
            column = "0"

        n -= len(column)

        return " " * n + column
    
    def format_amount(self, column):
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
            print("1. Show_transactions")
            print("2. Add transaction")
            print("3. Commit changes")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.show_transactions()
            elif choice == "2":
                self.create_transaction()
            elif choice == "3":
                self.commit_changes()
            elif choice == "4":
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
    
    def show_transactions_interface(self,):
        