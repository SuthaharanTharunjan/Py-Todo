import csv
from datetime import datetime


def main():
    print("TODO list creator and manager")
    print("[1] Create tasks")
    print("[2] Mark finished tasks")
    print("[3] View tasks")
    selector = input("Enter what do you want to do : ").strip()
    if selector == "1":
        task_creator()
    elif selector == "2":
        pass
    elif selector == "3":
        pass


def task_creator():
    print("ctrl+c to exit create tasks option")
    today = date_time_getter("date")
    with open(f"lists/{today}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        while True:
            try:
                todo = input("TODO : ")
                time_now = date_time_getter("time")
                writer.writerow([time_now, todo])
            except KeyboardInterrupt:
                print("Exiting......")
                break


def date_time_getter(choice):
    if choice == "date":
        return datetime.now().date()
    elif choice == "time":
        return datetime.now().strftime("%H:%M:%S")
    elif choice == "datetime":
        return datetime.now().date(), datetime.now().strftime("%H:%M:%S")
    else:
        raise ValueError


if __name__ == "__main__":
    main()
