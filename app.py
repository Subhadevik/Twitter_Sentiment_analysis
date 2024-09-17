from flask import Flask, request, jsonify, render_template
import joblib
import gzip
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Initialize Flask app
app = Flask(__name__)

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Load model and vectorizer
with gzip.open('sentiment_model.pkl.gz', 'rb') as f:
    loaded_model = joblib.load(f)

with gzip.open('vectorizer.pkl.gz', 'rb') as f:
    loaded_vectorizer = joblib.load(f)

# Preprocessing function
ps = PorterStemmer()
stops = set(stopwords.words('english'))

def preprocessing_text(text):
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    # Tokenize and remove stopwords and apply stemming
    token = text.split()
    token = [ps.stem(word) for word in token if word not in stops]
    return ' '.join(token)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Sentiment analysis route
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tweet = data.get('tweet', '')
    if not tweet:
        return jsonify({'sentiment': 'No input provided'})

    processed_tweet = preprocessing_text(tweet)
    user_vector = loaded_vectorizer.transform([processed_tweet])
    prediction = loaded_model.predict(user_vector)
    return jsonify({'sentiment': str(prediction[0])})

#if __name__ == "__main__":
    #app.run(debug=True)
