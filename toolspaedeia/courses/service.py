from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import format_html

from courses.models import Quiz
from toolspaedeia.utils import markdown_to_html


def build_fresh_answers_data(question):
    """Build answer render data for a fresh quiz attempt."""
    return [
        {
            "answer": answer,
            "was_selected": False,
            "is_correct_choice": False,
        }
        for answer in question.get_answers()
    ]


def build_quiz_data(questions, answers_by_question=None):
    """Build question/answer render data for a quiz section."""
    answers_by_question = answers_by_question or {}
    quiz_data = []

    for question in questions:
        answers_data = answers_by_question.get(question.id)
        if answers_data is None:
            answers_data = build_fresh_answers_data(question)
        quiz_data.append(
            {
                "question": question,
                "question_html": format_html(markdown_to_html(question.text or "")),
                "answers_data": answers_data,
            }
        )

    return quiz_data


def get_quiz_and_course(course_id, quiz_id):
    """Return quiz and its course for the provided ids."""
    quiz = get_object_or_404(
        Quiz.objects.select_related("module__course"),
        id=quiz_id,
        module__course_id=course_id,
    )
    return quiz, quiz.module.course


def get_attempt_questions(quiz, posted_question_ids=None):
    """
    Return the questions to the user in the same order as they were posted
    (if any were posted), or in a fresh randomized order if not. This ensures
    that when a user retries a quiz, they see the same questions in the same
    order as they did in the previous attempt, even if the quiz has
    randomization enabled.
    """
    posted_question_ids = posted_question_ids or []
    if posted_question_ids:
        question_map = {str(question.id): question for question in quiz.questions.filter(id__in=posted_question_ids)}
        return [question_map[question_id] for question_id in posted_question_ids if question_id in question_map]
    return list(quiz.get_questions_for_attempt())


def get_answers_in_display_order(question, posted_answer_ids):
    """
    Similarly to the questions, preserve the order of the answers as they were
    posted by the user, if any, or return them in a fresh randomized order if
    not. This ensures that when a user retries a quiz, they see the same answers
    in the same order as they did in the previous attempt, even if the quiz has
    randomization enabled.
    """
    if posted_answer_ids:
        answer_map = {str(answer.id): answer for answer in question.answers.filter(id__in=posted_answer_ids)}
        ordered_answers = [answer_map[answer_id] for answer_id in posted_answer_ids if answer_id in answer_map]
        if ordered_answers:
            return ordered_answers
    return list(question.get_answers())


def build_checked_answers_data(question, submitted_answer_ids, posted_answer_ids):
    """Build answer render data for a checked quiz attempt."""
    answers_data = []
    for answer in get_answers_in_display_order(question, posted_answer_ids):
        was_selected = str(answer.id) in submitted_answer_ids
        answers_data.append(
            {
                "answer": answer,
                "was_selected": was_selected,
                "is_correct_choice": was_selected == answer.is_correct,
            }
        )
    return answers_data


def render_quiz_section(request, quiz, course, quiz_data, show_results):
    """Render quiz section partial HTML response."""
    context = {
        "quiz": quiz,
        "course": course,
        "quiz_data": quiz_data,
        "show_results": show_results,
    }
    html = render_to_string("courses/partials/quiz_section.html", context, request=request)
    return HttpResponse(html)
