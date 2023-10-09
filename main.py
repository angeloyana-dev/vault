import os
from termcolor import colored as clr
from hashlib import sha256
from modules.prompt import Prompt, error, success

datas_path = 'db'
master_key_path = f'{datas_path}/master_key.txt'
credentials_path = f'{datas_path}/credentials.db'

def login():
	with open(master_key_path, 'r') as mkfile:
		master_key = mkfile.read()
	while True:
		input_master_key = input('Enter your master key: ')
		# Compare keys
		if sha256(input_master_key.encode('utf8')).hexdigest() == master_key:
			success('Master key confirmed, Welcome back!')
			break
		else:
			error('Incorrect key!')
	return input_master_key
	
def create_master_key():
	while True:
		initial_master_key = input('Create master key: ')
		confirm_master_key = input('Confirm master key: ')
		if initial_master_key == confirm_master_key:
			hashed_master_key = sha256(initial_master_key.encode('utf8')).hexdigest()
			break
		else:
			error('Input did not match!')
	# Save hashed master key for reference on login
	with open(master_key_path, 'w') as mkfile:
		mkfile.write(hashed_master_key)
	success('Succesfully saved your master key!')
	return initial_master_key
	
def main():
	if os.path.exists(master_key_path):
		master_key = login()
	else:
		master_key = create_master_key()
	# Starts prompt loop
	Prompt(master_key, credentials_path).begin()
	
if __name__ == '__main__':
	os.makedirs(datas_path, exist_ok=True)
	main()