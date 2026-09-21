import csv
from datetime import datetime
import time

LINE_UP = "\033[1A"
LINE_DOWN = "\033[1B"
LINE_CLEAR = "\x1b[2K\r"
SAVE_CURSOR = "\033[s"
RESTORE_CURSOR = "\033[u"

PROGRAM_NAME = r"""
   ))    wWw  wWw    (o)__(o)  .-.     _        .-.     
  (o0)-. (O)  (O)    (__  __)c(O_O)c  /||_    c(O_O)c   
   | (_))( \  / )      (  ) ,'.---.`,  /o_)  ,'.---.`,  
   | .-'  \ \/ /        )( / /|_|_|\ \/ |(\ / /|_|_|\ \ 
   |(      \o /        (  )| \_____/ || | ))| \_____/ | 
    \)    _/ /          )/ '. `---' .`| |// '. `---' .` 
    (    (_.'          (     `-...-'  \__/    `-...-'   
"""


def main():
    print(PROGRAM_NAME)
    print("Starting the programme......")
    while True:
        no_of_lines = 0
        print("Select an option")
        print("[1] Create tasks")
        print("[2] Mark finished tasks")
        print("[3] View tasks")
        print("[4] Delete tasks")
        print("[5] Quit")
        no_of_lines += 6
        selector = input("Enter what do you want to do : ").strip()
        no_of_lines += 1
        if selector == "1":
            line_cleaner(no_of_lines)
            task_creator()
        elif selector == "2":
            line_cleaner(no_of_lines)
            task_status_modifier()
        elif selector == "3":
            line_cleaner(no_of_lines)
            task_viewer()
        elif selector == "4":
            line_cleaner(no_of_lines)
            task_data_deleter()
        elif selector == "5":
            line_cleaner(no_of_lines)
            break
        else:
            print("Wrong input")
            time.sleep(0.4)
            no_of_lines += 1
            line_cleaner(no_of_lines)

    print("Closing the Programme.......")


def task_creator():
    print("Starting task creation...")
    no_of_lines = 0
    today = date_time_getter("date")
    with open(f"lists/{today}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        while True:
            try:
                todo = input("TODO : ")
                no_of_lines += 1
                time_now = date_time_getter("time")
                writer.writerow([time_now, todo, "created"])
            except KeyboardInterrupt:
                print(LINE_CLEAR, end="", flush=True)
                line_cleaner(no_of_lines)
                print("Exiting task creator...")
                break


def task_status_modifier():
    print("Starting task status modifier...")
    today = date_time_getter("date")
    todo_dict = {}
    temp_todo_data = {}
    available_task_no = set()
    try:
        with open(f"lists/{today}.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for no, row in enumerate(reader, start=1):
                todo_dict[no] = row
                if len(row) == 3 and row[2] == "created":
                    temp_todo_data[no] = f"[{no}] {row[1]}"
                    available_task_no.add(no)

        while True:
            no_of_lines = 0
            if len(available_task_no) == 0:
                print("No modifiable available")
                no_of_lines += 1
                time.sleep(0.3)
                break

            print("Select the TODO")
            no_of_lines += 1

            for no in available_task_no:
                print(temp_todo_data[no])
                no_of_lines += 1

            try:
                todo_no = todo_no_getter(available_task_no)
                available_task_no.remove(todo_no)
                state = status_getter()
                todo_dict[todo_no].append(date_time_getter("time"))
                todo_dict[todo_no].append(state)

            except KeyError:
                print("Wrong TODO no")
                time.sleep(0.4)
                line_cleaner(1)
            except KeyboardInterrupt:
                print(LINE_CLEAR, end="", flush=True)
                break
            else:
                line_cleaner(no_of_lines)

        with open(f"lists/{today}.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for todo_row in todo_dict.values():
                writer.writerow(todo_row)

    except FileNotFoundError:
        print("There is no TODO created today")
        time.sleep(0.4)
        line_cleaner(1)
    line_cleaner(no_of_lines)
    print("Exiting task status modifier...")


def task_viewer():
    todo_dict = {}
    today = date_time_getter("date")
    print("Starting task viewer...")
    no_of_lines = 0
    try:
        with open(f"lists/{today}.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for no, row in enumerate(reader, start=1):
                todo_dict[no] = row
                if len(row) == 3 and row[2] == "created":
                    print(f"[{no}] {row[1]} : Pending")
                    no_of_lines += 1
                elif len(row) == 5 and (
                    row[4] == "Done" or row[4] == "Moved" or row[4] == "Cancelled"
                ):
                    print(f"[{no}] {row[1]} : {row[4]}")
                    no_of_lines += 1
                else:
                    print(f"[{no}] ------N/A------")
                    no_of_lines += 1
    except FileNotFoundError:
        print("There is no TODO created today")
        time.sleep(0.4)
        line_cleaner(1)

    print("Stopping task viewer...")
    # line_cleaner(no_of_lines)


def task_data_deleter():
    print("Starting task recycler...")
    no_of_lines = 0
    today = date_time_getter("date")
    todo_dict = {}
    temp_todo_data = {}
    available_task_no = set()
    temp_todo_list = []
    try:
        with open(f"lists/{today}.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for no, row in enumerate(reader, start=1):
                todo_dict[no] = row
                if len(row) == 3 and row[2] == "created":
                    temp_todo_data[no] = f"[{no}] {row[1]} : {row[2]}"

                    available_task_no.add(no)
                elif len(row) == 5 and (
                    row[4] == "Done" or row[4] == "Moved" or row[4] == "Cancelled"
                ):
                    temp_todo_data[no] = f"[{no}] {row[1]} : {row[4]}"
                    available_task_no.add(no)

        while True:
            no_of_lines = 0
            if len(available_task_no) == 0:
                print("No tasks available to delete.")
                no_of_lines += 1
                time.sleep(0.4)
                line_cleaner(1)
                break

            print("Select the TODO")
            no_of_lines += 1

            for no in available_task_no:
                print(temp_todo_data[no])
                no_of_lines += 1

            try:
                todo_no = todo_no_getter(available_task_no)
                available_task_no.remove(todo_no)
                del_row = todo_dict.pop(todo_no)
                temp_todo_list.append(del_row)

            except KeyError:
                print("Wrong TODO no")
                time.sleep(0.4)
                line_cleaner(1)
            except KeyboardInterrupt:
                print(LINE_CLEAR, end="", flush=True)
                break
            else:
                line_cleaner(no_of_lines)

        with open(f"lists/{today}_del.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for todo_del_row in temp_todo_list:
                writer.writerow(todo_del_row)

        with open(f"lists/{today}.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for todo_row in todo_dict.values():
                writer.writerow(todo_row)

    except FileNotFoundError:
        print("There is no TODO created today")
        time.sleep(0.4)
        line_cleaner(1)
    line_cleaner(no_of_lines)
    print("Exiting task recycler...")


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
    while True:
        print("[1] Done     [2] Moved     [3] Cancelled")

        try:
            user_input = input("Enter the state of the task : ").strip()
            state_identifier = int(user_input)

            if state_identifier == 1 or state_identifier == 2 or state_identifier == 3:
                line_cleaner(2)
                return states_dict[state_identifier]
            else:
                print("wrong input")
                time.sleep(0.4)
                line_cleaner(3)

        except ValueError:
            print("Not a number")
            time.sleep(0.4)
            line_cleaner(3)


def todo_no_getter(no_set):
    no_of_lines = 0
    while True:
        try:
            no = int(input("TODO no : ").strip())
            no_of_lines += 1
            if no in no_set:
                line_cleaner(no_of_lines)
                return no
            else:
                print("Wrong No")
                time.sleep(0.4)
                line_cleaner(2)
                no_of_lines -= 1

        except ValueError:
            print("Not a number")
            time.sleep(0.4)
            line_cleaner(2)
            no_of_lines -= 1


def line_cleaner(no_of_lines_before_cursor):
    for _ in range(no_of_lines_before_cursor):
        print((LINE_UP + LINE_CLEAR), end="", flush=True)
        time.sleep(0.01)


if __name__ == "__main__":
    main()
