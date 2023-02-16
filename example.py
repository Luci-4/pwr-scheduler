from scheduler import Scheduler
from akz_scraping.AKZ_query_and import AKZQueryAnd
from akz_scraping.AKZ_scraper import AKZScraper
from class_course_abstraction.class_ import Class
from class_course_abstraction.AKZ_class import AKZClass

# remove result from the previous run
Scheduler.clear_output_folders()

all_classes_filepath = "siatka.csv"

# a line from a file should like like in the example below:
# K02-31a,INZ001842W,22,(C-3),Przetwarzanie strumieni danych,Dr hab. inż. Krzysztof Brzostowski,1,1,7:30,9:00,0,

# init the scheduler
scheduler = Scheduler(all_data_file_path=all_classes_filepath)

# update local file containing the akz classes
AKZScraper.scrape_all_table_rows()


# create a list of queries
queries = [
    AKZQueryAnd(
        name="turystyka", 
    ),
    AKZQueryAnd(
        name="kosz"
    ),
    AKZQueryAnd(
        name="Jezyk angielski / C1.2", 
        teacher="Morawska"
    )
]
# get search results from the queries above
akz_classes = AKZScraper.get_classes_by_queries(queries=queries)

scheduler.add_classes(akz_classes)

# choose one or more of the following attributes and create a scoring file
print(scheduler.get_all_possible_scoring_attributes_names())

# with one attribute:
scheduler.init_scoring_file("prowadzacy", "teacher")

# with a combination of attributes 
scheduler.init_scoring_file("dzien-godzina", "day, hour")
# after creating files add scores by hand in /scoring before running scheduler.plan()


# a custom scoring function that deducts points for every thursday class 
def less_classes_on_thursday(classes: list[Class]) -> float:
    score = 0
    for class_ in classes:
        # check if the class is an akz class
        if isinstance(class_, AKZClass):
            continue

        weekday = class_.time.weekday
        is_on_thursday = weekday == "Czw"
        score -= 10*is_on_thursday
    return score

# main function (might take a while to generate all possible schedules)
scheduler.plan(
    emergent_scoring_callbacks=[less_classes_on_thursday],
    required_class_codes=[],
    excluded_class_codes=[]
)

# dump from 0 to 10 schedules into timetable pdf files (output/timetables)
scheduler.dump_to_timetable(0, 10)

# dump the first result to json file that will appear in output folder
scheduler.dump_to_datafile(0)
