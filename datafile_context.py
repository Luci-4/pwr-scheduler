from schedule import Schedule
from json import load as json_load, dump as json_dump, decoder

class DataFileContext:
    __DATAFILEPATH = "output/datafile.json"

    @classmethod
    def loaded_json_dict(file_path: str) -> dict:
        try:
            with open(file_path, encoding="utf-8") as file:
                data = json_load(file)
        except FileNotFoundError:
            exit("file not found")
        except decoder.JSONDecodeError:
            exit("parsing error")
        else:
            return data

    @classmethod
    def dump_schedule(cls, schedule: Schedule):
        data = cls.__get_datafile_contents()
        data[str(schedule.index)] = {"score": schedule.score, "class_codes": schedule.class_codes}
        with open(cls.__DATAFILEPATH, "w+", encoding="utf-8") as file:
            json_dump(data, file,  indent=4)

    @classmethod
    def __get_datafile_contents(cls):
        try:
            result = cls.__try_to_get_datafile_contents()
        except FileNotFoundError:
            return {}
        else:
            return result

    @classmethod
    def __try_to_get_datafile_contents(cls):
        with open(cls.__DATAFILEPATH, encoding="utf-8") as file:
            data = json_load(file)
        return data