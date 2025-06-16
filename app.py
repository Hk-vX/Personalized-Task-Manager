import streamlit as st
import os
import datetime

# File naming helper
def get_file(username):
    return f"{username} task.txt"

def get_status_file(username):
    return f"{username} TASK.txt"

# Core logic
def save_user_data(username, password, name, address, age):
    filename = get_file(username)
    with open(filename, 'a') as f:
        f.write(password + "\n")
        f.write(f"Name: {name}\nAddress: {address}\nAge: {age}\n")

def verify_login(username, password):
    try:
        with open(get_file(username), 'r') as f:
            stored_password = f.readlines()[0].strip()
        return password == stored_password
    except:
        return False

def add_tasks(username, tasks):
    with open(get_file(username), 'a') as f:
        for i, (task, target) in enumerate(tasks, 1):
            f.write(f"TASK {i}: {task}\nTARGET {i}: {target}\n")

def update_task_status(username, completed, ongoing, not_started):
    with open(get_status_file(username), 'a') as f:
        f.write(str(datetime.datetime.now()) + "\n")
        f.write("COMPLETED TASK\n" + completed + "\n")
        f.write("ONGOING TASK\n" + ongoing + "\n")
        f.write("NOT YET STARTED\n" + not_started + "\n")

def read_user_data(username):
    with open(get_file(username), 'r') as f:
        return f.read()

def read_task_status(username):
    try:
        with open(get_status_file(username), 'r') as f:
            return f.read()
    except:
        return "No status updates yet."


# Streamlit UI
st.title("📋 Task Manager")

option = st.sidebar.radio("Choose Action", ["Sign Up", "Login"])

if option == "Sign Up":
    st.subheader("Create a new account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    name = st.text_input("Full Name")
    address = st.text_input("Address")
    age = st.number_input("Age", min_value=0, max_value=100, step=1)

    if st.button("Sign Up"):
        if os.path.exists(get_file(username)):
            st.warning("Username already exists.")
        else:
            save_user_data(username, password, name, address, str(age))
            st.success("Sign-up successful! Please log in.")

elif option == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if verify_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Incorrect username or password.")

# Show features after login
if st.session_state.get("logged_in"):
    st.header(f"Welcome, {st.session_state.username}")
    action = st.selectbox("Select an action", ["View Profile", "Add Task", "Update Task", "View Task Status"])

    if action == "View Profile":
        st.text(read_user_data(st.session_state.username))

    elif action == "Add Task":
        n = st.number_input("How many tasks?", min_value=1, step=1)
        task_inputs = []
        for i in range(n):
            task = st.text_input(f"Task {i+1}", key=f"task_{i}")
            target = st.text_input(f"Target {i+1}", key=f"target_{i}")
            task_inputs.append((task, target))
        if st.button("Save Tasks"):
            add_tasks(st.session_state.username, task_inputs)
            st.success("Tasks added successfully!")

    elif action == "Update Task":
        completed = st.text_area("Completed Tasks")
        ongoing = st.text_area("Ongoing Tasks")
        not_started = st.text_area("Not Started Tasks")
        if st.button("Update Status"):
            update_task_status(st.session_state.username, completed, ongoing, not_started)
            st.success("Status updated!")

    elif action == "View Task Status":
        st.text(read_task_status(st.session_state.username))
