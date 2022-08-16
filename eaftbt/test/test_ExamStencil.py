import pytest
from eaftbt.ExamDraft import TryOutQuestion, ExamDraft
from eaftbt.ExamStencil import ExamStencil
from eaftbt.ExamStencil import NoQuestionError, NoExamDraftError
from pathlib import Path
from copy import copy

question_id_test_1 = "1gg5l35hj3"
exam_set_id_test_1 = "q0l67rgm5"
exam_id_test_1 = "yyisjdfsd7544"
question_id_test_1 = "1gg5l35hj3"
playground_path = Path("../data") / "user-data" / "playground"

def test_ExamStencil_basic_0():
    with pytest.raises(ValueError) as e:
        es = ExamStencil('')
    assert str(e.value) == "The path is not valid."
    assert e.type == ValueError
    es = ExamStencil()
    assert es.question == None
    assert es.exam_template_substitution == {"course_substitution": 'Math 115',
                                  "professor_substitution": 'Professor Hilbert',
                                  "exam_title_substitution": 'First Exam 2022',
                                  "qrcode_data_substitution": 'tutaj znajduja sie informacje co do tego gdzie wyslac wyniki',
                                  "subtitle_substitution": 'Dzielenie'}

def test_ExamStencil_basic_1():
    es = ExamStencil(playground_path)
    assert es.path == playground_path

def test_ExamStencil_set_question():
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id("000")
    es = ExamStencil()
    es.set_question(tq)
    assert es.question == tq

def test_ExamStencil_generate_question_tex():
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id("000")
    tq.set_text()
    es = ExamStencil()
    es.set_question(tq)
    assert es.question == tq
    assert es.question.get_text() != None

def test_ExamStencil_generate_quesion_tex():
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id("000")
    tq.set_text()
    es = ExamStencil()
    es.set_question(tq)
    assert es.question == tq
    assert es.question.get_text() != None

def test_ExamStencil_generate_exam_draft_tex():
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id("000")
    tq.set_text()

def test_ExamStencil_set_question_raises_error():
    es = ExamStencil()
    with pytest.raises(ValueError) as e:
        es.set_question("3")
    assert str(e.value) == "Provided object is not of Question class."
    assert e.type == ValueError

def test_ExamStencil_generate_question_tex_raises_error():
    es = ExamStencil()
    with pytest.raises(NoQuestionError) as e:
        es.generate_question_tex()
    assert str(e.value) == "There is no question assigned."
    assert e.type == NoQuestionError

def test_ExamStencil_set_exam_draft():
    es = ExamStencil()
    ed = ExamDraft(exam_set_id=exam_set_id_test_1, exam_id=exam_id_test_1)
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id()
    tq.set_text()
    ed.add_question(copy(tq))
    tq.set_substitution_by_id("001")
    tq.set_text()
    ed.add_question(copy(tq))
    es.set_exam_draft(ed)
    assert es.exam_draft == ed

def test_ExamStencil_set_exam_draft_raises_error():
    es = ExamStencil()
    with pytest.raises(ValueError) as e:
        es.set_exam_draft("ueriue")
    assert str(e.value) == "The object is not of ExamDraft class."
    assert e.type == ValueError

def test_ExamStancil_generate_exam_draft_save():
    es = ExamStencil(path=playground_path)
    ed = ExamDraft(exam_set_id=exam_set_id_test_1, exam_id=exam_id_test_1)
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id()
    tq.set_text()
    ed.add_question(copy(tq))
    tq.set_substitution_by_id("001")
    tq.set_text()
    ed.add_question(copy(tq))
    es.set_exam_draft(ed)
    filename = "hhh"
    es.generate_exam_draft_tex(filename=filename, save=True)
    assert f"{filename}.tex" in [str(item).split(sep='/')[-1] for item in Path(es.get_path()).iterdir() if item.is_file()]
