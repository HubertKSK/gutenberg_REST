import re
from collections import Counter
from urllib.request import urlopen
import difflib

from flask import Flask, jsonify
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


def download_url(url):
    with urlopen(url, timeout=3) as response:
        return response.read().decode('utf-8')


def parse_text(link):
    text = download_url(link).lower()

    start = "\*\*\* start of the project gutenberg ebook .* \*\*\*"
    text_trimmed_start = text.split(re.findall(start, text)[0], 1)[1]
    end = "\*\*\* end of the project gutenberg ebook .* \*\*\*"
    text_trimmed_all = text_trimmed_start.split(re.findall(end, text)[0], 1)[0]
    return re.findall('[A-Za-z]+', text_trimmed_all, flags=re.S)


@app.route('/count_word&<path:link>&<word>', methods=['GET'])
def count_words(link, word):
    word = word.lower()
    m = parse_text(link)
    return jsonify({word: Counter(m)[word]})


@app.route('/top10&<path:link>', methods=['GET'])
def top10(link):
    m = parse_text(link)
    return jsonify(Counter(m).most_common(10))

@app.route('/similar&<path:link>&<word>', methods=['GET'])
def similar(link, word):
    word = word.lower()
    m = parse_text(link)
    return jsonify(difflib.get_close_matches(word, set(m), 10))


if __name__ == '__main__':
    print("Starting app")
    app.run(debug=True, port=8080)
