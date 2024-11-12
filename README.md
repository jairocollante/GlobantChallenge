# GlobantChallenge
Challenge create by Globant company

##Challenge #1
You are a data engineer at Globant and you are about to start an important project. This project
is big data migration to a new database system. You need to create a PoC to solve the next
requirements:

To resolve this challenge I made the following enviroments:
 * SO = Windows 11
 * IDE = Visual Code
 * REST python framework = Django
 * API REST = rest_framework library
 * Git local = Git bash
 * Database = SQLITE3

Develop

1. Move historic data from files in CSV format to the new database.

  Solution.
     * To copy data from CSV file to SQLITE I created ./historicalData folder to store CSV sources and load_history.py
     * To perform load data is needed locate in ./historicalData and execute "python load_history.py"

2. Create a Rest API service to receive new data. This service must have:

    Solution.
        * http://localhost:8000/challenge1/new_data/

2.1. Each new transaction must fit the data dictionary rules.

    Solution.
        * I create Django.MODELS as each CSV files to ensure data fit. 

2.2. Be able to insert batch transactions (1 up to 1000 rows) with one request.

    Solution.
        * I create a validation when Request is recived 
            if (1 <= len(request.data) <= 1000):

2.3. Receive the data for each table in the same service.

    Solution.
        * I check serialize data request based in django.MODEL to figurate the match model

2.4. Keep in mind the data rules for each table.

    Solution.
        * django.MODEL ensure model rules.

3. Create a feature to backup for each table and save it in the file system in AVRO format.

    Solution.
        * I create http://localhost:8000/challenge1/backup/ to perform view.py/backup(request)
        * Before method to create one file .avro for each table into /backupData folder. 


4. Create a feature to restore a certain table with its backup.

    Solution.
        * I create http://localhost:8000/challenge1/restore/ to perform view.py/restore(request)
        * Before method to recovery one file .avro for each table into /backupData folder.

You need to publish your code in GitHub. It will be taken into account if frequent updates are made to the repository that allow analyzing the development process.

    Solution.
        *  https://github.com/jairocollante/Globant_challenge.git


Clarifications
● You decide the origin where the CSV files are located.

    Solution.
        * Files located inside Django project in /challange1/historicalData

● You decide the destination database type, but it must be a SQL database.

    Solution.
        * BD located inside Django project, type SQLITE, file db.sqlite3

● The CSV file is comma separated.
● "Feature" must be interpreted as "Rest API, Stored Procedure, Database functionality,
Cron job, or any other way to accomplish the requirements".

    Solution.
        * I choose REST API

Not mandatory, but taken into account:
● Create a markdown file for the Readme.md

    Solution.
        * Created inside project.

● Security considerations for your API service

● Use the Git workflow to create versions

    Solution.
        * Applied

● Create a Dockerfile to deploy the package

    Solution.
        * Created

● Use cloud tools instead of local tools You can use Python, Java, Go or Scala to solve it!

    Solution.
        * Github

Data Rules
● Transactions that don't accomplish the rules must not be inserted but they must be logged.

    Solution.
        * I create a Logger Table where I record Transactions that don't accomplish

● All the fields are required.

    Solution.
        * Applied 


##Challenge #2
You need to explore the data that was inserted in the first challenge. The stakeholders ask for some specific metrics they need. You should create an end-point for each requirement.
Requirements:

1. Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.
    
    Solution.
        *   SELECT d.department,j.job,count(*),h.datetime,
            CASE 
                WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
                WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
                WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
                WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 10 AND 12 THEN 'Q4'
            END AS 'quarter'
            FROM challenge1_hiredemployee h, challenge1_department d, challenge1_job j
            WHERE h.department_id = d.id
            AND h.job_id = j.id
            AND substr(h.datetime,0,5) = '2021'
            GROUP BY d.department,j.job
            ORDER BY d.department,j.job DESC;


2. List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).

    Solution.
        *   SELECT h.department_id, d.department, count(h.id)
            FROM challenge1_hiredemployee h, challenge1_department d
            WHERE h.department_id = d.id 
            AND substr(h.datetime,0,5) = '2021'
            GROUP BY h.department_id
            HAVING count(h.id) > (
                    SELECT AVG( department_count )
                    FROM (
                        SELECT count(h.id) AS department_count
                        FROM challenge1_hiredemployee h
                        WHERE substr(h.datetime,0,5) = '2021'
                        GROUP BY h.department_id ) )
            ORDER BY count(h.id) DESC




