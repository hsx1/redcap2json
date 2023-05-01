import pandas as pd
import jsonpickle


class Project:
    def __init__(self, in_path) -> None: 
        self.forms = {}
        self.name = []
        self.intialize_form_to_csv(in_path)

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

    def intialize_form_to_csv(self, in_path):
        df = pd.read_csv(in_path)
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

    def get_forms(self) -> list:
        return list(self.forms.keys())

    def get_questions(self) -> list:
        all_questions = []
        for _, form_content in self.forms.items():
            all_questions.append(form_content.get_questions())
        return [item for sublist in all_questions for item in sublist]
    
    def get_content(self, question) -> dict:
        for _, cform in self.forms.items():
            for cquestion in cform.questions:
                    if cquestion.name == question:
                        return cquestion.content



class Form:
    def __init__(self, name) -> None:
        self.name = name
        self.questions = []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name}: {self.questions}"

    def add_question(self, question) -> None:
        self.questions.append(question)

    def get_content(self, question) -> dict:
        for current_question in self.questions:
            if current_question.name == question:
                return current_question.content

    def get_questions(self) -> list:
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
        return f"{self.name} - {self.content}\n"

    def add_content(self, content) -> None:
        if self._type in ("radio", "checkbox", "dropdown"):
            options_str = content.split(" | ")
            for option in options_str:
                # r"(*),(*)"
                key_values = option.split(", ")
                self.content[key_values[0]] = ", ".join(key_values[1:])


def main(in_path: str, out_path: str = None):
    proj = Project(in_path)
    if out_path is not None:
        proj.save_as_json(out_path)
    return proj


if __name__ == "__main__":
    proj = main("/Users/hheinrichs/Downloads/HannahBaseline_DataDictionary_2023-04-30.csv")
    #print(proj)
    quest = "pss10_2"
    print(proj.get_content(quest))
    #print(proj)