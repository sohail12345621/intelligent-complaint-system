import joblib, os

MODEL_PATH = "models/category_model.pkl"
VEC_PATH = "models/tfidf_vectorizer.pkl"

_model = None
_vectorizer = None

def _load():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not (os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH)):
            raise FileNotFoundError("ML model not found. Run ml/train_model.py first.")
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VEC_PATH)
    return _model, _vectorizer

def predict_category(text: str) -> str:
    model, vectorizer = _load()
    X = vectorizer.transform([text])
    return model.predict(X)[0]
