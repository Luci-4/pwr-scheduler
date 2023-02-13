from class_course_abstraction.class_ import Class
from class_course_abstraction.course.course import Course
from class_course_abstraction.AKZ_class import AKZClass
from schedule import Schedule
from timetable import Timetable
from datafile_context import DataFileContext
from scoring_context import ScoringContext
import itertools
import os
from user_input import user_agreed
import matplotlib.pyplot as plt



class Scheduler:
    __PLOTS_DIR = "plots"
    def __init__(self, all_data_file_path: str) -> None:
        self.create_folders() 
        Timetable.clear_output_folders()
        with open(all_data_file_path, encoding="utf-8") as file:
            lines = [line.strip() for line in file]
        classes = [Class.init_from_line(line) for line in lines]
        self.classes_dict = {}
        self.courses: list[Course] = [Course.init_from_line(line) for line in lines]
        self.update_classes(classes)
        self.scoring_context = ScoringContext()

    def create_folders(self):
        Timetable.create_output_folders()
        ScoringContext.create_scoring_folder()
        os.mkdir(Scheduler.__PLOTS_DIR)

    def __course_in_courses(self, course: Course):
        for old_course in self.courses:
            if old_course.code == course.code:
                return True
        return False

    def get_all_possible_scoring_attributes_names(self):
        random_class = [i for i in self.classes_dict.values() if isinstance(i, Class)][0]
        return list(random_class.score_attributes_dict.keys())


    def update_classes(self, classes: list[Class | AKZClass]):
        for class_ in classes:
            self.classes_dict[class_.code] = class_
            if self.__course_in_courses(class_.course):
                continue
            self.courses.append(class_.course)
        

    def init_scoring_file(self, scoring_category_name: str, fields_query: str) -> None: 
        self.scoring_context.init_scoring_file(scoring_category_name, fields_query, self.classes_dict)


    @classmethod
    def clear_output_folders(cls):
        user_agreed("all of your timetables will be lost: confirm action (y/n):")
        
        Timetable.clear_output_folders()


    def __found_colisions(self, classes: list[Class]):
        class_pairs: list[tuple[Class, Class]] = list(itertools.permutations(classes, 2))

        for (class1, class2) in class_pairs:
            if class1.collides(class2):
                return True

        return False

    def grade_schedule_by_class_codes(self, class_codes: list[str]):
        return Schedule([self.classes_dict[class_code] for class_code in class_codes]).score



    def dump_to_datafile(self, schedule_index: int, end: int | None = None):
        if end is None:
            end = schedule_index+1

        schedules = self.schedules[schedule_index:end]
        for i, s in enumerate(schedules):
            assert s.index == i, f"schedule index ({s.index}) does not match its position ({i})"
            DataFileContext.dump_schedule(s)

    def dump_to_timetable(self, schedule_index: int, end: int | None = None):
        if end is None:
            end = schedule_index+1

        schedules = self.schedules[schedule_index: end]
        for i, s in enumerate(schedules):
            assert s.index == i, f"schedule index ({s.index}) does not match its position ({i})"
            s.dump_to_timetable(s.index)
        
    def __load_scores(self):
        scores_dicts = self.scoring_context.get_scores_dicts()
        for scores_dict in scores_dicts:
            self.__update_classes_scores(scores_dict)

    def __update_classes_scores(self, scores_dict: dict[str, float]):
        for class_code, score in scores_dict.items():
            
            self.classes_dict[class_code].score += score

    def __save_to_plots(self):
        plt.hist([i.score for i in self.schedules])
        plt.savefig(f"{Scheduler.__PLOTS_DIR}/score_frequency_hist.png")
        plt.clf()
        plt.plot([i.index for i in self.schedules], [i.score for i in self.schedules])
        plt.savefig(f"{Scheduler.__PLOTS_DIR}/score_by_index_plot.png")

    def plan(self, emergent_scoring_callbacks=None):
        self.__load_scores()
        if emergent_scoring_callbacks is None:
            emergent_scoring_callbacks = []

        classes_by_course_code = {course.code:[] for course in self.courses}

        for class_ in self.classes_dict.values():
            classes_by_course_code[class_.course.code].append(class_)
        sort_key_function = lambda classes_in_course: max([class_.score for class_ in classes_in_course])
        classes_by_courses_sorted_by_max_score = sorted(list(classes_by_course_code.values()), key=sort_key_function, reverse=False)

        product_result = list(itertools.product(*classes_by_courses_sorted_by_max_score))
        schedules = [Schedule(s ,emergent_scoring_callbacks) for i, s in enumerate(product_result) if not self.__found_colisions(s)]
        schedules = sorted(schedules, key=lambda s: s.score, reverse=True)

        for i, s in enumerate(schedules):
            s.index = i
        print(f"found {len(schedules)} possible schedules")
        self.schedules = tuple(schedules) 
        self.__save_to_plots()
        

