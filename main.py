from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle

reg = pickle.load(open('modelo.sav','rb'))
colunas = ["tamanho", "ano", "garagem"]


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME']='Lucas'
app.config['BASIC_AUTH_PASSWORD']='alura'


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

app.run(debug=True)