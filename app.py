# -*- coding: utf-8 -*-
"""app.py"""

import json
import re
from collections import Counter
from flask import Flask, render_template, request


# ---------------- LOAD DATASET ----------------
with open("generated_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Dataset loaded:", len(data))


# ---------------- FUNCTIONS ----------------
def normalize(word):
    word = word.lower()
    word = re.sub(r'(.)\1+', r'\1\1', word)
    return word


def clean_sentence(sentence):
    return re.sub(r'[^\w\s]', '', sentence)


# ---------------- DICTIONARIES ----------------
english_dict = set([
"i","you","we","cancelled","they","he","she","it","this","that","these","those",
"is","am","are","was","were","be","been","being",
"have","has","had","do","does","did",
"will","would","shall","attend","should","can","could","may","might",
"and","or","but","because","so","if","then",
"what","why","when","where","who","how",
"my","your","his","her","their","our",
"me","him","them","us",
"hello","hi","hey","bro","dude","ok","okay","fine","good","bad","nice",
"yes","no","maybe","sure","please","thanks","sorry",
"class","college","school","teacher","sir","madam",
"project","assignment","exam","test","result","marks",
"meeting","call","message","reply","text","chat",
"code","coding","bug","error","fix","debug","run","execute",
"system","app","software","data","model","output","input",
"today","tomorrow","yesterday","now","later","soon",
"time","day","night","morning","evening",
"work","task","job","plan","idea","problem","solution",
"start","stop","continue","complete","finish","cancel",
"come","go","give","take","make","use","try",
"fast","slow","easy","hard","important","urgent",
"happy","sad","angry","tired","excited","confused",
"lol","haha","omg","wow","dip","bro","sis","friend","family","people","guys","sisters","sister"
])

hindi_dict = set([
"arey","bhai","yaar","kya","ka","ki","ke",
"hai","ho","tha","thi","the","hoga","hogi",
"nahi","mat","haan","acha","theek","sahi","galat",
"main","tu","tum","aap","hum","woh","yeh",
"mera","teri","uska","hamara","tumhara",
"mujhe","tujhe","usse","hume","tumhe",
"kal","aaj","abhi","baad","pehle","phir",
"kyun","kaise","kab","kahan","kaun",
"kar","karna","kiya","karunga","karoge",
"ja","jana","gaya","aaya","aana",
"de","dena","liya","lena",
"bol","bolo","sun","suno","samajh",
"dekha","dekho","mil","mila",
"raha","rahi","rahe","gaya","gayi",
"jaldi","der","baar",
"problem","solution","kaam",
"mast","bakwas","faltu","awesome",
"bhaiya","dost","friend","log",
"chalo","ruk","rukna","wait",
"ab","phir","toh","to","hi"
])

telugu_dict = set([
"nenu","ga","nuvvu","meeru","manam","memu","vaadu","aame",
"naa","nee","mee","mana",
"naaku","neeku","meeku","vaadiki","aameki",
"unna","unnanu","unnav","unnaru",
"ledu","le","kaadu",
"avunu","sare","inka","aithe",
"chala","konchem","ekkuva","takkuva",
"ippudu","appudu","malli",
"enduku","ela","eppudu","ekkada",
"em","emi","enti","yenti",
"cheppu","cheppanu","cheppandi","cheppava",
"cheyyi","chesa","chesanu","chesav","chesaru",
"vastanu","vastundi","vastav","vachindi",
"vellanu","vellava","vasthava","ki",
"ivvu","ichanu","ichav","icharu",
"teesuko","teesukonu","chesava"
"matladam","matladandi","matladava",
"chudu","chustanu","chusanu",
"ardham","ardhamayindi","telusu",
"pani","bagundi","bagoledu","baagundi",
"kastam","navvu","edupu","kopam",
"ra","amma","anna","bavunava","tinava","vachava","vachavu","vacharu","chalu","naku","nuvvu","meeru","manam","memu","vaadu","aame"
])

tamil_dict = set([
"naan","nee","neenga","avan","ava","avanga",
"en","un","unga","namma",
"irukken","irukka","irukku","irundha",
"illa","illai","aama","seri","sari",
"romba","konjam","nalla","ketta",
"ippadi","appadi","ippo","apram",
"enna","edhu","eppadi","enga",
"sol","sollu","sonnen","solren",
"pannu","pannuren","panninen","pannunga",
"vandhen","vandhuten","vandha",
"po","pona","poitu","poga",
"va","vaa","vandhu",
"koduthu","eduthu",
"paathu","parthu","paaru",
"theriyum","puriyala","purinjidhu",
"velai","mosam","correct","wrong",
"dei","da","pa","ma"
])


def predict_word(word, context_words):
    w = normalize(word)

    if not w.isalpha():
        return "other"

    # direct match (non-ambiguous words)
    if w in english_dict and w not in hindi_dict and w not in telugu_dict:
        return "en"
    if w in hindi_dict and w not in telugu_dict:
        return "hi"
    if w in telugu_dict and w not in hindi_dict:
        return "te"
    if w in tamil_dict:
        return "ta"

    # 🔥 CONTEXT CHECK (for ambiguous words like "ki")
    context_langs = []

    for cw in context_words:
        cw = normalize(cw)

        if cw in telugu_dict:
            context_langs.append("te")
        elif cw in hindi_dict:
            context_langs.append("hi")
        elif cw in english_dict:
            context_langs.append("en")
        elif cw in tamil_dict:
            context_langs.append("ta")

    if context_langs:
        counts = Counter(context_langs)

        if counts.get("te", 0) > 0:
            return "te"
        elif counts.get("hi", 0) > 0:
            return "hi"
        elif counts.get("ta", 0) > 0:
            return "ta"
        elif counts.get("en", 0) > 0:
            return "en"

    return "other"

def analyze_sentence(sentence):
    sentence = clean_sentence(sentence)
    words = sentence.split()

    langs = []
    result = []

    for i, w in enumerate(words):

        # 🔥 take surrounding words (context window)
        context = words[max(0, i-2): i] + words[i+1: i+3]

        lang = predict_word(w, context)

        langs.append(lang)
        result.append((w, lang))

    valid_langs = [l for l in langs if l != "other"]

    is_code_mixed = len(set(valid_langs)) > 1
    dominant = Counter(valid_langs).most_common(1)[0][0] if valid_langs else "unknown"

    return result, is_code_mixed, dominant


# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    code_mixed = None
    dominant = None
    sentence = ""   # ✅ NEW (stores input)

    if request.method == 'POST':
        sentence = request.form['sentence']   # ✅ capture input
        result, code_mixed, dominant = analyze_sentence(sentence)

    return render_template(
        'index.html',
        result=result,
        code_mixed=code_mixed,
        dominant=dominant,
        sentence=sentence   # ✅ send to HTML
    )


if __name__ == '__main__':
    app.run(debug=True)