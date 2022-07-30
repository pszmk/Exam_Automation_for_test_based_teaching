from abc import ABC, abstractmethod

class NoQuestionIdError(BaseException):
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

    def check_question_id(self):
        import json
        from pathlib import Path
        try:
            with open(Path(__file__).parent/"data"/"questions-data"/"questions-data.json") as qsdata_json:
                qsdata = json.load(qsdata_json)
                return self.question_id in qsdata["question_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with question: {self.question_id}.') as e:
            print(str(e.value))

    def get_text(self):
        pass

    def check_substitution_id(self, substitution_id):
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        import json
        from pathlib import Path
        try:
            with open(Path(__file__).parent/"data"/"questions-data"/f"{self.question_id}"/f"qdata-{self.question_id}.json") as qdata_json:
                qdata = json.load(qdata_json)
                return substitution_id in qdata["substitution_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with question: {self.question_id}.') as e:
            print(str(e.value))

    @abstractmethod
    def set_substitution_by_id(self, substitution_id):
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


# class EmptyQuestion(Question):
#     question_id = None
    #
    # def set_substitution_manually(self):
    #     pass


class TryOutQuestion(Question):

    def set_substitution_by_id(self, substitution_id):
        '''
        Set the substitution by reference to its unique id.
        '''
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        if not self.check_substitution_id(substitution_id):
            raise ValueError("Wrong substitution id!")

        self.substitution["substitution_id"] = substitution_id
        import json
        from pathlib import Path
        try:
            with open(
                    Path(__file__).parent / "data" / "questions-data" / self.question_id / "sub-1gg5l35hj3" / f'latex-{self.substitution["substitution_id"]}-{self.question_id}.txt') as latex_substitution:
                self.substitution["substitution"] = [line.strip() for line in latex_substitution if
                                                     not line.startswith('#')]
            with open(
                    Path(__file__).parent / "data" / "questions-data" / self.question_id / "sub-1gg5l35hj3" / f'sdata-{self.substitution["substitution_id"]}-{self.question_id}.json') as sdata_json:
                sdata = json.load(sdata_json)
                self.substitution["answer"] = sdata["possible_answers"]
        except FileNotFoundError("File with substitution not found. Substitution was reset.") as e:
            print(str(e.value))
            self.reset_substitution()

    def set_substitution_manually(self):
        pass


class ExamDraft:
    questions = []

    def __init__(self, exam_id):
        self.exam_id = exam_id
        pass

    def get_exam_id(self):
        return self.exam_id

    def add_question(self, question):
        # if type(question) is not right:
        #     raise cos tam error
        self.questions.append(question)

    def remove_question(self, question_index):
        self.questions.pop(question_index)

    def get_exam_draft(self):
        pass

    def save_exam_draft(self):
        pass

    def import_exam_draft(self):
        pass

    # def
    # def get_variant(self, seed: str):
    #     return []


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
    Pre-testing EmptyQuestion 
    '''
    dd = TryOutQuestion("1gg5l35hj3")
    print(str(type(dd)))

    question_id_test_1 = "1gg5l35hj3"
    exam_id_test_1 = "yyisjdfsd7544"

    tq1 = TryOutQuestion(question_id_test_1)
    tq2 = TryOutQuestion(question_id_test_1)
    tq2.set_substitution_by_id("000")
    ed = ExamDraft(exam_id_test_1)
    ed.add_question(tq1)
    ed.add_question(tq2)
    # assert ed.questions == [tq1, tq2]
    print(ed.questions == [tq1, tq2])

    tq3 = TryOutQuestion(question_id_test_1)
    ed.add_question(tq3)
    print(ed.questions == [tq1, tq2, tq3])

    ed.questions[2].set_substitution_by_id("000")
    print(ed.questions == [tq1, tq2, tq3])
    print(tq3.substitution == {"substitution_id" : "000", "substitution" : ['\\frac{2}{5}\\frac{3}{7}', '4'], "answer": ["0.666", "0.667"]})
