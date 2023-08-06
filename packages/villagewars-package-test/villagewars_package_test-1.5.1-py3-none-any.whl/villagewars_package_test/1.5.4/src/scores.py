from flask import Flask
import shelve
import pyperclip
app = Flask(__name__)

@app.route('/')
def html():
    users = shelve.open('database/data')
    final = '''<!DOCTYPEhtml>
<html>
    <head>
        <title>Scores - VillageWars</title>
    </head>
    <body>
        <script>

// TODO: Add this code.

        </script>
        <h1>VillageWars</h1>
        <h2 style="color:blue">Scores</h2>
'''

    for username in users.keys():
        final += '<h3>' + username + '''</h3>
<h4>Victories: %s</h4>
<h4>Games finished: %s</h4>
<h4>Total Kills: %s</h4>
<h4>Color: %s</h4>
<br>''' % (users[username]['victories'], users[username]['games finished'], users[username]['kills'], users[username]['color'])
    final += '''
    </body>
</html>'''
    return final

app.run()
pyperclip.copy('http://127.0.0.1:5000/')
