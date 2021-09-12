from flask import Flask, render_template, request
import requests
import math

millnames = ['',' Thousand',' Million',' Billion',' Trillion']


def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        ticker = request.form['ticker']
        key = 'D4hI0zbZW_yaHsRdDe5ql6n3e107JVxz'
        url = f"https://api.polygon.io/v1/meta/symbols/{ticker}/company?apiKey={key}"
        response = requests.get(url)
        if(response):
            json_resp = response.json()
            name = json_resp['name']
            sector = json_resp['sector']
            industry = json_resp['industry']
            ceo = json_resp['ceo']
            desc = json_resp['description']
            m_cap = millify(float(json_resp['marketcap']))
            url = f"https://api.polygon.io/v2/reference/news?limit=10&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte=2021-04-26&apiKey={key}"
            response = requests.get(url)
            try:
                json_resp = response.json()['results']
                article_1 = json_resp[0]
                article_2 = json_resp[1]
                article_1_title = article_1['title']
                article_1_url = article_1['article_url']
                article_2_title = article_2['title']
                article_2_url = article_2['article_url']
                return render_template("results.html",
                                        TickerName = ticker,
                                        name=name,
                                        sector=sector,
                                        industry=industry,
                                        ceo=ceo,
                                        m_cap=m_cap,
                                        relevant_news="Relevant News",
                                        url_1=article_1_url,
                                        url_2=article_2_url,
                                        title_1=article_1_title,
                                        title_2=article_2_title)
            except:
                return render_template("results.html",
                                        TickerName = ticker,
                                        name=name,
                                        sector=sector,
                                        industry=industry,
                                        relevant_news="No relevant news found.",
                                        ceo=ceo,
                                        m_cap=m_cap)
        else:
            return render_template("error.html",wrongTicker=ticker)
    return render_template('index.html')



if __name__ == '__main__':
   app.run()
