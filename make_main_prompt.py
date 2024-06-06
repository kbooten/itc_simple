import os
import json


with open('room_id2instructions.json','r') as f:
    room2instructions = json.load(f)


def build_prompt(user_input="what can I do?",room_id="", history=""):
    with open('prompt.txt','r') as f:
        prompt = f.read()
    prompt = prompt.replace("<<instructions>>",room2instructions[room_id])
    prompt = prompt.replace("<<history>>",history)
    prompt = prompt.replace("<<player_input>>",user_input)
    return prompt


def main():
    print(build_prompt())


if __name__ == '__main__':
    main()