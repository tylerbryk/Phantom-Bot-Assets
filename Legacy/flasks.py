from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')

def main():
	return "Bot online!"

def run():
    app.run(host="0.0.0.0", port=8080)

def start_server():
    server = Thread(target=run)
    server.start()