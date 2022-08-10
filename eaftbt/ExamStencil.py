from eaftbt.ExamDraft import TryOutQuestion, ExamDraft, Question
from eaftbt import data
from jinja2 import FileSystemLoader, Environment
from pathlib import PurePath, Path

class NoQuestionError(BaseException):
    pass

class NoExamDraftError(BaseException):
    pass

class ExamStencil:
    # output_path = ''
    default_template_path = Path('user-data')
    exam_template_substitution = {"course_substitution": 'Math 115',
                                  "professor_substitution": 'Professor Hilbert',
                                  "exam_title_substitution": 'First Exam 2022',
                                  "qrcode_data_substitution": 'tutaj znajduja sie informacje co do tego gdzie wyslac wyniki',
                                  "subtitle_substitution": 'Dzielenie'}
    question = None
    exam_draft = None

    def __init__(self, path=default_template_path):
        if "user-data" not in Path(path).parts:
            raise ValueError("The path is not valid.")
        self.path = path

    def get_path(self):
        return self.path

    def set_question(self, question):
        if not isinstance(question, Question):
            raise ValueError("Provided object is not of Question class.")

        self.question = question

    def generate_question_tex(self, exam_template_id="0", filename="es_question_tmp", raw=False, returns=True,
                              save=False):
        if not self.question:
            raise NoQuestionError("There is no question assigned.")

        if not raw:
            exam_env = Environment(
                variable_start_string='\VAR{',
                variable_end_string='}',
                loader=FileSystemLoader(Path('data') / 'exam_stencil-data' / 'templates')
            )

            exam_template = exam_env.get_template(f'exam_template-{exam_template_id}.tex')
            exam_template_output = exam_template.render(self.exam_template_substitution,
                                                        questions_substitution=[self.question.get_text()])
        else:
            exam_template_output = "\\begin{document}\n" + self.question.get_text() + "\n\\end{document}"

        if save:
            with open(Path(self.path) / f"{filename}.tex", "w") as tex_file:
                tex_file.write(exam_template_output)

        if returns:
            return exam_template_output

    def set_exam_draft(self, exam_draft):
        if not isinstance(exam_draft, ExamDraft):
            raise ValueError("The object is not of ExamDraft class.")

        self.exam_draft = exam_draft

    def generate_exam_draft_tex(self, exam_template_id="0", filename="es_exam_draft_tmp", returns=True, save=False):
        if not self.exam_draft:
            raise NoExamDraftError("There is no exam_draft to be used in generation.")

        exam_env = Environment(
            variable_start_string='\VAR{',
            variable_end_string='}',
            loader=FileSystemLoader(Path('data') / 'exam_stencil-data' / 'templates')
        )

        exam_template = exam_env.get_template(f'exam_template-{exam_template_id}.tex')
        exam_template_output = exam_template.render(self.exam_template_substitution,
                                                        questions_substitution=self.exam_draft.get_questions_text())

        if save:
            with open(Path(self.path) / f"{filename}.tex", "w") as tex_file:
                tex_file.write(exam_template_output)

        if returns:
            return exam_template_output

if __name__ == "__main__":
    # tq = TryOutQuestion("1gg5l35hj3")
    # tq.set_substitution_by_id('000')
    #
    # tq.set_text('0')
    # print(tq.get_text())
    #
    # questions = []
    #
    # question_env = Environment(
    #     variable_start_string='\VAR{',
    #     variable_end_string='}',
    #     loader=FileSystemLoader(Path("data")/"questions-data"/"1gg5l35hj3"/"templates-1gg5l35hj3")
    # )
    #
    # question_template = question_env.get_template("latextemplate-0-1gg5l35hj3.tex")
    # x = tq.get_substitution()
    # print(question_template.render({"value0":x[0], "value1":x[1], "value2":x[2]}))
    # questions.append(question_template.render({"value0":x[0], "value1":x[1], "value2":x[2]}))
    #
    # exam_env = Environment(
    #     variable_start_string='\VAR{',
    #     variable_end_string='}',
    #     loader=FileSystemLoader(Path("data")/"exam_stencil-data"/"templates")
    # )
    #
    # exam_template = exam_env.get_template("exam_template-0.tex")
    #
    # with open(Path("data")/"playground"/"exam0.tex", "w") as exam_file:
    #     exam_file.write(exam_template.render({"course_substitution":"Limon",
    #                                           "professor_substitution":"Mikel",
    #                                          "exam_title_substitution":"Math 355",
    #                                           "subtitle_substitution":"Robienie delty",
    #                                          "qrcode_data_substitution":"wysli tutaj lub tak o",
    #                                          "questions_substitution":questions}))
    #
    # doc = Document()
    # doc.append(NoEscape(exam_template.render({"course_substitution":"Limon",
    #                                           "professor_substitution":"Mikel",
    #                                          "exam_title_substitution":"Math 355",
    #                                           "subtitle_substitution":"Robienie delty",
    #                                          "qrcode_data_substitution":"wysli tutaj lub tak o",
    #                                          "questions_substitution":questions})))
    # doc.generate_pdf(filepath=Path("data")/"playground"/"doc")

    # es = ExamStencil(Path("data") / "user-data" / "playground")
    # tq = TryOutQuestion('1gg5l35hj3')
    # tq.set_substitution_by_id()
    # tq.set_text()
    # print(tq.get_text())
    # es.set_question(tq)
    #
    # p/rint(es.question.get_text())
    # print(es.generate_question_tex(save=True))

    # print(Path("data"))
    # import os
    # os.system(f"pdflatex {Path('data')/'playground'/'es_question_tmp.tex'}")

    # from copy import copy

    # ed = ExamDraft("q0l67rgm5", "trgf")
    # ed.add_question(copy(tq))
    # ed.add_question(copy(tq))
    # print(ed.get_questions_text())
    # es.set_exam_draft(copy(ed))
    # print(es.generate_exam_draft_tex())
    # es.generate_exam_draft_tex(save=True)

    print(Path("data"))
    print([str(item).split(sep='/')[-1] for item in Path("data").iterdir()])