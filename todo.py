import os
from colorama import Fore, Back, Style

def retrieve():
    infile = open("tasks.txt", 'r')
    data = (infile.read()).splitlines()
    tasks_dict = {}
    for i in range(0,len(data)):
        data[i] = data[i].split(":")
        tasks_dict[data[i][0]] = data[i][1]
    infile.close()
    sorted_list = sorted(tasks_dict.items(), key=lambda x: int(x[1].split("-")[0]), reverse=True)
    tasks_dict.clear()
    for item in sorted_list:
        tasks_dict[item[0]] = item[1]
    return tasks_dict

def update(new_tasks):
    infile = open("tasks.txt", "w")
    infile.truncate(0)
    for task, importance in new_tasks.items():
        infile.write(f"{task}:{importance}\n")
    infile.close()

def add(task): 
    importance = input("Priority> ")
    if not importance.isdigit():
        print("Only numeric values are allowed")
        add(task)
    elif int(importance) > 10:
        print("priority shoudn't exceed 10")
        add(task)
    else:
        tasks = retrieve()
        pos = 0
        tasks[task] = str(importance) + "-0"
        update(tasks)

def delete(task):
    tasks = retrieve()
    if task == "all":
        tasks.clear()
    elif task.isdigit():
        i = 0
        task_to_delete = ""
        for k in tasks.keys():
            if i == int(task):
                task_to_delete = k
            i += 1
        if task_to_delete in tasks:
            tasks.pop(task_to_delete)
        else:
            print("Task not found!!")
            return
    else:
        print("invalid input!!")
        return
    update(tasks)
    print("Task deleted successfully! ")

def printer(task, importance, count):
    status = int(importance[1])
    if status:
        box_len = len(task) + 31
    else:
        box_len = len(task) + 34
    if int(importance[0]) >= 10:
        box_len += 1
    statement = "┏" + "━"*box_len + "┓" + "\n" + "┃   " + str(count) + "   "
    if(status):
        statement +=  Fore.GREEN + Style.BRIGHT + task + Fore.WHITE + Style.NORMAL
        statement += "   "
        statement += "DONE"
    else:
        statement +=  Fore.YELLOW + Style.BRIGHT + task + Fore.WHITE + Style.NORMAL
        statement += "   "
        statement += "PENDING"
    statement += "   Priority: " + importance[0] + "   ┃" + "\n" + "┗" + "━"*box_len + "┛"
    print(statement)

def list(priority):
    tasks = retrieve()
    i = 0
    for task, importance in tasks.items():
        importance = importance.split("-")
        if priority == "all":
            printer(task, importance, i)
        elif priority == "done":
            if importance[1] == '1':
                printer(task, importance, i)
        elif priority == "pending":
            if importance[1] == '0':
                printer(task, importance, i) 
        else:
            if importance[0] == str(priority):
                printer(task, importance, i)
        i += 1

def verify(task):
    tasks = retrieve()
    count = 0
    for key in tasks:
        if count == int(task):
            return key
        count += 1
    return 0

def edit(task):
    verified = verify(task)
    if verified == 0:
        print("Task not added")
        return
    tasks = retrieve()
    status = int(tasks[verified].split("-")[1])
    priority = int(tasks[verified].split("-")[0])
    if status:
        box_length = len(verified) + 15
    else:
        box_length = len(verified) + 17
    importance = tasks[verified].split("-")
    printer(verified, importance, 0)
    new_status = input("Set Status> ")
    if new_status != status and new_status == "0" or new_status == "1":
        tasks[verified] = importance[0] + f"-{new_status}"
    update(tasks)
    print("status changed successfully ")

def main(): 
    os.system("CLS")
    list("all")
    while True:
        command = input("ToDo> ")
        if(command == "add"):
            task = input("Task> ")
            add(task)
            print("Task added successfully! ")
        elif(command == "delete"):
            task = input("Task> ")
            delete(task)
        elif(command == "show"):
            priority = input("Priority> ")
            os.system("CLS")
            list(priority)
        elif(command == "clear"):
            os.system("CLS")
        elif(command == "edit"):
            task = input("Task> ")
            if task.isdigit():
                edit(int(task))
            else:
                print("invalid input")
        elif(command == "help"):
            print("'add'    ->  to add a new task")
            print("'show'   ->  enter priority or enter 'all' to show all tasks")
            print("'delete' ->  enter the index of the task to delete or enter 'all' to delete all of them")
            print("'edit'   ->  enter the index of the task to edit its status")
            print("'clear'  ->  to clear command window")
            print("'stop'   ->  to exit")
        elif(command == "stop"):
            exit(0)

main()
