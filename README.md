# Database Normalization
## Table of Contents
- [Objective](#objective)
- [Contributors](#contributors)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Contributing](#contributing)
- [License](#license)

## Objective:
To develop a program that takes a dataset (relation) and functional dependencies as input normalizes the relations based on the provided functional dependencies, produces SQL queries to generate the normalized database tables, and optionally determines the highest normal form of the input table.

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
3) At the end, 
