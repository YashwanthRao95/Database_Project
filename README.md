# Database Normalization
## Table of Contents
- [Objective](#objective)
- [Contributors](#contributors)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Core Components](#core-components)
- [Assumptions](#assumptions)
- [Contact](#contact)

## Objective:
To develop a program that takes a dataset (relation) and functional dependencies as input normalizes the relations based on the provided functional dependencies, produces SQL queries to generate the normalized database tables, and optionally determines the highest normal form of the input table.</br>
To know more about normalizations, suggest reading : [Intoduction of Database Normalization - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-database-normalization/?ref=lbp)

## Contributors:
- Yashwanth Rao, Gujja (yg7bh@umsystem.edu)</br>
- Amarnath, Narne</br>
- Raja, N</br>
- Sai Krishna, P</br>
- Likith</br>

## Inputs
1) The input relation data must be mentioned in the _**'exampleInputTable.csv'**_ file.
2) The function dependencies must be mentioned in the _**'dependencies.txt'**_ file (eg: _'StudentID -> FirstName, LastName'_).
3) If any multi-valued dependencies are to be mentioned, please use the _**'mvd_dependencies.txt'**_ file (eg: _'Course ->> Professor'_).
4) The _**'key (primary key)'**_ is user input, and it needs to be _comma-separated_ in case of composite key (eg: '_StudentID, Course_').
5) The **'Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF)'** is a user input (eg: 4).
6) **' Find the highest normal form of the input table? (1: Yes, 2: No)'** is a user input (eg: 1).
7) For 5NF, each of the relations needs _candidate keys_ (user input) in the form _'(A, B), (C, D)'_.
</br>
NOTE: Please ensure all the keys are entered in the format mentioned above. It is necessary for the proper functioning of code.

## Outputs
1) The input relation shall pass through each of the normalization forms until it reaches the highest normal form asked for.
2) At every stage, it shall check if the relation follows the normalization form and outputs the normalized tables with data otherwise.
3) At the required highest normal form, the program shall quit and output the _**'CREATE TABLE <table-name> ...'**_ queries for the normalized tables.
4) At the very end, based on the user input, the highest normal form of the input table is either displayed or not.

## Core Components
1) [main.py](/main.py): This file is the _**main file to be executed**_. All the inputs are redirected accordingly from here.
2) [input_parser.py](/input_parser.py): This file is used to parse the inputs from the csv file, txt files, and user inputs, for further use in the program.
3) [normalizations.py](/normalizations.py): This file contains the entire logic of normalizations from 1NF, all to way to 5NF.
4) [output_generator.py](/output_generator.py): This file is used to generate the required SQL query by taking in the normalized tables as input.

## Assumptions
1) It is assumed that the user has python >= 3.9 installed and an environment created to execute this program.
2) It is assumed that the user has installed the required libraries are pre-installed. (pandas, numpy, etc,.)
3) It is assumed that the user shall input the required inputs in the format mentioned and will not deviate from it.
</br>
NOTE: Please run the default example with the provided key (StudentID, Course), and highest normal form (4) to get acquainted with the workings of this program.

## Contact
In case of any query regarding the program and its working, please reach out to [yg7bh@umsystem.edu](mailto:yg7bh@umsystem.edu).
