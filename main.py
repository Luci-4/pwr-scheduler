from scheduler import Scheduler
from AKZ_scraper_field_query import AKZFieldQuery
from AKZ_scraper import AKZScraper

# remove result from the previous run
Scheduler.clear_output_folders()

all_classes_filepath = ""
# init the scheduler
scheduler = Scheduler(all_data_file_path=all_classes_filepath)

# search by query and update classes with those from AKZ
# attributes of this query are optional
# when both present they form a conjunction of inclusion clauses

field_query = AKZFieldQuery(
    name="Jezyk angielski / C1.2", 
    teacher="Morawska"
)
akz_classes = AKZScraper.get_classes_by_field_query(field_query)
scheduler.update_classes(akz_classes)

# choose one or more of the following attributes and create a scoring file
print(scheduler.get_all_possible_scoring_attributes_names())

# with one attribute:
scheduler.init_scoring_file("prowadzacy", "teacher")

# with a combination of attributes 
scheduler.init_scoring_file("dzien-godzina", "day, hour")
# after creating files add scores by hand in /scoring before running scheduler.plan()


# main function (might take a while to generate all possible schedules)
scheduler.plan()

# dump from 0 to 10 schedules into timetable pdf files (output/timetables)
scheduler.dump_to_timetable(0, 10)

# dump the first result to json file that will appear in output folder
scheduler.dump_to_datafile(0)
