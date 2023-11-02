import os, sys, shutil
from vault import db_path
from vault.modules.data_manager import DataManager
from termcolor import colored

class Prompt:
    def __init__(self, key):
        self.data_manager = DataManager(key)
        self.actions = {
            1: self.add_action,
            2: self.get_action,
            3: self.list_action,
            4: self.update_action,
            5: self.delete_action,
            6: self.reset_action,
            7: sys.exit
        }
        
    def get_action_prompt(self):
        print("What would you like to do?")
        print("[1] Add credential")
        print("[2] Get credential")
        print("[3] List credentials")
        print("[4] Update credential")
        print("[5] Delete credential")
        print("[6] Reset all")
        print("[7] QUIT")
        return input(">> ")
        
    def run(self, action):
        try:
            self.actions.get(int(action), self.default_action)()
        except ValueError: print(colored("Invalid action!", "red"))
        
    def default_action(self):
        print(colored("Unknown action!", "red"))
        
    def add_action(self):
        credential = { 'pairs': {}}
        platform_names = self.data_manager.get_all_names() or []
        while True:
            platform_name = input("Platform name: ")
            if platform_name not in platform_names:
                credential["platform_name"] = platform_name
                break
            else: print(colored(f"'{platform_name}' already exists!", "red"))
        
        total_pairs = int(input("How many key/value pair would you like to add? "))
        for i in range(total_pairs):
            key = input("Key: ")
            credential["pairs"][key] = input("Value: ")
        
        action = input("Save it [Y|n]? ")
        if action.lower() in ['', 'y', 'yes']:
            self.data_manager.add(credential)
            print(colored(f"'{platform_name.capitalize()}' was saved!", "green"))
        else: print(colored("Abort saving credential.", "yellow"))
        
    def get_action(self):
        credentials = self.data_manager.get_all()
        if credentials is None: return print(colored("Database is empty.", "red"))
        print(colored("Credentials:", attrs=["bold"]))
        for credential in credentials:
            print(f"-- {credential['platform_name']}")
        
        to_retrieve = input("Retrieve: ")
        for credential in credentials:
            if credential["platform_name"].lower() == to_retrieve.lower():
                print(colored(credential["platform_name"], attrs=["bold"]))
                for key, value in list(credential["pairs"].items()):
                    print(f"{key}: {value}")
                return print()
        
        print(colored(f"'{to_retrieve}' is not in the list.", "red"))
        
    def list_action(self):
        credentials = self.data_manager.get_all()
        if credentials is None: return print(colored("Database is empty.", "red"))
        for credential in credentials:
            print(colored(credential["platform_name"], attrs=["bold"]))
            for key, value in list(credential["pairs"].items()):
                print(f"{key}: {value}")
            print()
            
    def update_action(self):
        platform_names = self.data_manager.get_all_names()
        if not platform_names: return print(colored("Database is empty.", "red"))
        print(colored("Credentials", attrs=["bold"]))
        for name in platform_names:
            print(f"-- {name}")
        
        to_update = input("Update: ")
        if to_update not in platform_names: return print(colored(f"'{to_update}' is not in the list.", "red"))
        credential = self.data_manager.get_one(to_update)
        
        platform_name = credential["platform_name"]
        pairs = credential["pairs"]
        print(colored(platform_name, attrs=["bold"]))
        for key, value in list(pairs.items()):
            print(f"Old {key}: {value}")
            new_value = input(f"New {key}: ")
            pairs[key] = new_value
        
        print(f"Are you sure you want to {colored('update ' + to_update, 'blue')}")
        action = input(f"[y|n] >> ")
        if action.lower() in ['y', 'yes']:
            self.data_manager.update_one(platform_name, pairs)
            print(colored(f"'{platform_name}' was updated!", "green"))
        else: print(colored("Abort updating process.", "yellow"))
        
    def delete_action(self):
        platform_names = self.data_manager.get_all_names()
        if not platform_names: return print(colored("Database is empty.", "red"))
        print(colored("Credentials:", attrs=["bold"]))
        for name in platform_names:
            print(f"-- {name}")
        
        to_delete = input("Delete: ")
        if to_delete not in platform_names: return print(colored(f"'{to_delete}' is not in the list.", "red"))
        
        print(f"Are you sure you want to {colored('delete ' + to_delete, 'red')}?")
        action = input(f"[y|n] >> ")
        if action.lower() in ['y', 'yes']:
            self.data_manager.delete_one(to_delete)
            print(colored(f"'{to_delete}' was deleted.", "green"))
        else: print(colored("Abort deletion.", "yellow"))
        
    def reset_action(self):
        print(f"Are you sure you want to {colored('DELETE EVERYTHING', 'red')}?")
        action = input(f"[y|n] >> ")
        if action.lower() in ['y', 'yes']:
            shutil.rmtree(db_path)
            sys.exit()
        else: print(colored("Abort deletion process.", "yellow"))