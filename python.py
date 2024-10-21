import os
import time
import requests
from flask import Flask, jsonify, render_template
from threading import Timer

app = Flask(__name__)

class MainApp:
    def __init__(self):
        self.data = []
        self.interval = None

    def regular_count(self):
        active = self.do_checks()
        new_data = []
        for b in self.data:
            if b['uid'] == active:
                b['count'] += 5
                if b['count'] >= 100:
                    # reset and trigger action
                    b['count'] = 0
                    response = requests.get(f"https://maker.ifttt.com/trigger/{b['action']}/with/key/{os.getenv('REACT_APP_IFTTT_KEY')}")
                    print(response)
            else:
                b['count'] -= 2.5
                if b['count'] < 0:
                    b['count'] = 0
            new_data.append(b)

        self.data = new_data

    def start_timer(self):
        self.interval = Timer(0.25, self.regular_count)
        self.interval.start()

    def stop_timer(self):
        if self.interval:
            self.interval.cancel()

    def do_checks(self):
        # Placeholder for context and environment logic
        # Simulate checking coordinates and matching with environment settings
        return -1

    def fetch_data(self):
        response = requests.get(os.getenv('REACT_APP_CONFIG'))
        self.data = response.json()

    def component_will_unmount(self):
        self.stop_timer()

    def component_did_mount(self):
        self.fetch_data()
        self.start_timer()


@app.route('/')
def index():
    app_instance = MainApp()
    app_instance.component_did_mount()
    return render_template('index.html', data=app_instance.data)


if __name__ == "__main__":
    app.run(debug=True)
