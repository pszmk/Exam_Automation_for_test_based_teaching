from eaftbt.ExamDraft import ExamDraft


def test_exam_draft_basic():
    exd = ExamDraft()
    var0 = exd.get_variant(0)
    var1 = exd.get_variant(101)
    var2 = exd.get_variant(69420)
    assert len(var0) == 0
    assert len(var1) == 0
    assert len(var2) == 0


def test_add_question():
    exd = ExamDraft()
    que = EmptyQuestion()
    exd.add_question(que)
    var = exd.get_variant(0)
    assert len(var) == 0
    assert var[0] is que

