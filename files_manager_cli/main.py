from manager import TransactionManager


def main():
    manager = TransactionManager()
    while True:
        file = input("File: ")
        res = manager.read_data(file)
        if res == 0:
            break    
    manager.user_interface()
    print("#"  *120)

if __name__ == "__main__":
    main()