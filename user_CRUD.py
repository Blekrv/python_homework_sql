import psycopg2
from config import *
from psycopg2 import Error
try:
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database='user_db')

    cursor = connection.cursor()
    cursor.execute('SELECT VERSION()')

    # ------------------------------------------------------
    task1 = """
        select first_name,last_name
        from employee e 
        where e.city_id in
        (select id from city c where c.city_name = 'London' );
    """
    cursor.execute(task1)
    show = cursor.fetchall()
    print(show)
    # ----------------------------------------------
    task2 = """
        select first_name,last_name
        from employee e 
        where first_name  like 'Z%';
    """
    cursor.execute(task1)
    show = cursor.fetchall()
    print(show)
    # --------------------------------------------
    task3 = """
        select first_name,last_name, extract(year from now())- extract(year from date_of_birth) as "Age" from employee e 
        where extract(year from e.date_of_birth) < (extract(year from now()) - 55 )
        order by last_name;
    """
    cursor.execute(task3)
    show = cursor.fetchall()
    print(show)
    # -------------------------------------------------
    task4 = """
        select min(extract(year from now())- extract(year from date_of_birth)) as "minimal age",
        max(extract(year from now())- extract(year from date_of_birth)) as "maximum age",
        avg(extract(year from now())- extract(year from date_of_birth)) as "average age" 
        from employee e where e.city_id in (select id from city c where c.city_name = 'London');
    """
    cursor.execute(task4)
    show = cursor.fetchall()
    print(show)
    # ----------------------------------------------------------------
    task5 = """
        select city_name,round(avg(extract (year from now())- extract(year from e.date_of_birth)))  from city c
        left join employee e on c.id =e.city_id  
        group by city_name having round(avg(extract (year from now())- extract(year from e.date_of_birth)))>=30;
    """
    cursor.execute(task5)
    show = cursor.fetchall()
    print(show)
    # ---------------------------
    task6 = """
        select first_name, last_name, extract(year from now())- extract(year from date_of_birth) as age
        from ( 
          select first_name, last_name, date_of_birth,
                 dense_rank() over (order by date_of_birth) as rnk
          from employee e 
        ) t
        --where rnk <= 3;
    """
    cursor.execute(task6)
    show = cursor.fetchall()
    print(show)
    # ---------------------------
    connection.commit()
    print('Commit Success')
except(Exception, Error) as error:
    print('Error Connection', error)
finally:
    if connection:
        print('Connection closed')
        cursor.close()
        connection.close()

