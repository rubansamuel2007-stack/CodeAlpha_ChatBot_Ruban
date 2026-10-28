import re
from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_data.csv"

SIMILARITY_THRESHOLD = 0.25


# --------------------------------------------------
# NLP RESOURCE SETUP
# --------------------------------------------------

def load_stopwords():
    """
    Load English stopwords from NLTK.
    Download the resource if it is not already installed.
    """

    try:
        return set(stopwords.words("english"))

    except LookupError:
        try:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))

        except Exception:
            # The chatbot can still run without stopword removal.
            return set()


STOP_WORDS = load_stopwords()


# --------------------------------------------------
# TEXT PREPROCESSING
# --------------------------------------------------

def preprocess_text(text):
    """
    Clean text for FAQ matching.

    Operations:
    1. Convert to lowercase.
    2. Remove URLs.
    3. Remove punctuation and special characters.
    4. Remove unnecessary spaces.
    5. Remove English stopwords.
    """

    text = str(text).lower()

    # Remove URLs.
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Keep letters, digits, and whitespace.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Split text into tokens.
    tokens = text.split()

    # Remove stopwords without deleting every word.
    cleaned_tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS
    ]

    return " ".join(cleaned_tokens)


# --------------------------------------------------
# LOAD FAQ DATABASE
# --------------------------------------------------

def load_faqs():
    """
    Load questions and answers from faq_data.csv.
    """

    if not FAQ_FILE.exists():
        raise FileNotFoundError(
            f"FAQ database not found: {FAQ_FILE}"
        )

    df = pd.read_csv(FAQ_FILE)

    required_columns = {"question", "answer"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "faq_data.csv must contain question and answer columns."
        )

    df = df.dropna(subset=["question", "answer"]).copy()

    df["question"] = df["question"].astype(str).str.strip()
    df["answer"] = df["answer"].astype(str).str.strip()

    df = df[
        (df["question"] != "")
        & (df["answer"] != "")
    ].reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "The FAQ database contains no valid questions."
        )

    return df


# --------------------------------------------------
# BUILD TF-IDF MODEL
# --------------------------------------------------

class FAQChatbot:

    def __init__(self):
        self.faqs = load_faqs()

        # Preprocess the stored FAQ questions.
        self.processed_questions = [
            preprocess_text(question)
            for question in self.faqs["question"]
        ]

        # Use word unigrams and bigrams.
        # Character n-grams help with minor spelling variations.
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            lowercase=True,
            sublinear_tf=True
        )

        self.faq_vectors = self.vectorizer.fit_transform(
            self.processed_questions
        )

    # --------------------------------------------------
    # FIND THE BEST MATCH
    # --------------------------------------------------

    def get_response(self, user_question):
        """
        Find the most similar FAQ question and return
        its answer when the similarity is sufficient.
        """

        if not user_question or not user_question.strip():
            return {
                "answer": "Please enter a question.",
                "matched_question": None,
                "confidence": 0.0,
                "matched": False
            }

        cleaned_question = preprocess_text(user_question)

        if not cleaned_question:
            return {
                "answer": (
                    "I couldn't understand that question. "
                    "Please enter a question with more details."
                ),
                "matched_question": None,
                "confidence": 0.0,
                "matched": False
            }

        # Convert the user's question into a vector.
        user_vector = self.vectorizer.transform(
            [cleaned_question]
        )

        # Compare the user question with every FAQ question.
        similarities = cosine_similarity(
            user_vector,
            self.faq_vectors
        ).flatten()

        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        matched_question = self.faqs.iloc[best_index]["question"]
        matched_answer = self.faqs.iloc[best_index]["answer"]

        # Do not return an unrelated answer.
        if best_score < SIMILARITY_THRESHOLD:
            return {
                "answer": (
                    "Sorry, I couldn't find a suitable answer "
                    "in my FAQ database. Please rephrase your "
                    "question or contact the support team."
                ),
                "matched_question": None,
                "confidence": best_score,
                "matched": False
            }

        return {
            "answer": matched_answer,
            "matched_question": matched_question,
            "confidence": best_score,
            "matched": True
        }


# --------------------------------------------------
# QUICK TEST
# --------------------------------------------------

if __name__ == "__main__":

    chatbot = FAQChatbot()

    print("\nFAQMate - FAQ Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("FAQMate: Goodbye!")
            break

        result = chatbot.get_response(question)

        print(f"FAQMate: {result['answer']}")

        if result["matched"]:
            print(
                "Matched FAQ:",
                result["matched_question"]
            )
            print(
                f"Similarity: {result['confidence']:.2%}"
            )

        print()
