from abc import ABC, abstractmethod
from pathlib import Path

path_eaftbt_data = Path(__file__).parent / "data"
# path_user_data =

class NoQuestionIdError(BaseException):
    pass

class UsedExamIdError(BaseException):
    pass

class Question(ABC):
    '''
    Abstract class handling questions with general methods.
    '''
    default_substitution = {"substitution_id": None, "substitution": [], "answer": []}

    def __init__(self, question_id):
        self.question_id = question_id
        self.is_question_id = self.check_question_id()
        if not self.is_question_id:
            raise NoQuestionIdError("Provided question_id is not valid.")
        self.substitution = self.default_substitution.copy()
        self.text = None


    def check_question_id(self):
        import json
        # from pathlib import Path
        try:
            with open(path_eaftbt_data/"questions-data"/"questions-data.json") as qsdata_json:
                qsdata = json.load(qsdata_json)
                return self.question_id in qsdata["question_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with questions including: {self.question_id}.') as e:
            print(str(e.value))

    def set_text(self, template_id="0"):
        # from pathlib import Path
        from jinja2 import Environment, FileSystemLoader
        try:
            with open(path_eaftbt_data / "questions-data" / self.question_id / f"templates-{self.question_id}"/f"latextemplate-{template_id}-{self.question_id}.tex") as x:
                env = Environment(
                    variable_start_string='\VAR{',
                    variable_end_string='}',
                    loader=FileSystemLoader(path_eaftbt_data / "questions-data" / self.question_id / f"templates-{self.question_id}"))
                template = env.get_template(f"latextemplate-{template_id}-{self.question_id}.tex")
                self.text = template.render(substitution=self.substitution['substitution'])
        except FileNotFoundError(f'Cannot find folder with templates related with question: {self.question_id}.') as e:
            print(str(e.value))

    def get_text(self):
        return self.text

    # def get_example(self, example_id):
    #     pass

    def check_substitution_id(self, substitution_id):
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        import json
        from pathlib import Path
        try:
            with open(path_eaftbt_data/"questions-data"/f"{self.question_id}"/f"qdata-{self.question_id}.json") as qdata_json:
                qdata = json.load(qdata_json)
                return substitution_id in qdata["substitution_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with question: {self.question_id}.') as e:
            print(str(e.value))

    @abstractmethod
    def set_substitution_by_id(self, substitution_id="000"):
        pass

    @abstractmethod
    def set_substitution_manually(self):
        pass

    def get_substitution(self):
        return self.substitution["substitution"]

    def reset_substitution(self):
        self.substitution = self.default_substitution.copy()

    def get_answer(self):
        return self.substitution["answer"]


class TryOutQuestion(Question):

    def set_substitution_by_id(self, substitution_id="000"):
        '''
        Set the substitution by reference to its unique id.
        '''
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        if not self.check_substitution_id(substitution_id):
            raise ValueError("Wrong substitution id!")

        self.substitution["substitution_id"] = substitution_id
        import json
        # from pathlib import Path
        try:
            with open(
                    path_eaftbt_data/ "questions-data" / self.question_id / "sub-1gg5l35hj3" / f'latex-{self.substitution["substitution_id"]}-{self.question_id}.txt') as latex_substitution:
                self.substitution["substitution"] = [line.strip() for line in latex_substitution if
                                                     not line.startswith('#')]
            with open(
                    path_eaftbt_data/ "questions-data" / self.question_id / "sub-1gg5l35hj3" / f'sdata-{self.substitution["substitution_id"]}-{self.question_id}.json') as sdata_json:
                sdata = json.load(sdata_json)
                self.substitution["answer"] = sdata["possible_answers"]
        except FileNotFoundError("File with substitution not found. Substitution was reset.") as e:
            print(str(e.value))
            self.reset_substitution()

    def set_substitution_manually(self):
        pass


class ExamDraft:
    def __init__(self, exam_set_id, exam_id):
        self.questions = []
        self.exam_draft = {}
        self.exam_set_id = exam_set_id
        self.exam_id = exam_id
        if self.check_exam_id():
            raise UsedExamIdError(f"The exam_id: {self.exam_id} is already used.")

    def check_exam_id(self):
        import json
        # from pathlib import Path
        try:
            with open(path_eaftbt_data/"user-data"/'exam_sets-data'/self.exam_set_id/f'esdata-{self.exam_set_id}.json', 'r') as esdata_json:
                esdata = json.load(esdata_json)
                return self.exam_id in esdata['exam_id_list']
        except FileNotFoundError(f"File with data related with exam_set: {self.exam_set_id} not found.") as e:
            print(str(e.value))

    def get_exam_id(self):
        return self.exam_id

    def add_question(self, question):
        if not isinstance(question, Question):
            raise ValueError("The object provided is not of Question class.")

        self.questions.append(question)

    def remove_question(self, question_index):
        if question_index not in range(len(self.questions)):
            raise ValueError("Provided question_index is not within the expected range.")

        self.questions.pop(question_index)

    # def get_exam_draft(self):
    #     pass

    def save_exam_draft(self):
        pass

    def import_exam_draft(self):
        pass

    def get_questions_text(self):
        return [one_question.get_text() for one_question in self.questions]

def compare_paths():
    from pathlib import Path
    return Path(__file__)

if __name__ == '__main__':
    '''
    Trying out Path from pathlib which will be used temporarily to handle file manipulation
    '''
    from pathlib import Path

    print(Path.cwd())
    print(Path(__file__))
    print(Path(__file__).parent)
    print(Path(__file__).parent.parent / "data")
    '''
    Trying out jinja2
    '''
    question_id_test_1 = "1gg5l35hj3"
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id('000')
    # print(tq.get_substitution()[0])
    from pathlib import Path
    from jinja2 import Environment, FileSystemLoader
    templates_path = Path(__file__).parent/'data' / 'questions-data' / '1gg5l35hj3' / 'templates-1gg5l35hj3'

    latex_jinja_env = Environment(
        variable_start_string='\VAR{',
        variable_end_string='}',
        loader=FileSystemLoader(templates_path)
    )

    # latex_template = latex_jinja_env.get_template('latextemplate-0-1gg5l35hj3.tex')
    # print(latex_template.render({'value0':tq.get_substitution()[0], 'value1':tq.get_substitution()[1], 'value2':tq.get_substitution()[2]}))
    # dkd = latex_template.render({'value0':tq.get_substitution()[0], 'value1':tq.get_substitution()[1], 'value2':tq.get_substitution()[2]})
    # with open(Path('data') / 'exam_sets-data' / 'q0l67rgm5' / 'tmp.tex', 'w') as latex_out:
    #     latex_out.write(dkd)

    ''''''
    # import json
    # from pathlib import Path
    # exam_id = 'ii'
    # try:
    #     with open(Path('data') / 'exam_sets-data' / 'q0l67rgm5' / f'esdata-q0l67rgm5.json',
    #               'r') as esdata_json:
    #         esdata = json.load(esdata_json)
    #         print(esdata)
    #         print(exam_id in esdata['exam_id_list'])
    # except FileNotFoundError("File with data related with exam_sets not found.") as e:
    #     print(str(e.value))
    #
    # ed = ExamDraft('q0l67rgm5', 'erer')
    # print(ed.questions)
    # print(len(ed.questions))

    # es = ExamSet('q0l67rgm5')
    # es2 = ExamSet('eees')
    # print(es.get_exam_set_id())
    # print(es.check_exam_set_id())
    # print(es2.check_exam_set_id())
    question_id_test_1 = "1gg5l35hj3"
    # with Environment(variable_start_string='\VAR{', variable_end_string='}', loader=FileSystemLoader(Path("data") / "questions-data" / question_id_test_1 / f"templates-{question_id_test_1}")) as env:
    #     template = env.get_template(f"latextemplate-{'0'}-{question_id_test_1}.tex")
    #     text = template.render(substitution=['1','3'])
    #     print(text)

    # env = Environment(variable_start_string='\VAR{', variable_end_string='}', loader=FileSystemLoader(Path("data") / "questions-data" / question_id_test_1 / f"templates-{question_id_test_1}"))
    # with Environment(variable_start_string='\VAR{', variable_end_string='}', loader=FileSystemLoader(Path("data") / "questions-data" / question_id_test_1 / f"templates-{question_id_test_1}")) as env:
    #     template = env.get_template(f'latextemplate-0-{question_id_test_1}.tex')
    #     print(template.render(substitution=['1', '3']))
    # template = env.get_template(f'latextemplate-0-{question_id_test_1}.tex')
    tq = TryOutQuestion(question_id_test_1)
    tq.set_substitution_by_id()
    print(tq.get_substitution())
    tq.set_text()
    print(tq.get_text())
    with open(Path("data")/"user-data"/"playground"/"mikos2.tex", "w") as mikos2_file:
        mikos2_file.write(tq.get_text())