import psycopg2
import psycopg2.extras

try:
    from DB.db_config import connection_params
    import DB.db_queries as query
except Exception as e:
    print('the file is run directly and not called by other file')
    from db_config import connection_params
    import db_queries as query


def get_all_google_presentations():
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query.get_all_google_presentations())
                return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to initialise tables due to :" + error)

def upload_file_to_temp_table(file_path):
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query.create_temp_table())
                cursor.execute(query.upload_data_from_file(file_path))
                cursor.execute(query.merge_temp_table_with_google_slides_table())
                cursor.execute(query.merge_temp_table_with_google_slide_textboxes_table())
                print('Merged successfully!')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to initialise tables due to :" + error)

def update_google_presentation_revision_id(revision_id):
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query.update_google_presentation_revision_id(revision_id))
        print('''Record (%s) has been updated successfully into google_presentations table ''' % revision_id)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to update the revision_id of google_presentation table due to :" + error)

def insert_google_presentation(presentation_link, club_name, revision_id):
    record_to_insert = (presentation_link, club_name, revision_id)
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query.insert_google_presentation(), record_to_insert)
        print('''Record (%s, %s, %s) inserted successfully into google_presentations table ''' % record_to_insert)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to insert to google_presentation table due to :" + error)


def initialise_database_tables():
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query.drop_all_tables())
                cursor.execute(query.create_all_tables())
        print("Initialised all the tables successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to initialise tables due to :" + error)


if __name__ == "__main__":
    initialise_database_tables()
    insert_google_presentation('19Fh8FULu6hNFVpb5iK6-NrBNqin3SLozE0emdJtstPM', 'Dekker', 'Miw8XHfMw58bkw')
    get_all_google_presentations()
