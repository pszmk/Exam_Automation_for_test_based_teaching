class ExamSet:
    exam_drafts = []
    structure_info = {}

    def __init__(self, exam_set_id):
        self.exam_set_id = exam_set_id
        if not self.check_exam_set_id():
            raise ValueError(f"Provided exam_set_id: {self.exam_set_id} is already used.")

    def check_exam_set_id(self):
        import json
        from pathlib import Path
        try:
            with open(Path('data')/'exam_sets-data'/'exam_sets-data.json', 'r') as essdata_json:
                essdata = json.load(essdata_json)
                return self.exam_set_id not in essdata['exam_set_id_list']
        except FileNotFoundError("File with data related with exam_sets ids not found.") as e:
            print(str(e.value))

    def get_exam_set_id(self):
        return self.exam_set_id

    def add_exam_draft(self, exam_draft):
        # if not of ExamDraft clas raise ValueError
        self.exam_drafts.append(exam_draft)

    def get_exam_drafts(self):
        return self.exam_drafts

    def remove_exam_draft(self, exam_draft_index):
        if exam_draft_index not in range(len(self.exam_drafts)):
            raise ValueError("Prodived index is out of range.")

        self.exam_drafts.pop(exam_draft_index)

    def save_exam_set(self):
        pass

    def get_structure_info(self):
        import json
        from pathlib import Path
        try:
            with open(Path("data")/'exam_sets-data'/self.exam_set_id/f'esdata-{self.exam_set_id}','r') as info_file_json:
                return json.load(info_file_json)
        except FileNotFoundError(f"File with data related with exam_set: {self.exam_set_id} not found.") as e:
            print(str(e.value))

if __name__ == '__main__':
    pass