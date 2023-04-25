from neo4j import GraphDatabase
import pandas as pd
import numpy as np

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
driver=GraphDatabase.driver(URI, auth=AUTH)

#cargar los datasets con pandas
movies = pd.read_csv('movies.dat',sep='::',encoding = "ISO-8859-1", engine='python' ,names=['MovieID','Title','Genres'])
ratings = pd.read_csv('ratings.dat',sep='::',encoding = "ISO-8859-1", engine='python',names=['UserID','MovieID','Rating','Timestamp'])
users = pd.read_csv('users.dat',sep='::',encoding = "ISO-8859-1", engine='python',names=['UserID','Gender','Age','Occupation','Zip_code'])

#Crear los nodos de usuarios a la base de datos
def create_users(tx,users):
    tx.run('''
        unwind $data as row
        merge (n:User{id: row.UserID})
        set n.Gender = row.Gender
        set n.Age =  row.Age 
        return count(*) as custmers_created
    ''', data= users.to_dict('records'))

#crear los nodos de las peliculas a la base de datos
def create_movies(tx,movies):
    tx.run('''
    unwind $data as row
    merge (n:Movie{id: row.MovieID})
    set n.Title = row.Title
    set n.Genres =  row.Genres 
    return count(*) as movies_created''', 
    data = movies.to_dict('records'))  

#crear las conexiones entre los nodos, con la calificacion de los usuarios a las peliculas
def create_connections(tx,ratings):
    i=1
    for part in np.array_split(ratings,200):
        if i == 50:
            break
        if i%10==0:
            print(i)

        tx.run('''
        unwind $data as row
        match (u:User{id: row.UserID}), (m:Movie{id: row.MovieID})
        merge (u)-[r:RATED]->(m)
        set r.Rating = row.Rating
        return count(*) as create_rated
        ''', data= part.to_dict('records'))
        i = i+1
    print("listo")

#ejecutar los scripts
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session() as session:
        session.execute_write(create_users,users)
        session.execute_write(create_movies,movies)
        session.execute_write(create_connections,ratings)
        #session.execute_read(get_similar_movies,"Toy Story")
