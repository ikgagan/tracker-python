from datetime import datetime
import json
import os

tasks = []
# constant, don't edit, use .copy()
TASK_TEMPLATE = {
    "name":"",
    "due": None, # datetime
    "lastActivity": None, # datetime
    "description": "",
    "done": False # False if not done, datetime otherise
}
# don't edit, intentionaly left an unhandled exception possibility
def str_to_datetime(datetime_str):
    """ attempts to convert a string in one of two formats to a datetime
    Valid formats (visual representation): mm/dd/yy hh:mm:ss or yyyy-mm-dd hh:mm:ss """
    try:
        return datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    except:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

def save():
    """ writes the tasks list to a json file to persist changes """
    f = open("tracker.json", "w")
    f.write(json.dumps(tasks, indent=4, default=str))
    f.close()

def load(print_flag=True):
    """ loads the task list from a json file """
    if not os.path.isfile("tracker.json"):
        return
    f = open("tracker.json", "r")
    
    data = json.load(f)
    # Note about global keyword: https://stackoverflow.com/a/11867510
    global tasks
    tasks = data
    f.close()
    if print_flag:
        print(f"data {data}")    

def list_tasks(_tasks):
    """ List a summary view of all tasks """
    i = 0
    for t in _tasks:
        print(f"{i+1}) [{'x' if t['done'] else ' '}] Task: {t['name']} (Due: {t['due']})")
        i += 1
    if len(_tasks) == 0:
        print("No tasks to show")

# edits should happen below this line

def add_task(name: str, description: str, due: str):
    """ Copies the TASK_TEMPLATE and fills in the passed in data then adds the task to the tasks list """
    task = TASK_TEMPLATE.copy() # don't delete this
    # Gagan Indukala Krishna Murthy - gi36 - 15th Feb 2023
    # Summary : I used the copy function of copy module to the task dict and initialized it with values from the user input and appeneded it to the tasks list. 
    # I also performed input validation for input name or description or due from the user and also validated the proper date and time format for due by exception handling.
    # I added a print statment in the end for succesfully adding a task
    now = datetime.now()  # datetime object containing current date and time
    dt_string = now.strftime("%m/%d/%y %H:%M:%S") # mm/dd/yy H:M:S
    if name=="": # I also performed input validation for input name or description or due
        print("Adding Task rejected, please enter a valid task name")
        return
    elif description =="":
        print("Adding Task rejected, please enter a valid task description")
        return
    elif due =="":
        print("Adding Task rejected, please enter a valid task due date")
        return
    try:
        str_to_datetime(due) # Due date must match one of the formats mentioned in str_to_datetime()
    except Exception as e: # Exception handling for the unhandled cases 
        print("Task rejected due to invalid date and time format")
        return
    task["name"] = name # set the name 
    task["due"] = due # set the due date 
    task["description"] = description # set the description
    task["lastActivity"] = dt_string  # update lastActivity with the current datetime value
    task["done"] = False # False if not done, datetime otherise   
    tasks.append(task) # add the new task to the tasks list
    print("Task added successfully")  # output a message confirming the new task was added or if the addition was rejected due to missing data
    save() # make sure save() is still called last in this function

def process_update(index):
    """ extracted the user input prompts to get task data then passes it to update_task() """
    # Gagan Indukala Krishna Murthy - gi36 - 16th Feb 2023 - process_update
    # Sumamry: To start I passed index to tasks list to get the index number, later to the same I passed name, description 
    # and due to get the current name, description and due of the input index by the user.
    # To validate the index bound I added a if condition "len(tasks)-1 < index or index < 0" if the condition passes then it print a index out of bound error message
    # get the task by index - tasks[index]
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    # show the existing value of each property where the TODOs are marked in the text of the inputs (replace the TODO related text) (line 97 to 99) 
    name = input(f"What's the name of this task? Current name: {tasks[index]['name']} \n").strip()
    desc = input(f"What's a brief descriptions of this task? Current description: {tasks[index]['description']} \n").strip()
    due = input(f"When is this task due (format: m/d/y H:M:S). Current due: {tasks[index]['due']} \n").strip()
    update_task(index, name=name, description=desc, due=due)

def update_task(index: int, name: str, description:str, due: str):
    """ Updates the name, description , due date of a task found by index if an update to the property was provided """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 17th feb 2023 
    # Summary: To start with i did the validation for index out of bound scenario by writing a if condition and checking if the length of tasks-1 is less than index
    # or index is less than zero if this condition is true then the index is out of bound, I will be displaying an error message for the same. 
    # later I am call 3 if condition for name description and due to check if it not equal to a empty string, if the condition passes then i will be taking the input
    # passed from the process_update function and replacing with the existing values( which is basically updating). 
    # by using datetime class from datetime module I am taking current time in mm/dd/yy H:M:S format and overiding the current lastActivity value.
    # For the final output for success message I am using a variable is_updated which will be initially false, which I will be making true if a if condition is executed 
    # In the end if the is_updated is true then I am printing the success message else I will print the task not updated message.
    # find the task by index - tasks[index]
    is_updated = False 
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    if description != "":
        tasks[index]['description'] = description  # update incoming task data if it's provided (if it's not provided use the original task property value)
        is_updated = True
    if name != "":
        tasks[index]['name'] = name # update incoming task data if it's provided (if it's not provided use the original task property value)
        is_updated = True
    if due != "":
        tasks[index]['due'] = due # update incoming task data if it's provided (if it's not provided use the original task property value)
        is_updated = True
    now = datetime.now()  # datetime object containing current date and time
    dt_string = now.strftime("%m/%d/%y %H:%M:%S") # mm/dd/yy H:M:S
    tasks[index]['lastActivity'] = dt_string # update lastActivity with the current datetime value
    if is_updated:
        print("Task was successfully updated") # output that the task was updated if any items were changed, otherwise mention task was not updated
    else:
        print("Task was not updated because there were no changes made")# output that the task was updated if any items were changed, otherwise mention task was not updated
    save() # make sure save() is still called last in this function

def mark_done(index):
    """ Updates a single task, via index, to a done datetime"""
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 17th feb 2023 
    # find task from list by index - tasks[index]
    # Summary: First I am checking for the index out of bounds scenarios like the usual way like how I have done in the previous functions. 
    # For the main function I am using a if else condition in which I am checking if done is equal to true for the given index, if this condition passes
    # then I am marking done as true and updating the lastActivity to current datetime by using the datetime class from datetime module and formating the datetime 
    # accroding to our format required format and I am also printing the task was marked done successfully message. 
    # in the else I am printing the message Task is already completed. 
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    if tasks[index]['done'] == False:
        tasks[index]['done'] = True
        now = datetime.now()  # datetime object containing current date and time
        dt_string = now.strftime("%m/%d/%y %H:%M:%S") # mm/dd/yy H:M:S
        tasks[index]['lastActivity'] = dt_string # if it's not done, record the current datetime as the value
        print("Task was marked done successfully")  # if it is done, print a message saying it's already completed
    else:
        print("Task is already completed") 
    save() # make sure save() is still called last in this function

def view_task(index):
    """ View more info about a specific task fetch by index """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 17th feb 2023
    # Sumamry: To start with I am checking the index out of bound senarios in the usual way(like previous functions) 
    # To the empty dict task I passed key of name, due, lastActivity, description, done and their value using index.
    # Using this dict task we are printing the request for view function. 
    # find task from list by index - tasks[index]
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    task = {
    "name":tasks[index]['name'],
    "due": tasks[index]['due'],
    "lastActivity": tasks[index]['lastActivity'], 
    "description": tasks[index]['description'],
    "done": tasks[index]['done'] 
    }
    # utilize the given print statement when a task is found
    print(f""" 
        [{'x' if task['done'] else ' '}] 
        Task: {task['name']}\n 
        Description: {task['description']} \n 
        Last Activity: {task['lastActivity']} \n
        Due: {task['due']}\n
        Completed: {task['done'] if task['done'] else '-'} \n
        """.replace('  ', ' '))


def delete_task(index):
    """ deletes a task from the tasks list by index """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 17th feb 2023
    # Summary: To start with I am checking the index out of bound senarios in the usual way(like previous functions) 
    # to remove a particular task I am using remove() method - The remove() method takes a single element as an argument and removes it from the list.
    # in the end printing for calling the save() function and  I am printing a success message if the task is deleted successfully. 
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    tasks.remove(tasks[index])  # delete/remove task from list by index
    print("Task deleted successfully")# message should show if it was successful or not
    save() # make sure save() is still called last in this function

def get_incomplete_tasks():
    """ prints a list of tasks that are not done """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 19th feb 2023
    # Summary: I am calling the load() function for loading the data in to our task. 
    # later in the for loop we can checking a condition if any task doesnot have task['done'] = true then we are appending those tasking to the empty list 
    # which is __task = [] which was pre delcared in the template. 
    # that list is being passed to the list_task functions where the print statement is called for this. 
    # I am passing print_flag = False to load() function because I am using it as a condition to not print the data which is being print in the load() function
    _tasks = []
    load(print_flag=False)
    for task in tasks:
        if not task['done']: # generate a list of tasks where the task is not done
            _tasks.append(task) # pass that list into list_tasks()
    list_tasks(_tasks)

def get_overdue_tasks():
    """ prints a list of tasks that are over due completion (not done and expired) """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 19th feb 2023
    # Summary: I am using datetime class from datetime module for comparing with the due time to checking if the task is overdue or not.
    # I am calling the load() function for loading the data in to our task. 
    # later in the for loop we can checking a condition if task[done] == false and the due time is lesser the now, if this condition passes 
    # then I am appending those tasks which satify the if condition to empty list of _tasks
    # now I have the overdue data in my list _tasks, which I am passing to list_tasks. list_tasks function has a print statement which is printing the result for this function
    # I am passing print_flag = Flase to load() function because I am using it as a condition to not print the data which is being print in the load() function
    now = datetime.now()  # datetime object containing current date and time
    _tasks = []
    load(print_flag=False)
    for task in tasks:
        if task['done'] == False and str_to_datetime(task['due']) < now:  # generate a list of tasks where the due date is older than now and that are not complete
            _tasks.append(task)# pass that list into list_tasks()
    list_tasks(_tasks)

def get_time_remaining(index):
    """ outputs the number of days, hours, minutes, seconds a task has before it's overdue otherwise shows similar info for how far past due it is """
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # Gagan Indukala Krishna Murthy - gi36 - 19th feb 2023
    # Summary:To start with I am checking the index out of bound senarios in the usual way(like previous functions)
    # I am using datetime class from datetime module to get the current time so that i can use it my if else condition to get the remaining time
    # for this functions I have 3 major condition if, if else and else.
    # In the if condition I am checking two conditions. 1. done is equal to false for the given index and 
    # 2. the due date of the task for the given index is lesser than or equal to the current time. 
    # if this condition passes then I am returning a print statement in which i am stating the remaining time by 
    # subtracting the due date and time with the current date and time and showing it to the user. 
    # In the if else condition I am again checkking 2 condtions 1. done is equal to false for the given index and 
    # 2. the due date of the task for the given index is greater than the current time. 
    # if this condition passes the i am prining the overdue time by subtracting the current date and time by the due date and time
    # if both the if and if else conditions fails then the else will get executed, which is the task is already completed. 

    # get the task by index - tasks[index]
    now = datetime.now()  # datetime object containing current date and time
    if len(tasks)-1 < index or index < 0: # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print(f"Index out of bounds, please enter a index less than or equal to {len(tasks)} and greater than 0")
        return
    # display the remaining time via print in a clear format showing days, hours, minutes, seconds
    if tasks[index]['done'] == False and str_to_datetime(tasks[index]['due']) >= now: 
        print(f"The remaining time for this task is {str_to_datetime(tasks[index]['due']) - now} ") # get the days, hours, minutes, seconds between the due date and now
    # if the due date is in the past print out how many days, hours, minutes, seconds the task is over due (clearly note that it's over due, values should be positive)
    elif tasks[index]['done'] == False and str_to_datetime(tasks[index]['due']) < now:
        print(f"The task is overdue by {now - str_to_datetime(tasks[index]['due'])} ") # get the days, hours, minutes, seconds between the due date and now
    else:
        print("The task is already completed")

    task = {}

# no changes needed below this line

command_list = ["add", "view", "update", "list", "incomplete", "overdue", "delete", "remaining", "help", "quit", "exit", "done"]
def print_options():
    """ prints a readable list of commands that can be typed when prompted """
    print("Choices")
    print("add - Creates a task")
    print("update - updates a specific task")
    print("view - see more info about a task by number")
    print("list - lists tasks")
    print("incomplete - lists incomplete tasks")
    print("overdue - lists overdue tasks")
    print("delete - deletes a task by number")
    print("remaining - gets the remaining time of a task by number")
    print("done - marks a task complete by number")
    print("quit or exit - terminates the program")
    print("help - shows this list again")

def run():
    """ runs the program until terminated or a quit/exit command is used """
    print("Welcome to Task Tracker!")
    load()
    print_options()
    while(True):
        opt = input("What would you like to do?\n").strip() # strip removes whitespace from beginning/end
        if opt not in command_list:
            print("That's not a valid option")
        elif opt == "add":
            name = input("What's the name of this task?\n").strip()
            desc = input("What's a brief descriptions of this task?\n").strip()
            due = input("When is this task due (visual format: mm/dd/yy hh:mm:ss)\n").strip()
            add_task(name, desc, due)
        elif opt == "view":
            num = int(input("Which task do you want to view? (hint: number from 'list') ").strip())
            index = num-1
            view_task(index)
        elif opt == "update":
            num = int(input("Which task do you want to update? (hint: number from 'list') ").strip())
            index = num-1
            process_update(index)
        elif opt == "done":
            num = int(input("Which task do you want to complete? (hint: number from 'list') ").strip())
            index = num-1
            mark_done(index)
        elif opt == "list":
            list_tasks(tasks)
        elif opt == "incomplete":
            get_incomplete_tasks()
        elif opt == "overdue":
            get_overdue_tasks()
        elif opt == "delete":
            num = int(input("Which task do you want to delete? (hint: number from 'list') ").strip())
            index = num-1
            delete_task(index)
        elif opt == "remaining":
            num = int(input("Which task do you like to get the duration for? (hint: number from 'list') ").strip())
            index = num-1
            get_time_remaining(index)
        elif opt in ["quit", "exit"]:
            print("Good bye.")
            quit()
        elif opt == "help":
            print_options()
        
if __name__ == "__main__":
    run()

# I hope I made justice to the code :)