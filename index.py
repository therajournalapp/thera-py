from flask import *
from flask_cors import CORS
import en_core_web_sm
import spacy
import asent
from string import punctuation
from collections import Counter
from heapq import nlargest
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test", methods=['GET'])
def test():
    return "hello world"


@app.route("/tags", methods=['POST'])
def tags():
    """Returns suggested tags for a document by a list of named entities and a list of keywords.
    
    Tags are returned in the form of a list of tuples where the first element is the text and the second element is the entity tag.
    Keywords are determined by taking the most common nouns, adjectives, verbs and adverbs and returning the top 5. 
    This helps to fill in suggestions when no named entities are identified.
    """
    text = request.get_json()['text']
    doc = nlp(text)
    ents = doc.ents
    
    # make tags more robust if no named entities are found
    keywords = []
    # only consider nouns, adjectives, verbs and adverbs
    for token in doc:
        if(token.is_stop or token.is_punct or token.is_space):
            continue
        if(token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'ADJ' or token.pos_ == 'VERB' or token.pos_ == 'ADV'):
            keywords.append(token.text)
    freq_word = Counter(keywords)
    freq_word.most_common(5)
    
    response = jsonify({
        "tags": [(ent.text, ent.label_) for ent in ents],
        "keywords": [w[0] for w in freq_word.most_common(5)],
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/summary", methods=['POST'])
def summary():
    """Generate a summary of the text

    If text is too short, returns the original text.
    Otherwise, returns a summary of the text.
    Credit: https://medium.com/analytics-vidhya/text-summarization-using-spacy-ca4867c6b744
    """
    doc = nlp(request.get_json()['text'])

    # only do it on more than a few sentences
    if(len(list(doc.sents)) < 5):
        response = jsonify({
            "summary": doc.text
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    keywords = []
    # only consider nouns, adjectives, verbs and adverbs
    for token in doc:
        if(token.is_stop or token.is_punct or token.is_space):
            continue
        if(token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'ADJ' or token.pos_ == 'VERB' or token.pos_ == 'ADV'):
            keywords.append(token.text)
    freq_word = Counter(keywords)
    freq_word.most_common(5)
    max_freq = freq_word.most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
                    
    summary_sentences = nlargest(3, sent_strength, key=sent_strength.get)
    final_sentences = [w.text for w in summary_sentences]
    summary = ' '.join(final_sentences)
    response = jsonify({
        "summary" : summary
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/sentiment", methods=['POST'])
def sentiment():
    """ Returns polarity scores for the text. 
    
    A negative, neutral, positive and compound score is returned.
    Compound score is a normalized score. 
    """
    # validation
    # do something

    text = request.get_json()['text']

    doc = nlp(text)
    sentiments = [s._.polarity for s in doc.sents]
    print(doc._.polarity)
    print(sentiments)
    polarities = str(doc._.polarity).split(' ')
    
    response = jsonify({
        "neg": polarities[0][4:],
        "neu": polarities[1][4:],
        "pos": polarities[2][4:],
        "compound": polarities[3][9:],
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    # change the nltk data directory
    # root = os.path.dirname(os.path.abspath(__file__))
    # on vercel serverless, you can refer to data from project root directory
    # download_dir = os.path.join('nltk_data')
    # os.chdir(download_dir)
    # nltk.data.path.append(download_dir)

    # nlp = spacy.load('en_core_web_sm')
    nlp = en_core_web_sm.load()
    nlp.add_pipe('asent_en_v1')

    # nlp.add_pipe('spacytextblob')
    app.run() # for localhost
    #app.run(host='0.0.0.0', port=8080)
