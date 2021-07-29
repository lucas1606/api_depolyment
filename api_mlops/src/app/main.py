from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

reg = pickle.load(open('../../models/modelo.sav','rb'))
colunas = ["tamanho", "ano", "garagem"]


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME']=os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD']=os.environ.get('BASIC_AUTH_PASSWORD')


basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    tb_en.sentiment.polarity
    polaridade = tb_en.sentiment.polarity
    return "polaridade: {}".format(polaridade)

@app.route('/cotacao/', methods = ['POST',])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = reg.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')