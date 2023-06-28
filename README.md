# PWR Scheduler

The PWR Scheduler Python Program is a customizable tool that helps to optimize a schedule for Wrocław University of Science and Technology. This program utilizes straighforward techniques to generate the most efficient schedule based on specific, user-provided requirements and constraints.

## Features

- Optimization: The program employs advanced optimization algorithms to find the best schedule based on specified objectives and constraints.
- Customizable Inputs: Users can customize input parameters such as personal lecturer preference, preferable time slots and weekdays, degree of synchronization with some external schedule and many more, thanks to the option of providing a custom cost function that modifies the overall score of the optimization result.
- Visualization: The program provides visual representations of the optimized schedule in a form of a pdf timetable

## Prerequisites

To run the Schedule Optimization Python Program, ensure that you have the following:

- Python 3.x: You can download and install Python from the official website: [python.org](https://www.python.org/downloads/).
- Required Packages: The program relies on specific packages and dependencies, which are listed in the `requirements.txt` file. To install these packages, navigate to the program's directory and run the following command:

  ```bash
  pip install -r requirements.txt
  ```

  This will install all the required packages and their dependencies, preferably within a virtual environment. Make sure to update the `requirements.txt` file if you add or modify any dependencies in the program.
Certainly! Here's an updated version with a table showing the required columns in the README:

## Usage

1. Prepare Input Data: For security reasons, this program does not make use of students academic login and password. Due to this fact a manual input data entry is required. Create a CSV file containing the input data required for the scheduling process. The CSV file should have the following columns:

    | Columns                                                  |
    | ------------------------------------------------------------ |
    | Code representing a group or section.                        |
    | Code representing a course.                                   |
    | Name or ID of the classroom where the course will be held.    |
    | Name or ID of the building where the classroom is located.    |
    | Name of the course.                                          |
    | Name of the teacher or instructor.                            |
    | Number assigned to the group or section.                      |
    | Total number of groups or sections in the course.             |
    | Start time of the course or activity.                         |
    | End time of the course or activity.                           |
    | Index representing the day of the week (0-6, where 0 represents Monday and 6 represents Sunday). |

    Ensure that the CSV file follows the specified column format and contains the necessary data for scheduling. 

2. Example Usage: The program repository includes an example.py file that demonstrates the usage of the Schedule Optimization Python Program. You can use this file as a starting point or reference for integrating the program into your own projects.

3. Run the Program: Execute the Python script or command to run the program, providing the path to the input CSV file as an argument. For example:

   ```bash
   python example.py
   ```

    Replace `example.py` with the actual program file name.

4. Review the Schedule: Once the program completes, analyze the generated schedule(s) pdf files in the created ./output/timetables directory. 

5. Refine and Iterate: If necessary, adjust the program parameters to further improve the schedule. Repeat steps 3 and 4 until you achieve a satisfactory and optimal schedule.

## License

This program is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to contribute enhancements or bug fixes, please open an issue or submit a pull request on the [GitHub repository](https://github.com/username/schedule-optimization-python-program).
