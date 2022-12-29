# Dear reviewer, please let me know if I created too many functions... I tried to make it as organized as I could
# since this project is kinda big :)

# Importing Libraries
import datetime

# Declaring global variables
USER_USERNAME = ""
IS_LOGGED_IN = False  # Helper variable 'is_logged_in' for loop to validate username and password.


def getting_username_dictionary():
    """Gets usernames and passwords from 'user.txt' and return them as a dictionary."""
    user_pw = {}  # Creating an empty dictionary to store a list of usernames and passwords from the file.
    usernames = []  # Empty username list.
    passwords = []  # Empty passwords list.
    # Reading usernames and password from the user.txt file and adding details to 'USER_PW' dict.
    with open("user.txt", "r") as file:
        user_data = file.readlines()
        for data in user_data:  # Looping through users and splitting to get hold of username and password.
            split_user_data = data.split(",")  # Splitting data every ",".
            # Adding usernames and passwords to previously created lists.
            usernames.append(split_user_data[0])
            stripped_pw = split_user_data[1].strip(" \n")  # Stripping spaces and new lines.
            passwords.append(stripped_pw)
        # Populating previously created dictionary with lists of usernames and passwords.
        user_pw["username"] = usernames
        user_pw.update({'password': passwords})
    return user_pw


def log_in():
    """Asks for username and password, and check if these credentials are correct.
    Returns username or displays error message."""
    global IS_LOGGED_IN  # Accessing global variable in inner scope.

    user_pw = getting_username_dictionary()
    user_username = input("Please enter your username: ")
    # If the username is correct, ask for password, if not displays appropriate message.
    if user_username in user_pw['username']:
        username_index = user_pw['username'].index(user_username)
        user_password = input("Please enter your password: ")

        # Log in if username and passwords are correct, if not displays appropriate message.
        if user_password == user_pw['password'][username_index]:
            print("You're logged in.")
            IS_LOGGED_IN = True
            return user_username
        else:
            print("Incorrect password. Try again.")
    else:
        print("Incorrect username. Try again.")


def which_menu(current_username):
    """Displays appropriate menu based on current username.
    Returns menu option chosen by user as a string."""
    # Presenting menu to the user and making sure that the user input is converted to lower case.
    # Displays additional options for 'admin'.
    if current_username == "admin":
        admin_menu = input('''Select one of the following Options below:
        r -     Registering a user
        a -     Adding a task
        va -    View all tasks
        vm -    View my task
        st -    Statistics
        gr -    Generate reports
        e -     Exit
        : ''').lower()
        return admin_menu
    else:
        user_menu = input('''Select one of the following Options below:
    r -     Registering a user
    a -     Adding a task
    va -    View all tasks
    vm -    View my task
    e -     Exit
    : ''').lower()
        return user_menu


def reg_user(current_username):
    """Enables administrator to register new user saving it to 'user.txt'."""
    user_pw = getting_username_dictionary()
    if current_username == "admin":
        # Request input of a new username.
        new_username = input("Please enter new username: ")
        if new_username in user_pw['username']:  # Checking if new user already exists.
            print("This username already exists.\n")  # Giving user feedback.
        else:  # Proceed if new user doesn't yet exist.
            # Request input of a new password.
            new_password = input("Please enter new password: ")
            # Request input of password confirmation.
            new_password_confirmation = input("Please repeat new password: ")
            # Check if the new password and confirmed password are the same.
            # Otherwise, displays a relevant message.
            if new_password == new_password_confirmation:
                new_user = f"\n{new_username}, {new_password}"
                save_new_user(new_user)  # then add them to the user.txt file.
                print(f"'{new_username}' has been registered.\n")  # Giving user feedback.
            else:
                print("Passwords don't match. Try again.")
    else:
        print("Only the Administrator is able to register new users.")


def save_new_user(text):
    """Saves new user to 'user.txt'."""
    with open('user.txt', "a") as f:
        f.write(text)


def format_date(date):
    """Receives a date as string 'DD/MM/YYYY' and returns formatted date as a string 'DD Mon YYYY'."""
    formatted_date = datetime.datetime.strptime(date, "%d/%m/%Y")  # Formatting date to the requested format.
    final_formatted_date = formatted_date.strftime('%d %b %Y')
    return final_formatted_date


def add_task():
    """Enables user to add a new task and appends it to 'tasks.txt'."""
    # Asks the username of the person whom the task is assigned to, title, description and due date of the task.
    new_task_username = input("Please enter the username this task is designed to: ")
    new_task_title = input("Please enter the title of the new task: ")
    new_task_description = input("Please enter a task description: ")
    new_task_date = input("Enter the due date for this task (DD/MM/YYYY): ")
    formatted_date = format_date(new_task_date)
    # Getting the current date using datetime.
    current_date = datetime.datetime.now()
    formatted_current_date = current_date.strftime("%d %b %Y")  # Formatting to requested format.
    new_task = f"\n{new_task_username}, {new_task_title}, {new_task_description}, {formatted_current_date}, " \
               f"{formatted_date}, No"  # Getting the task formatted to be saved on text file.
    save_new_task(new_task)  # Saving new_task to 'tasks.txt'.
    print(f"'{new_task_title}' has been added to tasks.\n")  # Giving user feedback.


def save_new_task(task_text):
    """Appends new task to 'tasks.txt'."""
    with open("tasks.txt", "a") as f:
        f.write(task_text)


def get_all_tasks():
    """Gets all tasks currently on 'tasks.txt' and return all tasks as a list."""
    with open("tasks.txt", "r") as f:
        all_tasks = f.readlines()
        return all_tasks


def view_all():
    """Prints all tasks on terminal in a user-friendly manner."""
    all_tasks = get_all_tasks()  # Getting all tasks (list) and looping through it to print on terminal.

    for task in all_tasks:
        split_task = task.split(",")  # Split line by ",".
        stripped_status = split_task[5].strip("\n")  # Stripping 'status' from '\n' to avoid unnecessary spacing.
        print(f"""
    Task {all_tasks.index(task) + 1}:           {split_task[1]}
    Assigned to:     {split_task[0]}
    Date Assigned:  {split_task[3]}
    Due Date:       {split_task[4]}
    Task Complete?  {stripped_status}
    Task Description:
     {split_task[2]}\n""")


def select_task():
    """Prompts user to select a task and returns which task was selected as int."""
    task_num = int(input("Which task would you like to select? (-1 to return to menu): ")) - 1  # Subtracting 1 since
    # lists count start from 0, and I displayed count from 1 on terminal to improve user experience.
    return task_num


def overwrite_tasks(new_text_list):
    """Receives the complete new text to be written on 'tasks.txt' and overwrites the file with new text."""
    with open("tasks.txt", "w") as f:
        for task in new_text_list:
            f.write(task)


def mark_task_as_complete(task_num, user_tasks):
    """Receives all tasks for a user and the index of the task which is to be marked as complete. Finds the chosen
    tasks among all currently available tasks and replaces status as 'Yes'. T
    hen overrides all tasks to text file to save changes."""
    all_tasks = get_all_tasks()  # Getting all tasks as a list and looping through.
    for task in all_tasks:
        if task == user_tasks[task_num]:  # Finding chosen tasks among all tasks.
            if all_tasks.index(task) == len(all_tasks) - 1:  # Checking if the task is the last one on the
                # file (the last status won't have '\n').
                # Replacing current status for 'Yes'.
                all_tasks[all_tasks.index(task)] = all_tasks[all_tasks.index(task)].replace(" No", "Yes\n")
            else:
                all_tasks[all_tasks.index(task)] = all_tasks[all_tasks.index(task)].replace("No\n", "Yes\n")
            overwrite_tasks(all_tasks)  # Saving changes. P.S. I couldn't figure out other way of altering a string
            # and saving it on file other than overwriting everything.


def change_task_username(task_num, user_tasks):
    """Receives all tasks from a user and the index of the task which they want to change.
    Prompt to user to enter new username. Finds the desired tasks among all tasks and alter
    the username and overwrites all tasks to save it to file."""
    all_tasks = get_all_tasks()  # Getting all tasks and looping through.
    new_user = input("Enter new user assigned to this task: ")  # Getting new user from user.
    for task in all_tasks:
        if task == user_tasks[task_num]:  # Getting chosen task among all tasks.
            split_task = task.split(", ")  # Splitting chosen task to get access to current username
            # and changing it to new user.
            all_tasks[all_tasks.index(task)] = all_tasks[all_tasks.index(task)].replace(split_task[0], new_user)
            overwrite_tasks(all_tasks)  # Saving changes to 'tasks.txt'.


def change_due_date(task_num, user_tasks):
    """Receives all tasks from a user and the index of the task which they want to change.
    Prompt to user to enter new due date as DD/MM/YYYY. Finds the desired tasks among all tasks and alter
    the due date and overwrites all tasks to save it to file."""
    all_tasks = get_all_tasks()  # Getting all tasks.
    new_due_date = input("Enter new due date for this task (DD/MM/YYYY): ")  # Getting new date from user.
    formatted_new_due_date = format_date(new_due_date)  # Formatting new date to desired format.
    for task in all_tasks:  # Looping through all tasks.
        if task == user_tasks[task_num]:  # Finding the desired task.
            split_task = task.split(", ")  # Splitting desired task to get hold of current date.
            all_tasks[all_tasks.index(task)] = all_tasks[all_tasks.index(task)].replace \
                (split_task[4], formatted_new_due_date)  # Replacing old date by new one.
            print(f"Due date has been altered to {formatted_new_due_date}.")  # Giving user feedback.
            overwrite_tasks(all_tasks)  # Saving changes.


def edit_chosen_task(task_num, user_tasks):
    sub_menu = input('''Select one of the following Options below:
        mc -    Mark task as complete
        ed -    Edit task
        : ''').lower()
    if sub_menu == "mc":
        mark_task_as_complete(task_num, user_tasks)

    elif sub_menu == "ed":
        editing_menu = input('''Select one of the following Options below:
        un -    Change username whom the task is designed to.
        dd -    Change due date of the task.
        : ''').lower()
        if editing_menu == "un":
            change_task_username(task_num, user_tasks)

        elif editing_menu == "dd":
            change_due_date(task_num, user_tasks)

        else:
            print("You chose an invalid option.")


def get_user_tasks(current_username):
    """Gets all tasks for a specific user and returns them as a list."""
    all_tasks = get_all_tasks()  # Getting all current tasks.
    my_tasks = []  # Declaring empty list to hold user's tasks.

    for task in all_tasks:  # Looping through all tasks to get user's tasks and append it to 'my_tasks'.
        split_task = task.split(",")  # Split line by "," to get hold of username.
        if split_task[0] == current_username:  # Selecting only tasks for this specific user.
            my_tasks.append(task)
    return my_tasks


def view_mine(current_username):
    """Prints all tasks for current user in a user-friendly format."""
    my_tasks = get_user_tasks(current_username)  # Getting all tasks for specific user and looping through them.

    for task in my_tasks:
        split_task = task.split(",")  # Split line by "," to get hold of details. Added index to each task
        # (added 1 to make it more user-friendly).
        print(f"""
    Task {my_tasks.index(task) + 1}:           {split_task[1]}
    Assigned to:     {split_task[0]}
    Date Assigned:  {split_task[3]}
    Due Date:       {split_task[4]}
    Task Complete?  {split_task[5]}
    Task Description:
     {split_task[2]}\n""")

    selected_task_index = select_task()  # Asking if user would like to select a task.
    if selected_task_index > -1:  # If user's input is > -1 continue, else returns to menu.
        split_current_task = my_tasks[selected_task_index].split(",")  # Splitting current task to access status.
        current_task_status = split_current_task[5].strip("\n")  # Stripping status from '\n' and " ".
        stripped_current_status = current_task_status.strip(" ")
        if selected_task_index != -1 and stripped_current_status == "No":  # Checking if tasks is incomplete so
            # user is able to edit it, else displaying appropriate message.
            edit_chosen_task(selected_task_index, my_tasks)
        else:
            print("You can't edit a completed task.")


def get_all_users():
    """Gets all users currently on 'user.txt' and return all users as a list."""
    with open("user.txt", "r") as f:  # Reading from 'users.txt'.
        users = f.readlines()
        return users


def statistics():
    """Displays current statistics on terminal in a user-friendly format."""
    generate_reports()  # Generating all reports with current data.
    with open("task_overview.txt", "r") as f:  # Reading from "task_overview.txt".
        task_overview = f.read()
        print(task_overview)  # Printing content.
    with open("user_overview.txt", "r") as f:  # Reading from "user_overview.txt".
        user_overview = f.read()
        print(user_overview)  # Printing content.


def check_if_overdue(task):
    """Receives a task as a string. Returns True if task is overdue, else returns False."""
    split_task = task.split(",")  # Splitting task to get hold of due date.
    today_date = datetime.date.today()  # Getting current date.
    task_due_date = split_task[4]  # Getting due date and transforming it to datetime object.
    task_due_date_datetime = datetime.datetime.strptime(task_due_date[1:], "%d %b %Y").date()
    if today_date > task_due_date_datetime:  # Checking if today's date is bigger than due date.
        return True
    else:
        return False


def get_complete_tasks(tasks):
    """Receives a list of tasks and returns number of completed tasks."""
    total_complete_tasks = 0  # Declaring counter.
    for task in tasks:  # Looping through tasks.
        if "Yes" in task:  # If the tasks contains "Yes", adds 1 to counter.
            total_complete_tasks += 1
    return total_complete_tasks


def get_uncompleted_tasks(tasks):
    """Receives a list of tasks and returns number of uncompleted tasks."""
    total_uncompleted_tasks = 0  # Declaring counter.
    for task in tasks:  # Looping through tasks.
        if "No" in task:  # If the tasks contains "No", adds 1 to counter.
            total_uncompleted_tasks += 1
    return total_uncompleted_tasks


def create_task_overview():
    """Creates a report containing all details about currently available tasks, and writes it on 'task_overview.txt'."""
    all_tasks = get_all_tasks()  # Getting all tasks.
    total_tasks = len(all_tasks)  # Getting total number of tasks.
    total_complete_tasks = get_complete_tasks(all_tasks)  # Getting number of completed tasks.
    total_incomplete_tasks = get_uncompleted_tasks(all_tasks)  # Getting number of uncompleted tasks.
    total_overdue_tasks = 0  # Counter to get overdue and uncompleted tasks.
    for task in all_tasks:  # Looping through all tasks.
        if check_if_overdue(task):  # Checking if ask is overdue and uncompleted. Then adding 1 to counter.
            if "No" in task:
                total_overdue_tasks += 1
    # Writing report to 'task_overview.txt'.
    with open("task_overview.txt", "w") as f:
        f.write(f"""
Tasks that have been generated and 
tracked using Task Manager:         {total_tasks}
Completed tasks:                    {total_complete_tasks}
Uncompleted tasks:                  {total_incomplete_tasks}
Overdue uncompleted tasks:          {total_overdue_tasks}
Incomplete tasks (%):               {round(((total_incomplete_tasks / total_tasks) * 100), 2)}%
Overdue tasks (%):                  {round(((total_overdue_tasks / total_tasks) * 100), 2)}%""")


def initiate_user_overview():
    """Creates header on 'user_overview.txt'."""
    with open("user_overview.txt", "w") as f:
        f.write(f"""
Total users:                                    {len(get_all_users())}
Tasks that have been generated and 
tracked using Task Manager:                     {len(get_all_tasks())}
""")


def get_overdue_task_count(username):
    """Receives a username and returns number of overdue uncompleted tasks for user."""
    is_overdue = 0  # Declaring counter.
    all_user_tasks = get_user_tasks(username)  # Getting all tasks for this user and looping through them.
    for task in all_user_tasks:
        if check_if_overdue(task):  # Checking if task is overdue and uncompleted.
            if "No" in task:
                is_overdue += 1  # Adding 1 to counter.
    return is_overdue


def create_user_overview():
    """Creates a report about all details for each user, and appends it to 'user_overview.txt'."""
    all_users = get_all_users()  # Getting all current users.
    all_tasks = get_all_tasks()  # Getting all current tasks.
    initiate_user_overview()  # Writes header for user_overview.

    for user_details in all_users:  # Looping through all users.
        split_user_details = user_details.split(", ")  # Splitting user_details to get hold of username.
        # Getting number of complete tasks.
        user_complete_tasks = get_complete_tasks(get_user_tasks(split_user_details[0]))
        # Getting number of uncompleted tasks.
        user_uncompleted_tasks = get_uncompleted_tasks(get_user_tasks(split_user_details[0]))
        user_tasks = get_user_tasks(split_user_details[0])  # Getting all quests for current user.
        number_user_tasks = len(user_tasks)
        if number_user_tasks == 0:  # Adding condition to cover if user has zero tasks.
            number_user_tasks = 1
        # Getting number of overdue and uncompleted tasks for user.
        total_user_overdue_tasks = get_overdue_task_count(split_user_details[0])
        # Creating user_overview in a user-friendly format.
        user_report = f"""
Total tasks for {split_user_details[0]}:                          {len(user_tasks)}
Tasks assigned for {split_user_details[0]} (%):                   {round(((len(user_tasks) / len(all_tasks)) * 100),2)}%
Tasks completed:                                {user_complete_tasks}
Tasks yet to be completed:                      {user_uncompleted_tasks}
Tasks incomplete and overdue:                   {round(((total_user_overdue_tasks / number_user_tasks) * 100), 2)}%
"""

        with open("user_overview.txt", "a") as f:  # Saving user_overview.
            f.write(user_report)


def generate_reports():
    """Generates task_overview and user_overview."""
    create_task_overview()
    create_user_overview()
    print("Reports have been generated.")  # Giving user feedback.


# Login section
while not IS_LOGGED_IN:
    USER_USERNAME = log_in()

# Task Manager.
while True:
    # Displays menu to user.
    menu = which_menu(USER_USERNAME)

    # Adds a new user to the user.txt file, only if user is 'admin'.
    if menu == 'r':
        reg_user(USER_USERNAME)

    # Allows user to add a new task to task.txt file.
    elif menu == 'a':
        add_task()

    # Reading tasks from task.txt file and printing formatted task as required.
    elif menu == 'va':
        view_all()

    # Reading tasks from task.txt file and printing formatted task as requested (specific for user).
    elif menu == 'vm':
        view_mine(USER_USERNAME)

    # Displays statistics about users and tasks ('admin' only).
    elif menu == "st":
        statistics()

    # Generates user and tasks reports ('admin' only').
    elif menu == "gr":
        generate_reports()

    # Exits the program.
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # Displays appropriate message if user selects wrong option.
    else:
        print("You have made a wrong choice. Please Try again.")
