import csv
from datetime import datetime


def main():
    print("TODO list creator and manager")
    while True:
        print("[1] Create tasks")
        print("[2] Mark finished tasks")
        print("[3] View tasks")
        print("[4] Delete tasks")
        print("[5] Quit")
        selector = int(input("Enter what do you want to do : ").strip())
        if selector == 1:
            task_creator()
        elif selector == 2:
            task_status_modifier()
        elif selector == 3:
            task_viewer()
        elif selector == 4:
            task_data_deleter()
        elif selector == 5:
            break
        else:
            print("Wrong input")


def task_creator():
    print("ctrl+c to exit create tasks option")
    today = date_time_getter("date")
    with open(f"lists/{today}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        while True:
            try:
                todo = input("TODO : ")
                time_now = date_time_getter("time")
                writer.writerow([time_now, todo, "created"])
            except KeyboardInterrupt:
                print("Exiting......")
                break


def task_status_modifier():
    print("ctrl++c to exit marking task status")
    today = date_time_getter("date")
    todo_dict = {}
    available_task_no = set()
    try:
        with open(f"lists/{today}.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            print("Select the TODO")
            for no, row in enumerate(reader, start=1):
                todo_dict[no] = row
                if len(row) == 3 and row[2] == "created":
                    print(f"[{no}] {row[1]}")
                    available_task_no.add(no)
        while True:
            try:
                todo_no = todo_no_getter(available_task_no)
                state = status_getter()
                todo_dict[todo_no].append(date_time_getter("time"))
                todo_dict[todo_no].append(state)
            except KeyError:
                print("Wrong TODO no")
            except KeyboardInterrupt:
                print("Exiting......")
                break
        with open(f"lists/{today}.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for todo_row in todo_dict.values():
                writer.writerow(todo_row)
    except FileNotFoundError:
        print("There is no TODO created today")


def task_viewer():
    todo_dict = {}
    today = date_time_getter("date")
    print("ctrl++c to exit viewing tasks")
    try:
        with open(f"lists/{today}.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for no, row in enumerate(reader, start=1):
                todo_dict[no] = row
                if len(row) == 3 and row[2] == "created":
                    print(f"[{no}] {row[1]} : Pending")
                elif len(row) == 5 and (
                    row[4] == "Done" or row[4] == "Moved" or row[4] == "Cancelled"
                ):
                    print(f"[{no}] {row[1]} : {row[4]}")
                else:
                    print(f"[{no}] ------N/A------")
    except FileNotFoundError:
        print("There is no TODO created today")


def task_data_deleter():
    pass


def date_time_getter(choice):
    if choice == "date":
        return datetime.now().date()
    elif choice == "time":
        return datetime.now().strftime("%H:%M:%S")
    elif choice == "datetime":
        return datetime.now().date(), datetime.now().strftime("%H:%M:%S")
    else:
        raise ValueError


def status_getter():
    states_dict = {1: "Done", 2: "Moved", 3: "Cancelled"}
    print("[1] Done     [2] Moved     [3] Cancelled")
    while True:
        state_identifier = int(input("Enter the state of the task : ").strip())
        if state_identifier == 1 or state_identifier == 2 or state_identifier == 3:
            return states_dict[state_identifier]
        else:
            print("wrong input")


def todo_no_getter(no_set):
    while True:
        no = int(input("TODO no : ").strip())
        if no in no_set:
            return no
        else:
            print("Wrong No")


if __name__ == "__main__":
    main()
