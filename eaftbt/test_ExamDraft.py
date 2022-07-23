from eaftbt.ExamDraft import ExamDraft, TestQuestion


def test_exam_draft_basic():
    exd = ExamDraft()
    var0 = exd.get_variant(0)
    var1 = exd.get_variant(101)
    var2 = exd.get_variant(69420)
    assert len(var0) == 0
    assert len(var1) == 0
    assert len(var2) == 0


# def test_add_question():
#     exd = ExamDraft()
#     que = EmptyQuestion()
#     exd.add_question(que)
#     var = exd.get_variant(0)
#     assert len(var) == 0
#     assert var[0] is que

def test_basic_question():
    default_substitution = {"id": None, "substitution": []}

    q = TestQuestion("")
    assert q.question_id == ""
    assert q.substitution == default_substitution

    q.set_substitution_manually()
    assert q.question_id == ""
    assert q.substitution == default_substitution

def test_set_substitution_by_id():
    default_substitution = {"id": None, "substitution": []}

    q = TestQuestion("")
    q.set_substitution_by_id('111')
    assert q.question_id == ""
    assert q.substitution == default_substitution

    q.set_substitution_by_id('111')
    assert q.question_id == ""
    assert q.substitution == default_substitution

    q.set_substitution_by_id('000')
    assert q.question_id == ""
    assert q.substitution == default_substitution

    q = TestQuestion("1gg5l35hj3")
    assert q.question_id != ""
    assert q.substitution == default_substitution

    q.set_substitution_by_id('111')
    assert q.substitution == default_substitution

    new_substitution = {"id": "000", "substitution": ["\\frac{2}{5}\\frac{3}{7}", "4"]}

    q.set_substitution_by_id('000')
    assert q.substitution != default_substitution
    assert q.substitution["id"] == '000'
    assert q.substitution == new_substitution

def test_question_get_substitution():
    q = TestQuestion("")
    assert q.get_substitution() == new_substitution

    q.set_substitution_by_id("111")
    assert q.get_substitution() == default_substitution



def test_question_get_substitution():
    pass