from pathlib import Path
from yaml import safe_load
from threading import Thread
from controller import setup, teardown
from scheduler import create_scheduler, create_background_scheduler, run_scheduler
from datetime import datetime
from functools import partial
from flask import Flask, redirect
app = Flask(__name__)

def read_config() -> int:
    config_file = Path(__file__).parent / "config.yml"
    config = safe_load(config_file.read_text())
    return int(config["interval"])

job_interval = read_config()
job_scheduler = create_scheduler(interval=job_interval)
background_scheduler = create_background_scheduler(interval=5)

@app.route("/")
def main():
    next_exec = job_scheduler.next_run
    time_str = datetime.now()
    until = next_exec - time_str
    return f"""
<html>
    <head>
        <title>Plantebob</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1>Plantebob</h1>
        <table>
            <tr><td>Interval:</td><td>{job_interval} minutes</td></tr>
            <tr><td>Now:</td><td>{time_str}</td></tr>
            <tr><td>Next:</td><td>{next_exec} ({until})</td></tr>
        </table>
        <form action="/trigger"><input type="submit" value="Trigger" /></form>
    </body>
</html>"""

@app.route("/trigger")
def trigger():
    return redirect("/")



if __name__ == "__main__":
    setup()
    t1 = Thread(target=run_scheduler, args=(background_scheduler,), daemon=True)
    t1.start()
    t2 = Thread(target=run_scheduler, args=(job_scheduler,), daemon=True)
    t2.start()
    
    fnc = partial(app.run, host="0.0.0.0", port=8080)
    t3 = Thread(target=fnc, args=tuple(), daemon=True)
    t3.start()
    t3.join()