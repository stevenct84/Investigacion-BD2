from neo4j import GraphDatabase

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
    RETURN m2.Title,m2.Genres,count(DISTINCT(u)) as common_users
    ORDER BY common_users DESC
    LIMIT 6''', data=movie_name )
    values = [record.values() for record in result]
    print(values)
    return values

#ejecutar los scripts
def get_movies(movie_name):
    return driver.session().execute_read(get_similar_movies, movie_name)

