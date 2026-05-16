import operator
from functools import cache

import spacy

from courses.models import CourseTag


@cache
def _get_nlp_model():
    """Return the shared spaCy model instance, loading on first call."""
    return spacy.load("en_core_web_sm")


def suggest_tags(course, top_k: int = 5) -> list[tuple]:
    """Return the top k semantically relevant CourseTag objects for a course."""
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

    nlp = _get_nlp_model()
    course_doc = nlp(course_text)
    tag_names = [tag.name for tag in all_tags]
    tag_docs = [nlp(tag_name) for tag_name in tag_names]

    scores = [course_doc.similarity(tag_doc) for tag_doc in tag_docs]

    results = [(all_tags[i], float(scores[i])) for i in range(len(all_tags))]
    return sorted(results, key=operator.itemgetter(1), reverse=True)[:top_k]
