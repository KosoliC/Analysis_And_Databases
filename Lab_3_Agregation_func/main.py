import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(category_id, int) or category_id < 0:
        return None

   
    request =   f"""select f.title, l.name as languge, c.name as category from film f 
                    inner join language l on f.language_id = l.language_id 
                    inner join film_category fc on fc.film_id = f.film_id 
                    inner join category c on fc.category_id = c.category_id 
                    where fc.category_id = {category_id} 
                    order by f.title, l.name"""

    return pd.read_sql_query(request, con=connection)

    
def number_films_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(category_id, int):
        return None

    else:

        request =   f"""select fl.category, count(fl.title)
                    from film_list fl
                    join category c on c.name = fl.category
                    where c.category_id = {category_id}
                    group by fl.category"""

        return pd.read_sql_query(request, con=connection)


def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(min_length, (int, float)):
        return None
    elif not isinstance(max_length, (int, float)):
        return None

    elif min_length > max_length:
        return None

    else:

        request =   f"""select length, count(title)
                    from film
                    where film.length between {min_length} and {max_length}
                    group by length 
        """

        return pd.read_sql_query(request, con=connection)

def client_from_city(city:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(city, str):
        return None

    request =   f"""select city.city, c.first_name, c.last_name
                    from city
                    join address on address.city_id = city.city_id
                    join customer c on c.address_id = address.address_id
                    where city.city = '{city}'"""

    return pd.read_sql_query(request, con=connection)

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(length, (int,float)) or length < 0:
        return None

    request =   f"""select f.length, avg(p.amount)
                    from film f
                    join inventory using(film_id)
                    join rental using(inventory_id)
                    join payment p using(rental_id)
                    where f.length = {length}
                    group by f.length"""

    return pd.read_sql_query(request, con=connection)



def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(sum_min, (int, float)):
        return None

    if sum_min < 0:
        return None

    request =   f"""select c.first_name, c.last_name, sum(f.length) as sum
                    from film as f
                    join inventory i on i.film_id = f.film_id
                    join rental r on r.inventory_id = i.inventory_id
                    join customer c on c.customer_id = r.customer_id
                    group by c.first_name, c.last_name
                    having sum(f.length) > {sum_min}
                    order by sum, c.last_name, c.first_name"""
    return pd.read_sql_query(request, con=connection)  


def category_statistic_length(name:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(name, (str)):
        return None

    request =   f"""select c.name as category, avg(f.length), sum(f.length), min(f.length), max(f.length) 
                    from film f 
                    join film_category fc using(film_id) 
                    join category c using(category_id) 
                    group by c.name 
                    having  c.name = '{name}'"""

    return pd.read_sql_query(request, con=connection)


