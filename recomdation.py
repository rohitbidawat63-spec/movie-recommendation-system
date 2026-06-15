import pandas as pd
import pickle
data = pd.read_csv("tmdb_5000_movies.csv")
data = data[['id','title','overview']]
data.dropna(inplace = True)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words = 'english')
vectors = cv.fit_transform(data['overview']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
pickle.dump(data,open('data.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

