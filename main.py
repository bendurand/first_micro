import logging
import requests
import matplotlib.pyplot as plt
import base64

from io import BytesIO
#from googleapiclient.discovery import build
#from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request
from pytrends.request import TrendReq


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

@app.route('/cookies')
def cookies():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a250909573w345029243p281176908")
    return req.text

@app.route('/logger')
def printLogs():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return render_template('logs.html')


# OAUTH part

"""
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'json/data-sources-deta-5cc0c71b7dba.json' # Stored in local
VIEW_ID = '281176908'


def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
        }]
      }
  ).execute()


def get_visitors(response):
  visitors = 0 # in case there are no analytics available yet
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dateRangeValues = row.get('metrics', [])

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          visitors = value

  return str(visitors)


@app.route('/oauth')
def oauth():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    visitors = get_visitors(response)
    return render_template('oauth.html', visitors=str(visitors))
"""

# Pytrends

@app.route('/trend')
def trend_plot():
    # Get the trend data using pytrends
    pytrends = TrendReq()
    kw_list = ['geneve']
    pytrends.build_payload(kw_list=kw_list, timeframe='today 5-y')
    trend_data = pytrends.interest_over_time()

    # Create a line chart using Matplotlib
    plt.plot(trend_data['geneve'])
    plt.xlabel('Date')
    plt.ylabel('Trend')

    # Save the chart to a PNG file
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the chart in base64
    chart_url = base64.b64encode(buf.getvalue()).decode()
    plt.clf()

    # Render the chart in an HTML template
    return render_template('trend_plot.html', chart_url=chart_url)