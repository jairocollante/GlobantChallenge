from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic


from django.db import connection

# Create your views here.

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



def employees_quarter(request):
    query = "SELECT d.department,j.job,count(*) AS employees,\
                CASE \
                    WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1' \
                    WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2' \
                    WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3' \
                    WHEN CAST(SUBSTR(datetime, 6, 2) AS INTEGER) BETWEEN 10 AND 12 THEN 'Q4' \
                END AS 'quarter' \
                FROM challenge1_hiredemployee h, challenge1_department d, challenge1_job j \
                WHERE h.department_id = d.id \
                AND h.job_id = j.id \
                AND substr(h.datetime,0,5) = '2021' \
                GROUP BY d.department,j.job \
                ORDER BY d.department,j.job DESC"


    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)

    print(rows)

    data = {'rows':rows}

    return render(request,'challenge2/_list.html',data);



def employees_hired(request):

    query = "SELECT h.department_id, d.department, count(h.id) AS hired \
            FROM challenge1_hiredemployee h, challenge1_department d \
            WHERE h.department_id = d.id \
            AND substr(h.datetime,0,5) = '2021' \
            GROUP BY h.department_id \
            HAVING count(h.id) > ( \
                    SELECT AVG( department_count ) \
                    FROM ( \
                        SELECT count(h.id) AS department_count \
                        FROM challenge1_hiredemployee h \
                        WHERE substr(h.datetime,0,5) = '2021' \
                        GROUP BY h.department_id ) ) \
            ORDER BY count(h.id) DESC"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)

    print(rows)

    data = {'rows':rows}

    return render(request,'challenge2/_list2.html',data);
