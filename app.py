from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from scraper import IMDBSCRAPER
import pandas as pd



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('home.html')

@app.route('/results',methods=['GET', 'POST'])
def results():

    scraper = IMDBSCRAPER()
    scraper.parse()
    df= pd.DataFrame(scraper.results)
    table= df.to_html()
    df.to_csv('downloadable.csv', index=False)
    return render_template('results.html', tables=[df.to_html(classes='data')], titles=df.columns.values, row_data=list(df.values.tolist()))
    


@app.route('/download')
def download():
    return send_from_directory('', 'downloadable.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)