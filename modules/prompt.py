import os
import sys
from termcolor import colored as clr
from modules.display_help import display_help
from modules.data_manager import DataManager

def error(message):
	print(clr(f'\u2716 {message}', 'red'))

def success(message):
	print(clr(f'\u2714 {message}', 'green'))

class Prompt:
	def __init__(self, master_key, credentials_path):
		self.db = DataManager(master_key, credentials_path)
		
	# Prompt loop
	def begin(self):
		actions = {
			'add key': self.add_key,
			'add multiple': self.add_multiple,
			'list keys': self.list_keys,
			'list multiples': self.list_multiples,
			'list all': self.list_all,
			'clear': lambda: os.system('clear'),
			'help': display_help,
			'quit': lambda: sys.exit()
		}
		while True:
			prompt_input = input('>> ')
			actions.get(prompt_input.strip(), lambda: error('Invalid command!'))()
		
	# Commands
	def add_key(self):
		while True:
			name = input('Where would/do you use it? (ex. Github Api Key)[name]: ')
			key = input('Key/Token: ')
			print(f"\n{clr('Are you sure?', 'magenta')}\nName: {clr(name, 'yellow')}\nKey/Token: {clr(key, 'yellow')}\n")
			save = input('[Y|n]: ')
			if save.lower() in ['', 'y']:
				self.db.insert(name, key=key)
				success(f'Succesfully saved key for {name}!')
				break
			else:
				error('Cancelled')
				break
			
	def add_multiple(self):
		while True:
			name = input('Where would/do you use it? (ex. Google)[name]: ')
			username = input('Username: ')
			password = input('Password: ')
			print(f"\n{clr('Are you sure?', 'magenta')}\nName: {clr(name, 'yellow')}\nUsername: {clr(username, 'yellow')}\nPassword: {clr(password, 'yellow')}\n")
			save = input('[Y|n]: ')
			if save.lower() in ['', 'y']:
				self.db.insert(name, multiple={ 'username': username, 'password': password })
				success(f'Succesfully saved username and password for {name}!')
				break
			else:
				error('Cancelled')
				break
			
	def list_keys(self):
		rows = self.db.select(which='keys')
		if rows:
			print(clr('Keys/Tokens', 'magenta'))
			for row in rows:
				print(f" {clr(row['name'], 'blue', attrs=['bold'])}: {clr(row['key'], 'yellow')}")
			print('')
		else:
			error('No keys has been saved yet!')
	
	def list_multiples(self):
		rows = self.db.select(which='multiples')
		if rows:
			print(clr('Username and Password', 'magenta'))
			for row in rows:
				print(clr(f" {row['name']}", 'blue', attrs=['bold']))
				print(f"  Username: {clr(row['username'], 'yellow')}")
				print(f"  Password: {clr(row['password'], 'yellow')}")
			print('')
		else:
			error('No username and password has been saved yet!')
			
	def list_all(self):
		self.list_keys()
		self.list_multiples()