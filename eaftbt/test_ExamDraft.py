import pytest
from eaftbt.ExamDraft import ExamDraft, TryOutQuestion, NoQuestionIdError\
    # , ExamSet

question_id_test_1 = "1gg5l35hj3"
exam_id_test_1 = "yyisjdfsd7544"
exam_set_id_test_1 = "q0l67rgm5"
def exam_draft_fixture_test_1():
    yield ExamDraft(exam_set_id=exam_set_id_test_1, exam_id=exam_id_test_1)

# def test_exam_set_basic_0():
#     es = ExamSet(None)
#     assert es.exam_set_id == None
#     assert es.check_exam_set_id()
#
# def test_exam_set_basic_1():
#     es = ExamSet(None)
#     ed = exam_draft_fixture_test_1().__next__()
#     tq = TryOutQuestion(question_id_test_1)
#     ed.add_question(tq)
#     es.add_exam_draft(ed)
#     assert es.get_exam_drafts() == [ed]
#
# def test_exam_set_raises_ValusError():
#     with pytest.raises(ValueError) as e:
#         es = ExamSet(exam_set_id_test_1)
#     assert str(e.value) == "Provided exam_set_id: q0l67rgm5 is already used."

'''
TESTING EXAM DRAFT
'''
def test_exam_draft_basic_0():
    # from copy import copy
    ed = ExamDraft(exam_set_id_test_1, None)
    assert ed.exam_set_id == exam_set_id_test_1
    assert ed.exam_id == None

    ed.exam_id = exam_id_test_1
    assert ed.exam_id == exam_id_test_1

def test_exam_draft_basic_1():
    ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)
    assert ed.exam_id == exam_id_test_1
    assert len(ed.questions) == 0

#     '''
#     What I do here seems kinda dumb because I am creating direct copies of objects meaning that I all of them are
#     modified once I modify one of them. In real case scenario we will be passing deep copies of objects meaning that
#     they have the same content, but are separate object not just references to original objects.
#     '''

def test_exam_draft_add_many_questions():
    ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)
    tq1 = TryOutQuestion(question_id_test_1)
    tq2 = TryOutQuestion(question_id_test_1)
    tq2.set_substitution_by_id("000")
    ed.add_question(tq1)
    ed.add_question(tq2)
    assert ed.questions == [tq1, tq2]

    tq3 = TryOutQuestion(question_id_test_1)
    ed.add_question(tq3)
    assert ed.questions == [tq1, tq2, tq3]

    ed.questions[2].set_substitution_by_id("000")
    assert ed.questions == [tq1, tq2, tq3]
    assert tq3.substitution == {"substitution_id" : "000", "substitution" : ['\\frac{2}{5}','\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]}

    ed.remove_question(0)
    assert ed.questions == [tq2, tq3]


def test_exam_draft_raises_NoQuestionIdError():
    # ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)
    ed = exam_draft_fixture_test_1().__next__()

    with pytest.raises(NoQuestionIdError) as e:
        ed.add_question(TryOutQuestion(''))
    assert str(e.value) == "Provided question_id is not valid."
    assert e.type == NoQuestionIdError

    # assert len(ed.questions) == ed.questions
    assert len(ed.questions) == 0

def test_exam_draft_raises_ValueError_wrong_class():
    ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)

    with pytest.raises(ValueError) as e:
        ed.add_question('dfjfjd')
    assert str(e.value) == "The object provided is not of Question class."
    assert e.type == ValueError

    assert len(ed.questions) == 0

def test_ExamDraft_get_questions_text():
    from copy import copy
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id()
    tq.set_text()
    ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)
    ed.add_question(copy(tq))
    tq.set_substitution_by_id("001")
    tq.set_text()
    ed.add_question(copy(tq))
    # assert ed.get_questions_text() == None
    assert ed.get_questions_text() == ['Solve the following second degree polynomial and provide the smallest '
 'solution  $\\frac{2}{5}x^2 + \\frac{3}{7}x + 4$.',
 'Solve the following second degree polynomial and provide the smallest '
 'solution  $5x^2 + \\frac{2}{9}x + 123$.']


def test_question_check_question_id():
    tq = TryOutQuestion(question_id_test_1)
    assert tq.question_id == question_id_test_1
    assert tq.check_question_id()

    tq.question_id = '4'
    assert not tq.check_question_id()


def test_exam_draft_raises_ValueError_wrong_index_():
    ed = ExamDraft(exam_set_id_test_1, exam_id_test_1)

    ed.add_question(TryOutQuestion(question_id_test_1))
    with pytest.raises(ValueError) as e:
        ed.remove_question(5)
    assert str(e.value) == "Provided question_index is not within the expected range."
    assert e.type == ValueError


def test_question_basic_0():

    with pytest.raises(NoQuestionIdError) as e:
        tq = TryOutQuestion("")
    assert str(e.value) == "Provided question_id is not valid."
    assert not e.type == ValueError
    assert e.type == NoQuestionIdError

def test_question_basic_1():

    with pytest.raises(NoQuestionIdError) as e:
        tq = TryOutQuestion("5783783721rr")
    assert str(e.value) == "Provided question_id is not valid."
    assert not e.type == ValueError
    assert e.type == NoQuestionIdError

def test_question_basic_2():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}

    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_manually()
    assert not tq.question_id == ""
    assert tq.substitution == default_substitution


def test_question_basic_3():
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id()
    tq.set_text('0')
    assert tq.get_text() != None
    # assert f'{tq.get_text()}' == "Solve the following second degree polynomial and provide the smallest solution  $\frac{2}{5}x^2 + \frac{3}{7}x + 4$."


def test_question_check_substitution_id_0():
    tq = TryOutQuestion(question_id_test_1)
    tq.question_id = ""
    tq.is_question_id = False
    with pytest.raises(NoQuestionIdError) as e:
        tq.check_substitution_id("")
    assert str(e.value) == "There is no question_id."
    assert e.type == NoQuestionIdError

def test_question_check_substitution_id_1():

    tq = TryOutQuestion(question_id_test_1)
    assert not tq.check_substitution_id("")
    assert not tq.check_substitution_id('00')
    assert not tq.check_substitution_id('uut')
    assert tq.check_substitution_id('000')

    tq.reset_substitution()
    assert tq.check_substitution_id('000')


def test_question_set_substitution_by_id_2():

    tq = TryOutQuestion(question_id_test_1)
    tq.is_question_id = False
    with pytest.raises(NoQuestionIdError) as e:
        tq.set_substitution_by_id('000')
    assert str(e.value) == "There is no question_id."
    assert e.type == NoQuestionIdError

def test_question_set_substitution_by_id_3():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}

    tq = TryOutQuestion(question_id_test_1)
    with pytest.raises(ValueError) as e:
        tq.set_substitution_by_id('111')
    assert str(e.value) == "Wrong substitution id!"
    assert e.type == ValueError
    assert tq.substitution == default_substitution

def test_question_set_substitution_by_id_4():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id": "000",
                                                "substitution": ['\\frac{2}{5}','\\frac{3}{7}', '4'],
                                                "answer": ["0.666", "0.667"]}

    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id('000')
    assert tq.substitution == substitution_000_question_1gg5l35hj3

    tq = TryOutQuestion(question_id_test_1)
    assert tq.question_id != ""
    assert tq.substitution == default_substitution


def test_question_get_substitution():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id": "000",
                                            "substitution": ['\\frac{2}{5}', '\\frac{3}{7}', '4'],
                                            "answer": ["0.666", "0.667"]}
    tq = TryOutQuestion(question_id_test_1)
    assert tq.get_substitution() == default_substitution["substitution"]

    tq.set_substitution_by_id("000")
    assert tq.get_substitution() == substitution_000_question_1gg5l35hj3["substitution"]

    tq.reset_substitution()
    assert tq.get_substitution() == default_substitution["substitution"]

def test_question_get_answer():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id": "000", "substitution": ['\\frac{2}{5}','\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]}
    tq = TryOutQuestion(question_id_test_1)
    assert tq.get_answer() == default_substitution["answer"]

    tq.set_substitution_by_id("000")
    assert tq.get_answer() == substitution_000_question_1gg5l35hj3["answer"]

    tq.reset_substitution()
    assert tq.get_answer() == default_substitution["answer"]


# def test_question_get_text()