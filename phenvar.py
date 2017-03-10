#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify
from datetime import datetime
from flaskext.markdown import Markdown
from visualization import generate_wordcloud, word_statistics
from database import session, RSIDCitation

application = Flask(__name__)
Markdown(application)


@application.route("/")
def index():
    home_markdown = open('markdown/home.md', 'r').read()
    return render_template('index.html', home_markdown=home_markdown)


@application.route("/results/", methods=["GET", "POST"])
def results():
    # Log user's IP address
    with open("logs/visits.log", "a") as logfile:
        log_string = "{}\t{}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.environ["REMOTE_ADDR"])
        logfile.write(log_string)
    rsid_string = request.form["rsids"].strip("rs")
    rsid_list = rsid_string.split()
    pmid_data = {}
    for rsid in rsid_list:
        pmid_data[rsid] = [str(result.pmid) for result in session.query(RSIDCitation).filter_by(rsid=int(rsid))]

    ## Comment below when changing wordcloud form
    normalization_type = request.form["normalization_type"]
    weights = {
        "default": ["word_count"],
        "rsid": ["word_count", "rsid_balance"],
        "article": ["word_count", "article_count"],
        "article_count": ["article_count"],
    }[normalization_type]

    ## Uncomment below when changing wordcloud form
    #weights = request.form.getlist('weight')
    results = generate_wordcloud(rsid_list, weights)
    if results:
        return render_template(
            'results.html',
            wordcloud_file_name=results[0],
            word_statistics=results[1],
            pmid_data=pmid_data
        )
    else:
        return render_template('results.html', wordcloud_file_name="")

@application.route("/about/")
def about():
    about_markdown = open('markdown/about.md', 'r').read()
    return render_template('about.html', about_markdown=about_markdown)

@application.route("/acknowledgements/")
def acknowledgements():
    acknowledgements_markdown = open('markdown/acknowledgements.md', 'r').read()
    return render_template('acknowledgements.html', acknowledgements_markdown=acknowledgements_markdown)

@application.route("/testtable/")
def testtable():
    testdata = word_statistics(['328'], ['article_count'])
    return render_template('word_statistics_table.html', word_statistics=testdata)


if __name__ == "main":
    application.run()

