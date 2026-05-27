import operator
from functools import cache

from sklearn.feature_extraction.text import TfidfVectorizer

from courses.models import CourseTag


@cache
def _get_vectorizer():
    return TfidfVectorizer(lowercase=True, stop_words="english", max_features=5000)


def suggest_tags(course, min_score: float = 0.01) -> list[tuple]:
    all_tags = list(CourseTag.objects.all())
    if not all_tags:
        return []

    course_text = " ".join(
        [
            course.name,
            course.description,
            *course.modules.values_list("title", flat=True),
            *course.modules.values_list("description", flat=True),
            *course.modules.values_list("content", flat=True),
        ],
    )

    vectorizer = _get_vectorizer()
    tag_names = [tag.name for tag in all_tags]

    texts = [course_text, *tag_names]
    tfidf_matrix = vectorizer.fit_transform(texts)

    course_vector = tfidf_matrix[0]
    tag_vectors = tfidf_matrix[1:]

    scores = course_vector.dot(tag_vectors.T).toarray().flatten()

    results = [(all_tags[i], float(scores[i])) for i in range(len(all_tags)) if scores[i] >= min_score]
    return sorted(results, key=operator.itemgetter(1), reverse=True)
