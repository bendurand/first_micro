import logging
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-250909573-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', ' UA-250909573-1');
    </script>
    """

    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            pass # do something
        else:
            pass # unknown
    elif request.method == 'GET':
        return prefix_google + render_template('home.html')
    
    return prefix_google + render_template("home.html")

@app.route('/logger')
def printLogs():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return render_template('logs.html')