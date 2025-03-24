tasks = {}

def add_task():
    print("Add a Task")
    task_name = str(input("Task name: "))
    task = str(input('Task Description: '))
    tasks[task_name] = [task, False]

def remove_task():
    print("Remove a Task")
    view_tasks()
    remove = str(input("Which task would you like to remove?: "))
    if remove in tasks:
        del tasks[remove]
    else:
        print("Task not found")

def task_complete():
    print("Completed Task?")
    view_tasks()
    task_name = str(input("Which task has been completed?: "))
    if task_name in tasks:
        tasks[task_name][1] = True
    else:
        print("Task not found")

def view_tasks():
    print("Tasks")
    print(tasks)

def main():
    finished = False
    while not finished:
        print('To-Do List Manager')
        print('1. Add a new task')
        print('2. Remove a task')
        print('3. Mark a task as completed')
        print('4. View all task')
        print('5. Exit')
        try:
            choice = int(input('Choice (1-5): '))
            match choice:
                case 1:
                    add_task()
                case 2:
                    remove_task()
                case 3:
                    task_complete()
                case 4:
                    view_tasks()
                case 5:
                    print('Thank you!!')
                    finished = True
                case _:
                    print("Invalid Input")
        except ValueError:
            print("Invalid Input")

main()

