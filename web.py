import os

import findspark
findspark.init()

import moz_sql_parser
from flask import Flask, render_template
from flask import request, jsonify
from moz_sql_parser import parse
from pyspark import SparkContext

from tables.tables import *


sc = SparkContext()
sc.addPyFile("./tables/__init__.py")
sc.addPyFile("./tables/html.py")
sc.addPyFile("./tables/xml.py")
sc.addPyFile("./tables/yml.py")
sc.addPyFile("./tables/tables.py")
sc.addPyFile("./tables/jshtml.py")
sc.addPyFile("./tables/json.py")
app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/console")
def console():
    return render_template("console.html")
    # return "Python Flask SparkPi server running. Add the 'sparkpi' route to this URL to invoke the app."


@app.route("/healthz")
def healthz():
    response = jsonify({"status": "ok"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/stocks")
def stocks():
    return render_template("stocks.html")
    # return "Python Flask SparkPi server running. Add the 'sparkpi' route to this URL to invoke the app."

@app.route("/price")
def price():
    return render_template("price.html")
    # return "Python Flask SparkPi server running. Add the 'sparkpi' route to this URL to invoke the app."


@app.route("/api")
def sparkpi():
    sql = str(request.args.get('api', ""))

    if sql == "":
        sql = 'select "//section/div[1]/div[2]/div/div/div/div[1]/span/span","//section/div[1]/div[2]/div/div/div/h1/text()" from html where url in (select "/html/body/div[6]/main/div[3]/section/div[1]/div/div/div/div/div/a/@href" from html where url in ("https://www.lttstore.com") and selector=xpath) and selector=xpath'
    try:
        parsed_sql = parse(sql)
        print(sql)
        table = tableclass(parsed_sql, sc)
        response = table.run(sc)
    except Exception as e:
        print(e)
        return ("Oops! Error in Query. Try again after correcting the Query")
    response=jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getweb")
def getwebpage():
    url = request.args.get('url', "")
    if url != "":
        text = requests.get(url).content
        return text


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
