import os, getpass
from termcolor import colored
from hashlib import sha256
from vault import master_key_path
from vault.modules.prompt import Prompt

def create_key():
    print("You're new here, please create your master key to begin.")
    while True:
        initial_key = getpass.getpass("Create master key: ")
        confirm_key = getpass.getpass("Confirm master key: ")
        if initial_key == confirm_key: break
        else: print(colored("Key input did not match.", "red"))
        
    hashed_key = sha256(initial_key.encode()).hexdigest()
    with open(master_key_path, 'w') as file:
        file.write(hashed_key)
    print(colored("Master key confirmed!", "green"))
    return initial_key
    
def get_key():
    with open(master_key_path) as file:
        master_key = file.read()
        
    print("Welcome back!")
    while True:
        input_key = getpass.getpass("Enter your master key: ")
        if sha256(input_key.encode()).hexdigest() == master_key: break
        else: print(colored("Incorrect master key!", "red"))
    
    print(colored("Master key confirmed!", "green"))
    return input_key
    
def main():
    if os.path.exists(master_key_path): master_key = get_key()
    else: master_key = create_key()
    
    prompt = Prompt(master_key)
    # Actions prompt loop
    while True:
        action = prompt.get_action_prompt()
        prompt.run(action)
    
if __name__ == "__main__":
    main()