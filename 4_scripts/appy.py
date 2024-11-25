from flask import Flask, jsonify, send_file, make_response 
from flask_restx import Api, Resource, fields 
import pandas as pd 

app = Flask(__name__)
api = Api(app, version="1.0", title="API de Dados CSV",
          description="API para acessar e baixar os dados CSV.")

ns_dados = api.namespace('dados', description="Dados CSV")

csv_file = '../0_bases_originais/dados.csv'
df = pd.read_csv(csv_file)
dados_json = df.to_dict(orient='records')

modelo_dados = api.model('Dados', {col: fields.String(description=f"Valor da coluna {col}") for col in df.columns})

@ns_dados.route('/')
class DadosLista(Resource):
    @ns_dados.doc(description="Retorna dados do arquivo CSV em formato JSON.")
    @ns_dados.marshal_with(modelo_dados, as_list=True)
    def get(self):
        return dados_json

@ns_dados.route('/download')
class DadosDownload(Resource):
    @ns_dados.doc(description="Permite baixar o arquivo CSV original.")
    def get(self):
        """
        Retorna o arquivo CSV original para download.
        """
        try:
            return send_file(csv_file, as_attachment=True)
        except Exception as e:
            return {"mensagem": f"Erro ao baixar o arquivo: {str(e)}"}, 500

@api.route('/dados-brutos')
class DadosBrutos(Resource):
    def get(self):
        """
        Exibe os dados brutos do CSV em formato JSON.
        """
        return make_response(jsonify(dados_json), 200)


@api.route('/')
class Home(Resource):
    def get(self):
        """
        Página inicial da API.
        """
        return {
            "mensagem": "Bem-vindo à API de dados!",
            "endpoints": {
                "/dados": "Lista os dados do CSV em JSON",
                "/dados/download": "Faz o download do CSV original",
                "/dados-brutos": "Visualiza os dados brutos no navegador"
            }
        }


api.add_namespace(ns_dados)

if __name__ == "__main__":
    app.run(debug=True)
