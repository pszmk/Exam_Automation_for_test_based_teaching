import pytest
from eaftbt.ExamDraft import ExamDraft, TryOutQuestion, NoQuestionIdError

question_id_test_1 = "1gg5l35hj3"

# def test_exam_draft_basic():
#     exd = ExamDraft()
#     var0 = exd.get_variant(0)
#     var1 = exd.get_variant(101)
#     var2 = exd.get_variant(69420)
#     assert len(var0) == 0
#     assert len(var1) == 0
#     assert len(var2) == 0


# def test_add_question():
#     exd = ExamDraft()
#     que = EmptyQuestion()
#     exd.add_question(que)
#     var = exd.get_variant(0)
#     assert len(var) == 0
#     assert var[0] is que

def test_question_basic():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}

    with pytest.raises(NoQuestionIdError) as e:
        tq = TryOutQuestion("")
    assert str(e.value) == "Provided question_id is not valid."
    assert not e.type == ValueError
    assert e.type == NoQuestionIdError

    with pytest.raises(NoQuestionIdError) as e:
        tq = TryOutQuestion("5783783721rr")
    assert str(e.value) == "Provided question_id is not valid."
    assert not e.type == ValueError
    assert e.type == NoQuestionIdError

    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_manually()
    assert not tq.question_id == ""
    assert tq.substitution == default_substitution


def test_question_check_question_id():
    tq = TryOutQuestion(question_id_test_1)
    assert tq.question_id == question_id_test_1
    assert tq.check_question_id()

    tq.question_id = '4'
    assert not tq.check_question_id()


def test_question_check_substitution_id():
    tq = TryOutQuestion(question_id_test_1)
    tq.question_id = ""
    tq.is_question_id = False
    with pytest.raises(NoQuestionIdError) as e:
        tq.check_substitution_id("")
    assert str(e.value) == "There is no question_id."
    assert e.type == NoQuestionIdError

    tq = TryOutQuestion(question_id_test_1)
    assert not tq.check_substitution_id("")
    assert not tq.check_substitution_id('00')
    assert not tq.check_substitution_id('uut')
    assert tq.check_substitution_id('000')

    tq.reset_substitution()
    assert tq.check_substitution_id('000')


def test_question_set_substitution_by_id():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id" : "000", "substitution" : ['\\frac{2}{5}\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]}

    tq = TryOutQuestion(question_id_test_1)
    tq.is_question_id = False
    with pytest.raises(NoQuestionIdError) as e:
        tq.set_substitution_by_id('000')
    assert str(e.value) == "There is no question_id."
    assert e.type == NoQuestionIdError

    tq = TryOutQuestion(question_id_test_1)
    with pytest.raises(ValueError) as e:
        tq.set_substitution_by_id('111')
    assert str(e.value) == "Wrong substitution id!"
    assert e.type == ValueError
    assert tq.substitution == default_substitution

    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id('000')
    assert tq.substitution == substitution_000_question_1gg5l35hj3

    tq = TryOutQuestion(question_id_test_1)
    assert tq.question_id != ""
    assert tq.substitution == default_substitution


def test_question_get_substitution():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id": "000", "substitution": ['\\frac{2}{5}\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]}
    tq = TryOutQuestion(question_id_test_1)
    assert tq.get_substitution() == default_substitution["substitution"]

    tq.set_substitution_by_id("000")
    assert tq.get_substitution() == substitution_000_question_1gg5l35hj3["substitution"]

    tq.reset_substitution()
    assert tq.get_substitution() == default_substitution["substitution"]

def test_question_get_answer():
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}
    substitution_000_question_1gg5l35hj3 = {"substitution_id": "000", "substitution": ['\\frac{2}{5}\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]}
    tq = TryOutQuestion(question_id_test_1)
    assert tq.get_answer() == default_substitution["answer"]

    tq.set_substitution_by_id("000")
    assert tq.get_answer() == substitution_000_question_1gg5l35hj3["answer"]

    tq.reset_substitution()
    assert tq.get_answer() == default_substitution["answer"]