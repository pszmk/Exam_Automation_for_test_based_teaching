from abc import ABC, abstractmethod

# crate abstract class Question
class Question(ABC):
    pass

class EmptyQuestion(Question):
    pass

class ExamDraft:
    def get_variant(self, seed: str):
            return []
