from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(job_description, resumes_text):
    """
    resumes_text: list of strings (resume texts)
    Returns: list of cosine similarity scores
    """
    if not resumes_text:
        return []
        
    documents = [job_description] + resumes_text
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        # Calculate similarity of all resumes against the job description (index 0)
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        return cosine_similarities.tolist()
    except Exception as e:
        print(f"Error in ranking: {e}")
        return [0.0] * len(resumes_text)
