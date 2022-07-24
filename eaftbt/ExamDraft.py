from abc import ABC, abstractmethod

class NoQuestionIdError(BaseException):
    pass

class Question(ABC):
    '''
    Abstract class handling questions with general methods.
    '''
    default_substitution = {"substitution_id": None, "substitution": []}

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
            with open(Path(__file__).parent / "data" / "questions-data" / "questions-data.json") as qsdata_json:
                qsdata = json.load(qsdata_json)
                return self.question_id in qsdata["question_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with question: {self.question_id}.') as e:
            print(str(e.value))
            # print(f'Cannot find folder with data related with question: {self.question_id}.')

    def check_substitution_id(self, substitution_id):
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        import json
        from pathlib import Path
        try:
            with open(Path(__file__).parent / "data/questions-data" / f"{self.question_id}" / f"qdata-{self.question_id}.json") as qdata_json:
                qdata = json.load(qdata_json)
                return substitution_id in qdata["substitution_id_list"]
        except FileNotFoundError(f'Cannot find folder with data related with question: {self.question_id}.') as e:
            print(str(e.value))

    def set_substitution_by_id(self, substitution_id):
        '''
        Set the substitution by reference to its unique id.
        '''
        if not self.is_question_id:
            raise NoQuestionIdError("There is no question_id.")
        if not self.check_substitution_id(substitution_id):
            raise ValueError("Wrong substitution id!")

        self.substitution["substitution_id"] = substitution_id
        from pathlib import Path
        try:
            with open(Path(__file__).parent / "data" / "questions-data" / self.question_id / f'latex-{self.substitution["substitution_id"]}-{self.question_id}.txt') as latex_substitution:
                self.substitution["substitution"] = [line.strip() for line in latex_substitution if not line.startswith('#')]
        except FileNotFoundError("File with substitution not found. Substitution was reset.") as e:
            print(str(e.value))
            self.reset_substitution()

    def get_substitution(self):
        return self.substitution

    def reset_substitution(self):
        self.substitution = self.default_substitution.copy()

    def get_answer(self):
        pass

    @abstractmethod
    def set_substitution_manually(self):
        pass


class EmptyQuestion(Question):
    # question_id = None

    def set_substitution_manually(self):
        pass


class TryOutQuestion(Question):
    def set_substitution_manually(self):
        pass


class ExamDraft:
    def get_variant(self, seed: str):
        return []


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
    tq = TryOutQuestion("1gg5l35hj3")
    # tq.set_substitution_by_id('000')

    from pathlib import Path
    substitution = {"substitution_id": "111", "substitution":[]}
    try:
        with open(Path(__file__).parent / "data" / "questions-data" / "1gg5l35hj3" / f'latex-{substitution["substitution_id"]}-{"1gg5l35hj3"}.txt') as latex_substitution:
            substitution["substitution"] = [line.strip() for line in latex_substitution if
                                                 not line.startswith('#')]
    except FileNotFoundError("File with substitution not found. Substitution was reset.") as e:
        print(str(e.value))
        # self.reset_substitution()

    # print(NoQuestionIdError('Cannot find folder with data related with question:.').type())
    # print(Exception('Cannot find folder with data related with question:.').type())
    # try:
    #     1/0
    # except NoQuestionIdError('Cannot find folder with data related with question:.') as e:
    #     print(str(e.value))

    # question_id = "1gg5l35hj3"
    # r = EmptyQuestion(question_id)
    # substitution_id = "000"
    # r.set_substitution_by_id('000')
    # print(r.get_substitution())
    # print(r.question_id)
    # r.reset_substitution()
    # print(r.get_substitution())
    # tq = TestQuestion("")
    # tq = TestQuestion(question_id)
    # import json
    # from pathlib import Path
    #
    # try:
    #     with open(Path(__file__).parent / "data/questions-data" / "questions-data.json") as qdata_json:
    #         qdata = json.load(qdata_json)
    #         if question_id in qdata["question_id_list"]:
    #             print("question_id in")
    # except FileNotFoundError:
    #     pass
# from os import path
# print(path.join('eaftbt','data','1gg5l35hj3','tmp.txt'))
# with open(path.join('eaftbt','data','1gg5l35hj3','tmp.txt')) as tmp:
#     for line in tmp:
#         print(line)
