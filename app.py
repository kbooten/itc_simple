from flask import Flask, render_template, request, jsonify
import json
import time

from llm_interface import get_llm_response
from google_sheets_io import read_rooms_from_google_sheet

from make_main_prompt import build_prompt

app = Flask(__name__)


## load basic room info
with open('room_id2room_title_author.json', 'r') as f:
    room_id2title_author = json.load(f)


room_info_for_frontend = [
    {"id": k, "title": v["title"], "author": v["author"]}
    for k, v in room_id2title_author.items()
]

@app.route('/')
#@auth.login_required
def home():
    return render_template('map.html', rooms=room_info_for_frontend)


@app.route('/select_room', methods=['POST'])
def select_room():
    room = request.form.get('room_id')
    room_title = room_id2title_author[room]["title"]
    room_author = room_id2title_author[room]["author"]
    if not room:
        return "Missing room", 400
    return render_template('chat.html', room_info={"id": room, "title": room_title, "author": room_author})


def process_history(history):
    hist_string = ""
    for h in history:
        # Log h to inspect its structure
        if isinstance(h, dict):  # Ensure h is a dictionary
            if 'user' in h and 'text' in h:  # Ensure required keys are present
                hist_string += "%s: %s\n" % (h["user"], h["text"])
            else:
                print("Warning: Missing 'user' or 'text' key in history item:", h)
        else:
            print("Warning: Unexpected item in history:", h)
    return hist_string


def process_input(user_text, room_id, history):
    try:
        llm_response = get_llm_response(build_prompt(user_text, room_id, history))
        return {"response": llm_response}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        user_input = request.form.get("message")
        room_id = request.form.get("room_id")
        history = request.form.get("history")
        
        # Attempt to parse the history JSON data
        history = json.loads(history)
        
        # Process the history into a string format
        history = process_history(history)
        if user_input.strip():
            response = process_input(user_input, room_id, history)
            #print(response)
            return jsonify({"user": "ROOM", "text": response['response']})
        else:
            return jsonify({"error": "No message received"})
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in history"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()