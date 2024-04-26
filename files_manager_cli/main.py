from manager import TransactionManager


def main():
    manager = TransactionManager("test.txt")
    manager.user_interface()

if __name__ == "__main__":
    main()