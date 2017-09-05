from flask import Flask, render_template, jsonify, request
import datetime
from dateutil.relativedelta import *
import quandl
import numpy as np
import re
from bokeh.plotting import figure, show, output_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/background_process')
def background_process():

    try:
        ticker = request.args.get('ticker_name')
        today = str(datetime.date.today())
        last_mo = str(datetime.date.today() - relativedelta(months=1))
        quandl.ApiConfig.api_key = 'e2CzxwuQ_fxAy75oscGa'
        data = quandl.get("WIKI/{}".format(ticker.upper()), start_date=last_mo, end_date=today)
        x_axis = []
        for i in range(len(data.index)):
            m = re.search('(?<=2017-)(.*)(?=T00:00:00.000000000)', str(np.array(data.index)[i]))
            x_axis.append(m.group(0))
        y_axis = data['Adj. Close'].tolist()
        number = [a for a in range(len(data.index))]
        p = figure(title="{}".format(ticker.upper()), x_range=x_axis)
        p.line(number, y_axis, line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        output_file('{}.html'.format(ticker.upper()))
        show(p)
        return jsonify(result=None)
    except:
        return jsonify(result='Try Again')


if __name__ == "__main__":
    app.run(port=5000)

