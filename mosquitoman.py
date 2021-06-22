from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Sleep is temporary, the pasta is now"

def run():
  app.run(host='0.0.0.0',port=8080)

def ping():
    t = Thread(target=run)
    t.start()