import os
from class_course_abstraction.class_ import Class
from user_input import user_agreed

class ScoringContext:
    __SCORING_IDENTIFIERS_SEPARATOR = "|"
    __SCORING_DIR = "scoring"

    def __init__(self) -> None:
        self.scoring_files = [] 


    @classmethod
    def create_scoring_folder(cls):
        os.mkdir(cls.__SCORING_DIR)

    def init_scoring_file(self, scoring_category_name: str, fields_query: str, classes_dict) -> None: 
        fields = [field.strip() for field in fields_query.split(",")]
        filename = f"{scoring_category_name}_scores.txt"
        values_sorted = [c.get_score_attrs_values_with_identifier(fields) for c in sorted(classes_dict.values(), key=Class.sort_callback_by_code)]
        identifiers_by_values_formated = {}
        for identifier, *values in values_sorted:
            values_key = tuple(values)
            if not (values_key in identifiers_by_values_formated):
                identifiers_by_values_formated[tuple(values)] = []
            identifiers_by_values_formated[tuple(values)].append(identifier)
        lines_formated = [f"{ScoringContext.__SCORING_IDENTIFIERS_SEPARATOR.join(identifiers)},{','.join([str(v) for v in attr_values])}," for (attr_values, identifiers) in identifiers_by_values_formated.items()]

        filepath = f"{ScoringContext.__SCORING_DIR}/{filename}"
        if os.path.isfile(filepath):
            if not user_agreed(f"{filepath} scoring file already exist. overwrite? (y/n):"):
                return
        self.__create_scoring_file(filepath, lines_formated)
        self.scoring_files.append(filename)

    def get_scores_dicts(self):    
        scoring_files = [f for f in os.listdir(ScoringContext.__SCORING_DIR) if os.path.isfile(os.path.join(ScoringContext.__SCORING_DIR, f))]
        return [self.__load_from_scoring_file(file) for file in scoring_files]

    def __load_from_scoring_file(self, filename: str):
        with open(f"{ScoringContext.__SCORING_DIR}/{filename}", encoding="utf-8") as file:
            lines = [l.strip() for l in file]
        return self.__parse_lines_to_scores_by_class_code(lines)

    def __parse_lines_to_scores_by_class_code(self, lines: list[str]):
        lines_split = [l.split(",") for l in lines]
        
        scores_str_by_codes = {tuple(l[0].split(ScoringContext.__SCORING_IDENTIFIERS_SEPARATOR)): l[-1] for l in lines_split}
        scores_str_by_code = {}

        for codes, score in scores_str_by_codes.items():
            for code in codes:
                scores_str_by_code[code] = score
    
        scores = {code: self.__parse_score_to_float(score_str) for code, score_str in scores_str_by_code.items()}
        return scores
        
    @staticmethod
    def __create_scoring_file(filepath: str, lines_formated: list[str]):
        with open(filepath, "w+", encoding="utf-8") as file:
            file.write("\n".join(lines_formated))

    @staticmethod
    def __parse_score_to_float(str_score):
        return 0 if not str_score.strip() else float(str_score)
