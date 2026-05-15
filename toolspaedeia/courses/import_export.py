import re
from enum import StrEnum

from django.db import transaction

from courses.models import Answer
from courses.models import Course
from courses.models import Module
from courses.models import Question
from courses.models import Quiz


class Tag(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"
    MODULE = "module"
    TITLE = "title"
    CONTENT = "content"
    QUIZ = "quiz"
    QUESTION = "question"
    TEXT = "text"
    ANSWER = "answer"
    IS_CORRECT = "is_correct"


_ACCEPTED_TAGS = tuple(tag.value for tag in Tag)


def _next_tag_block(text, cursor=0):
    start_regex = re.compile(rf"@start\s+({'|'.join(sorted(_ACCEPTED_TAGS))})", re.IGNORECASE)
    start_match = start_regex.search(text, cursor)
    if not start_match:
        return None

    tag = Tag(start_match.group(1).lower())

    end_regex = re.compile(rf"@end\s+{re.escape(tag.value)}\b", re.IGNORECASE)
    end_match = end_regex.search(text, start_match.end())
    if not end_match:
        error_message = f"Unclosed @start {tag.value} block."
        raise ValueError(error_message)

    inner = text[start_match.end() : end_match.start()].strip()
    return tag, inner, end_match.end()


def _iter_blocks(text):
    cursor = 0
    while True:
        block = _next_tag_block(text, cursor)
        if block is None:
            return
        yield block
        cursor = block[2]


def _parse_answer_block(answer_inner):
    answer = Answer()
    for tag, value, _ in _iter_blocks(answer_inner):
        if tag is Tag.TEXT:
            answer.text = value
        elif tag is Tag.IS_CORRECT:
            answer.is_correct = value.strip().lower() == "true"
    return answer


def _parse_question_block(question_inner):
    question = Question(order=0)
    answers = []
    for tag, value, _ in _iter_blocks(question_inner):
        if tag is Tag.TEXT:
            question.text = value
        elif tag is Tag.ANSWER:
            answers.append(_parse_answer_block(value))
    return question, answers


def _parse_quiz_block(quiz_inner, module):
    quiz = Quiz(module=module)
    questions_payload = []
    for tag, value, _ in _iter_blocks(quiz_inner):
        if tag is Tag.TITLE:
            quiz.title = value
        elif tag is Tag.DESCRIPTION:
            quiz.description = value
        elif tag is Tag.QUESTION:
            question, answers = _parse_question_block(value)
            questions_payload.append((question, answers))
    return quiz, questions_payload


def _parse_module_block(module_inner):
    module = Module(order=0)
    quiz_payload = None
    for tag, value, _ in _iter_blocks(module_inner):
        if tag is Tag.TITLE:
            module.title = value
        elif tag is Tag.DESCRIPTION:
            module.description = value
        elif tag is Tag.CONTENT:
            module.content = value
        elif tag is Tag.QUIZ:
            quiz_payload = _parse_quiz_block(value, module)
    return module, quiz_payload


def create_course_from_import(markdown_input, publisher):
    course = Course(publisher=publisher)
    module_quiz_pairs = []

    for tag, inner, _ in _iter_blocks(markdown_input):
        if tag is Tag.NAME:
            course.name = inner
        elif tag is Tag.DESCRIPTION:
            course.description = inner
        elif tag is Tag.MODULE:
            module_quiz_pairs.append(_parse_module_block(inner))

    with transaction.atomic():
        course.save()
        for module, quiz_payload in module_quiz_pairs:
            module.course = course
            module.save()
            if quiz_payload is None:
                continue

            quiz, questions_payload = quiz_payload
            quiz.module = module
            quiz.save()

            for question, answers in questions_payload:
                question.quiz = quiz
                question.save()
                for answer in answers:
                    answer.question = question
                    answer.save()
    return course
