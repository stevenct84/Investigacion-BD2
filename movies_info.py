from neo4j import GraphDatabase
import numpy as np
import pandas as pd

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
driver=GraphDatabase.driver(URI, auth=AUTH)

#obtener las peliculas similares segun la consulta
def get_similar_movies(tx, movie_name):
    result=tx.run('''
    MATCH(m1:Movie)-[r1]-(u:User)-[r2]-(m2:Movie)
    WHERE m1.Title CONTAINS $data
      AND m2.Title<>$data
      AND r1.Rating>3 AND r2.Rating>3
      AND m1.Genres = m2.Genres
    RETURN m2.Title as common_users
    ORDER BY common_users DESC
    LIMIT 6''', data=movie_name )
    values = [record.values() for record in result]
    print(values)
    return values

#ejecutar los scripts
def get_movies(movie_name):
    return driver.session().execute_read(get_similar_movies, movie_name)


#usuarios con mejor concordancia en las puntuaciones
#MATCH (u1)-[r1:SIMILAR]-(u2) return r1.Similarity  ORDER BY r1.Similarity DESC limit 10
def get_recomendations_by_userid(tx,userid):
    result=tx.run('''
        MATCH (u1:User)-[r1:SIMILAR]-(u2)-[r2:RATED]-(m:Movie)
        WHERE id(u1)=$id
        AND r1.Similarity>0.35
        AND NOT ( (u1)-[]-(m))
        RETURN m.Title 
        LIMIT 6
        ''', id=userid)
    values = [record.values() for record in result]
    print(values)
    return values

def get_movies_by_useid( userid):
    return driver.session().execute_read(get_recomendations_by_userid, userid)
get_movies_by_useid(546)




def similarity(tx):
    # Create projection
    query=('''Call gds.graph.project(
            'myGraph',
            ['User', 'Movie'],
            {
                RATED: {properties:  'Rating'}
            });''')
    tx.run(query)

def user_similarity(tx):
    # Get user similarity
    query=('''
    CALL gds.nodeSimilarity.stream('myGraph')
    YIELD node1, node2, similarity
    RETURN gds.util.asNode(node1).id AS UserID1, gds.util.asNode(node2).id AS UserID2, similarity
    ORDER BY similarity DESCENDING, UserID1, UserID2
    ''')
    result=tx.run(query)
    values = [record.values() for record in result]
    return values


def create_similar_relationship(tx):
# Create Similar relationship
    users_data=driver.session().execute_read(user_similarity)
    query='''
        unwind $data as row
        match (u1:User{id: row.UserID1}), (u2:User{id: row.UserID2})
        merge (u1)-[r:SIMILAR]->(u2)
        set r.Similarity=row.similarity
        return count(*) as create_rated'''
    for part in users_data:
        tx.run(query, data={"UserID1":int(part[0]), "UserID2" :int(part[1]), "similarity":float(part[2])} )


def create_relation():
    driver.session().execute_read(similarity)
    driver.session().execute_write(create_similar_relationship)




