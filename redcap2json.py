import pandas as pd
import jsonpickle


class Project:
    def __init__(self, codebook_path) -> None:
        self.forms = {}
        self.name = []
        self.intialize_form_to_csv(codebook_path)

    def __repr__(self) -> str:
        """Recursively calls string methods of lower-level objects"""
        return self.__str__()

    def __str__(self) -> str:
        output = []
        for value in self.forms.values():
            output.append(value)
        return f"Project: {self.name}\n\nForms:\n{output}\n"

    def to_json(self) -> str:
        return jsonpickle.encode(self)

    def save_as_json(self, filepath):
        with open(filepath, "w") as text_file:
            text_file.write(self.to_json())

    def intialize_form_to_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            form_name = row["Form Name"]
            # select or if not existent create form
            if not form_name in self.forms:
                self.forms[form_name] = Form(name=form_name)

            question = Question(
                name=row["Variable / Field Name"],
                _type=row["Field Type"],
                label=row["Field Label"],
                content=row["Choices, Calculations, OR Slider Labels"]
            )

            self.forms[form_name].add_question(question)

    def get_forms(self):
        return list(self.forms.keys())

    def get_qustions(self):
        all_questions = []
        for _, form_content in self.forms.items():
            all_questions.append(form_content.get_questions())
        return [item for item in sublist for sublist in all_questions]


class Form:
    def __init__(self, name) -> None:
        self.name = name
        self.questions = []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name}: {self.questions}"

    def add_question(self, question):
        self.questions.append(question)

    def get_content(self, question) -> dict:
        for question in self.questions:
            if question.name == question:
                return question.content

    def get_questions(self):
        # map or lambda method to get names of all Question objects
        return list(map(lambda x: x.name, self.questions))


class Question:
    def __init__(self, name, _type, label, content) -> None:
        self.name = name
        self._type = _type
        self.label = label
        self.content = {}
        self.add_content(content)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} - {self.content} "

    def add_content(self, content) -> None:
        if self._type in ("radio", "checkbox", "dropdown"):
            options_str = content.split(" | ")
            for option in options_str:
                # r"(*),(*)"
                key_values = option.split(", ")
                self.content[key_values[0]] = ", ".join(key_values[1:])


filepath = "/Users/hheinrichs/Downloads/Civibescreening_DataDictionary_2023-04-30.csv"
proj = Project(filepath)
proj.save_as_json("/Users/hheinrichs/Downloads/test.json")


language_options = proj.forms["online_screening_consent_form"].get_question(
    name="screening_language")
# print(language_options)
print(proj.get_qustions())
