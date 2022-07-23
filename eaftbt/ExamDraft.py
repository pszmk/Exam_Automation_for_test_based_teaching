from abc import ABC, abstractmethod


class Question(ABC):
    '''
    Abstract class with general methods.
    '''
    default_substitution = {"id": None, "substitution": []}

    def __init__(self, question_id):
        # self.questions_path = questions_path
        self.question_id = question_id
        self.check_question_id()
        self.substitution = self.default_substitution.copy()

    def check_question_id(self):
        import json
        from pathlib import Path
        try:
            with open(Path(__file__).parent / "data/questions-data" / "questions-data.json") as qdata_json:
                qdata = json.load(qdata_json)
                if not self.question_id in qdata["question_id_list"]:
                    # raise error
                    print('check_question_id wrong id of the question')
        except:
            # raise error
            print('check_question_id oops')

    def set_substitution_by_id(self, substitution_id):
        '''
        Set the substitution by reference to its unique id.
        '''
        # if substitution_id == "" or not self.check_substitution_id():
            # raise error
            # pass
        from pathlib import Path
        try:
            self.substitution["id"] = substitution_id
            with open(
                    Path(
                        __file__).parent / "data/questions-data" / self.question_id / f'latex-{self.substitution["id"]}-{self.question_id}.txt') as latex_substitution:
                self.substitution["substitution"] = [line.strip() for line in latex_substitution if
                                                     not line.startswith('#')]
        except:
            self.reset_substitution()
            # raise error
            # tutaj ma byc error ze nie ma sciezki
            print(["szkoda"])
            pass

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
    question_id = None

    def set_substitution_manually(self):
        pass


class TestQuestion(Question):
    question_id = None

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
    question_id = "1gg5l35hj3"
    r = EmptyQuestion(question_id)
    substitution_id = "000"
    r.set_substitution_by_id('000')
    print(r.get_substitution())
    print(r.question_id)
    r.reset_substitution()
    print(r.get_substitution())
# from os import path
# print(path.join('eaftbt','data','1gg5l35hj3','tmp.txt'))
# with open(path.join('eaftbt','data','1gg5l35hj3','tmp.txt')) as tmp:
#     for line in tmp:
#         print(line)
