import json

from google_sheets_io import read_rooms_from_google_sheet

import os


# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_rooms= os.path.join(module_dir, '/rooms/')



def build_rooms():
	room_data = read_rooms_from_google_sheet()

	room_id2room_title_author = {}

	room_id2instructions = {}

	for n,r in enumerate(room_data):
		author,title,instructions = r
		room_id = 'room'+str(n)
		room_id2room_title_author[room_id]={"title":title,"author":author}
		room_id2instructions[room_id]=instructions

	with open('room_id2room_title_author.json','w') as f:
		json.dump(room_id2room_title_author,f)

	with open('room_id2instructions.json','w') as f:
		json.dump(room_id2instructions,f)


def main():
	build_rooms()

if __name__ == '__main__':
	main()