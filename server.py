import copy
import json
import openai
import pymongo

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from bson.objectid import ObjectId
from datetime import datetime


OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_KEY = ""
OPENAI_MAX_INPUT = 100
OPENAI_MAX_DIALOGUES = 3000
OPENAI_TITLE = "title"
OPENAI_CHAT = "chat"
OPENAI_TITLE_PROMPT = """
{0}

Summarize the above content within 5 words title in English, no special symbols allowed.
"""
OPENAI_CHAT_PROMPT = """
{0}

Answer the above question within 100 words in one paragraph in English, no special symbols allowed.
"""

HOST = "0.0.0.0"
SERVER_PORT = 5050
DATABASE = "chatbot-tutorial"
DATABASE_PORT = 27017
COLLECTION = "chat_history"

application = Flask(__name__)
client = pymongo.MongoClient(HOST, DATABASE_PORT)
database = client[DATABASE]
collection = database[COLLECTION]


def set_key(key):
    openai.api_key = key
    try:
        messages = [{"role": "system", "content": "You are a helpful food assistant and nutritionist."}]
        openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages
        )
        is_valid = True
    except (Exception,):
        is_valid = False
    return is_valid


def is_valid_dialogues(dialogues):
    previous_role = None
    for item in dialogues:
        if "role" not in item or "content" not in item:
            return False
        if previous_role and previous_role == item["role"]:
            return False
        previous_role = item["role"]
    if previous_role != "user":
        return False
    return True


def send(dialogues, title_chat):
    messages = copy.deepcopy(dialogues)
    if title_chat == OPENAI_TITLE:
        messages[-1]["content"] = OPENAI_TITLE_PROMPT.format(messages[-1]["content"])
    else:
        messages[-1]["content"] = OPENAI_CHAT_PROMPT.format(messages[-1]["content"])
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages
    )
    output_text = response.choices[0].message.content.strip()
    if title_chat == OPENAI_TITLE:
        return output_text
    else:
        dialogues.append({"role": "system", "content": output_text})
        return dialogues


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/<path:filename>")
def get_static(filename):
    return send_from_directory(application.static_folder, filename)


@application.route("/api/history", methods=["GET"])
def get_history():
    response = {
        "code": 0,
        "message": ""
    }
    try:
        all_documents = collection.find().sort("created", -1)
        titles = [{"chatId":  str(doc["_id"]), "title": doc["title"]} for doc in all_documents]
        response["code"] = 1
        response["message"] = "success"
        response["titles"] = titles
    except (Exception,):
        response["message"] = "output text error"
    return response


@application.route("/api/chat", methods=["GET"])
def get_chat():
    response = {
        "code": 0,
        "message": ""
    }
    if "chatId" not in request.args:
        response["message"] = "chat id missing"
        return response
    chatId = ObjectId(request.args["chatId"])
    existing_document = collection.find_one({"_id": chatId})
    if existing_document:
        chats = existing_document.get("chats", [])
        dialogues = existing_document.get("dialogues", [])
        response["code"] = 1
        response["message"] = "success"
        response["chats"] = chats
        response["dialogues"] = dialogues
    else:
        response["message"] = "invalid chat id"
    return response


@application.route("/api/chat", methods=["DELETE"])
def delete_chat():
    content = request.json
    response = {
        "code": 0,
        "message": ""
    }
    if "chatId" not in content:
        response["message"] = "chat id missing"
        return response
    chatId = ObjectId(content["chatId"])
    delete_result = collection.delete_one({"_id": chatId})
    if delete_result.deleted_count > 0:
        response["code"] = 1
        response["message"] = "success"
    else:
        response["message"] = "delete chat failed"
    return response


@application.route("/api/chat", methods=["POST"])
def send_chat():
    content = request.json
    response = {
        "code": 0,
        "message": ""
    }
    if "dialogues" not in content:
        response["message"] = "dialogues missing"
        response["dialogues"] = []
        return response
    dialogues = content["dialogues"]
    if not is_valid_dialogues(dialogues):
        response["message"] = "invalid dialogues"
        response["dialogues"] = []
        return response
    if "chatId" not in content:
        response["message"] = "chat id missing"
        response["dialogues"] = dialogues
        return response
    if len(dialogues[-1]["content"]) > OPENAI_MAX_INPUT:
        response["message"] = "input text should not exceed {0} characters".format(OPENAI_MAX_INPUT)
        response["dialogues"] = dialogues.pop()
        return response
    while len(json.dumps(dialogues)) > OPENAI_MAX_DIALOGUES:
        dialogues.pop(1)
        dialogues.pop(1)
    try:
        title = "Dialogues"
        if len(dialogues) == 1:
            dialogues.insert(0, {"role": "system", "content": "You are a helpful food assistant and nutritionist."})
            title = send(dialogues, OPENAI_TITLE)
        updated_dialogues = send(dialogues, OPENAI_CHAT)
        chatId = ObjectId(content["chatId"])
        existing_document = collection.find_one({"_id": chatId})
        if existing_document:
            existing_chats = existing_document.get("chats", [])
            updated_chats = existing_chats + updated_dialogues[-2:]
            insert_update_result = collection.update_one(
                {"_id": chatId}, {"$set": {"chats": updated_chats, "dialogues": updated_dialogues}})
        else:
            insert_update_result = collection.insert_one({
                "_id": chatId,
                "title": title,
                "chats": updated_dialogues[-2:],
                "dialogues": updated_dialogues,
                "created": datetime.now().timestamp()
            })
        if insert_update_result.acknowledged:
            response["code"] = 1
            response["dialogues"] = updated_dialogues
            response["message"] = "success"
        else:
            response["message"] = "save chat failed"
            response["dialogues"] = dialogues
    except (Exception,):
        response["message"] = "output text error"
        response["dialogues"] = dialogues
    return response


if __name__ == "__main__":
    set_key(OPENAI_KEY)
    # application.debug = True
    application.run(host=HOST, port=SERVER_PORT)
