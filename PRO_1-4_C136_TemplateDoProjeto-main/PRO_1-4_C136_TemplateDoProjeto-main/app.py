from flask import Flask, render_template, request, jsonify
import prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# api ouvindo solicitações POST e prevendo sentimentos
@app.route('/predict', methods=['POST'])
def predict():
    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status': 'error',
                    'message': 'Avaliação em Branco'}
    else:
        sentiment, path = prediction.predict(review)
        response = {'status': 'success',
                    'message': 'Got it',
                    'sentiment': sentiment,
                    'path': path}
    return jsonify(response)

# Criando uma API para salvar a avaliação. O usuário clica no botão Salvar
@app.route('/save', methods=['POST'])
def save():
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')
    data_entry = f"{date}, {product}, {review}, {sentiment}\n"

    with open('data_file.txt', 'a') as file:
        file.write(data_entry)

    return jsonify({'status': 'success', 
                    'message': 'Dados Registrados'})

if __name__ == "__main__":
    app.run(debug=True)
