import operator
from functools import cache

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from courses.models import CourseTag


@cache
def embedding_model():
    return SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


def suggest_tags(course, min_score: float = 0.2) -> list[tuple]:
    all_tags = list(CourseTag.objects.all())
    if not all_tags:
        return []

    modules = [f"{module.title}\n{module.description}\n\n{module.content}" for module in course.modules.all()]

    course_chunks = [
        f"{course.name}\n{course.description}",
        *modules,
    ]

    tag_names = [tag.name for tag in all_tags]

    course_embedding = embedding_model().encode(course_chunks, convert_to_tensor=True)
    tag_embeddings = embedding_model().encode(tag_names, convert_to_tensor=True)

    scores = cos_sim(course_embedding, tag_embeddings)[0]

    results = [(all_tags[i], float(scores[i])) for i in range(len(all_tags)) if float(scores[i]) >= min_score]
    return sorted(results, key=operator.itemgetter(1), reverse=True)
