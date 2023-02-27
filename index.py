from flask import *
import en_core_web_sm
import spacy
# from spacytextblob.spacytextblob import SpacyTextBlob

app = Flask(__name__)


@app.route("/test", methods=['GET'])
def test():
    return "hello world"


@app.route("/tags", methods=['POST'])
def tags():
    # validation
    # credential = request.cookies.get('credential')
    # do something

    # text = request.form['text']
    text = request.args.get('text')

    ents = nlp(text).ents
    return {
        "tags": [(ent.text, ent.label_) for ent in ents]
    }


# @app.route("/sentiment", methods=['POST'])
# def sentiment():
#     # validation
#     credential = request.cookies.get('credential')
#     # do something

#     text = request.form['text']
#     processed = nlp(text)
#     return {
#         "sentiment": processed._.blob.sentiment_assessments.assessments
#     }

if __name__ == '__main__':
    # change the nltk data directory
    # root = os.path.dirname(os.path.abspath(__file__))
    # on vercel serverless, you can refer to data from project root directory
    # download_dir = os.path.join('nltk_data')
    # os.chdir(download_dir)
    # nltk.data.path.append(download_dir)

    # nlp = spacy.load('en_core_web_sm')
    nlp = en_core_web_sm.load()

    # nlp.add_pipe('spacytextblob')
    # app.run() for localhost
    app.run(host='0.0.0.0')
