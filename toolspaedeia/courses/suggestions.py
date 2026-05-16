import operator
from functools import cache

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from courses.models import CourseTag


@cache
def _get_embedding_model():
    """Return the shared SentenceTransformer instance, loading on first call."""
    return SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


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

    model = _get_embedding_model()
    tag_names = [tag.name for tag in all_tags]

    course_embedding = model.encode(course_text, convert_to_tensor=True)
    tag_embeddings = model.encode(tag_names, convert_to_tensor=True)

    scores = cos_sim(course_embedding, tag_embeddings)[0]

    results = [(all_tags[i], float(scores[i])) for i in range(len(all_tags))]
    return sorted(results, key=operator.itemgetter(1), reverse=True)[:top_k]
