import subprocess
from flask import Flask, render_template_string, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

# https://gist.github.com/JV-conseil/7063daeadf0041cb845d0ec22f8c418f

flux = {

"France Inter": "https://icecast.radiofrance.fr/franceinter-hifi.aac?id=radiofrance",
"France Culture": "https://icecast.radiofrance.fr/franceculture-hifi.aac?id=radiofrance",

"FIP": "https://icecast.radiofrance.fr/fip-hifi.aac?id=radiofrance",
"FIP Electro": "https://icecast.radiofrance.fr/fipelectro-hifi.aac?id=radiofrance",
"FIP Groove": "https://icecast.radiofrance.fr/fipgroove-hifi.aac?id=radiofrance",
"FIP Hip-Hop": "https://icecast.radiofrance.fr/fiphiphop-hifi.aac?id=radiofrance",
"FIP Jazz": "https://icecast.radiofrance.fr/fipjazz-hifi.aac?id=radiofrance",
"FIP Metal": "https://icecast.radiofrance.fr/fipmetal-hifi.aac?id=radiofrance",
"FIP Nouveautés": "https://icecast.radiofrance.fr/fipnouveautes-hifi.aac?id=radiofrance",
"FIP Pop": "https://icecast.radiofrance.fr/fippop-hifi.aac?id=radiofrance",
"FIP Reggae": "https://icecast.radiofrance.fr/fipreggae-hifi.aac?id=radiofrance",
"FIP Rock": "https://icecast.radiofrance.fr/fiprock-hifi.aac?id=radiofrance",
"FIP Sacré Français": "https://icecast.radiofrance.fr/fipsacrefrancais-hifi.aac?id=radiofrance",
"FIP World": "https://icecast.radiofrance.fr/fipworld-hifi.aac?id=radiofrance",


"France Musique": "https://icecast.radiofrance.fr/francemusique-hifi.aac?id=radiofrance",
"France Musique Baroque": "https://icecast.radiofrance.fr/francemusiquebaroque-hifi.aac?id=radiofrance",
"France Musique Classique Plus": "https://icecast.radiofrance.fr/francemusiqueclassiqueplus-hifi.aac?id=radiofrance",
"France Musique Concerts Radio France": "https://icecast.radiofrance.fr/francemusiqueconcertsradiofrance-hifi.aac?id=radiofrance",
"France Musique Easy Classique": "https://icecast.radiofrance.fr/francemusiqueeasyclassique-hifi.aac?id=radiofrance",
"France Musique Labo": "https://icecast.radiofrance.fr/francemusiquelabo-hifi.aac?id=radiofrance",
"France Musique La Contemporaine": "https://icecast.radiofrance.fr/francemusiquelacontemporaine-hifi.aac?id=radiofrance",
"France Musique La Jazz": "https://icecast.radiofrance.fr/francemusiquelajazz-hifi.aac?id=radiofrance",
"France Musique Ocora Monde": "https://icecast.radiofrance.fr/francemusiqueocoramonde-hifi.aac?id=radiofrance",


"France Musiques de films" : "https://stream.radiofrance.fr/francemusiquelabo/francemusiquelabo.m3u8?id=radiofranceBose",


}


clocks = {'1': '2025-03-07 19:30:00'}
started_clocks = []

def scheduled_task():
    current_time = datetime.now().replace(microsecond=0).isoformat(sep=" ")
    print(current_time)
    for clock in clocks:
        print(clocks[clock])
        print(current_time >= clocks[clock])
        if current_time >= clocks[clock] and clock not in started_clocks:
            kill_mpv()
            play(flux['France Inter'])
            started_clocks.append(clock)


    print(f"Scheduled task executed at {datetime.now()}")

# Initialize the scheduler
scheduler = BackgroundScheduler(job_defaults={'replace_existing': True})

scheduler.add_job(scheduled_task, 'interval', seconds=60)

# Start the scheduler
scheduler.start()




# HTML template with buttons and Bulma styling
template = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radio player</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css">

<style>
        /* Ensure that the html and body take up the full height of the viewport */
        html, body {
            height: 100%;
            margin: 0;
        }

        /* Flexbox layout to make sure footer is pushed to the bottom */
        .content {
            display: flex;
            flex-direction: column;
            min-height: 100%;
        }

        .footer {
            margin-top: auto;  /* Push footer to the bottom */
        }
    </style>

</head>
<body>
 <div class="content">
    <section class="section">
        <div class="container">
            <h1 class="title">Welcome to Radio player</h1>
            <div class="buttons">
            {% for radio in radios %}
                <a href="/play_radio/{{ radio }}" class="button is-primary {% if 'Inter' in radio %}is-danger{%endif%}"
                
                {% if 'Culture' in radio %}style = "background-color: #762b84;"{%endif%}
                {% if 'Musique' in radio %}style = "background-color: #a90042;"{%endif%}
                {% if 'FIP' in radio %}style = "background-color: #e2007a;"{%endif%}
                {% if 'Mouv' in radio %}style = "background-color: #00fb8e;"{%endif%}


                >{{ radio }}</a>
                <br>
            {% endfor %}
            </div>
                <br>
                <a href="/stop" class="button is-link is-danger">Stop</a>

        </div>
    </section>


<!-- Footer -->
    <footer class="footer has-background-dark has-text-white">
        <div class="content has-text-centered">
        <small>
            <p>
                CPU temperature: {{ cpu_temp }}<br>
                Uptime: {{ uptime }}<br>
            </p>
            </small>
        </div>
    </footer>
 </div>

</body>
</html>
"""

def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        temp = f.read()
    return f"{float(temp) / 1000:0.1f}°C"  # Convert to Celsius

def uptime():

    def decimal_to_hours_minutes(decimal_hours):
        hours = int(decimal_hours)  # Extract the whole hours
        minutes = (decimal_hours - hours) * 60  # Convert the decimal to minutes
        minutes = round(minutes)  # Round to the nearest minute

        if hours > 24:
            return f"{round(hours/24, 1)} days"
        else:
            return f"{hours} hours {minutes} min"

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_str = decimal_to_hours_minutes(uptime_seconds / 60 / 60)

    return uptime_str


@app.route('/')
def home():
    return render_template_string(template, cpu_temp=get_cpu_temp(), uptime=uptime(), radios=flux)

def play(url):
    print(f"play {url}")
    try:
        subprocess.Popen(["mpv", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("mpv is not installed or not found in the system path.")

def kill_mpv():
    print('kill mpv')
    subprocess.Popen(["killall", "mpv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@app.route('/play_radio/<radio>')
def play_radio(radio):

    print(f'play {radio}')
    play(flux[radio])

    return redirect('/')



@app.route('/stop')
def stop():
    kill_mpv()
    return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, use_reloader=False)

