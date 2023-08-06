def drop_all_tables():
    return '''DROP TABLE IF EXISTS google_presentations CASCADE; 
              DROP TABLE IF EXISTS google_slides CASCADE; 
              DROP TABLE IF EXISTS google_slide_textboxes CASCADE;'''

def get_all_google_presentations():
    return '''SELECT presentation_id, presentation_link, revision_id FROM google_presentations;'''

def create_all_tables():
    return create_table_google_presentations() + create_table_google_slides() + create_table_google_slide_textboxes()


def create_table_google_presentations():
    return '''CREATE TABLE IF NOT EXISTS google_presentations ( 
              presentation_id SERIAL PRIMARY KEY,
	          presentation_link VARCHAR UNIQUE NOT NULL,
	          club_name VARCHAR UNIQUE NOT NULL,
	          revision_id VARCHAR NOT NULL,
	          created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	          updated_at TIMESTAMP NOT NULL DEFAULT NOW()
              );'''

def update_google_presentation_revision_id(revision_id):
    return "UPDATE google_presentations SET revision_id = '" + revision_id + "'"


def insert_google_presentation():
    return '''INSERT INTO google_presentations (presentation_link, club_name, revision_id) VALUES (%s, %s, %s)'''

def create_table_google_slides():
    return '''CREATE TABLE IF NOT EXISTS google_slides ( 
                slide_id SERIAL PRIMARY KEY, 
                slide_link VARCHAR UNIQUE NOT NULL,
                presentation_id INT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                CONSTRAINT fk_presentation FOREIGN KEY(presentation_id) REFERENCES google_presentations(presentation_id) ON DELETE CASCADE
            );'''

def create_temp_table():
    return ''' CREATE TEMPORARY TABLE IF NOT EXISTS temp_t AS 
                SELECT gs.presentation_id, gs.slide_link, textbox_link, text FROM 
                google_presentations AS gp INNER JOIN 
                google_slides AS gs ON gp.presentation_id = gs.presentation_id INNER JOIN
                google_slide_textboxes AS gt ON gs.slide_id = gt.slide_id WITH NO DATA;
            '''

def upload_data_from_file(file_path):
    return "COPY temp_t FROM '" +file_path+"' (DELIMITER(';'))"

def merge_temp_table_with_google_slides_table():
    return '''INSERT INTO google_slides(slide_link, presentation_id)
              SELECT slide_link, presentation_id FROM temp_t GROUP BY slide_link, presentation_id
              ON CONFLICT DO NOTHING;'''

def merge_temp_table_with_google_slide_textboxes_table():
    return '''WITH join_t AS(
                            SELECT gs.slide_id, tm.*
                            FROM google_slides as gs
                            INNER JOIN temp_t as tm
                            ON gs.slide_link = tm.slide_link)
              INSERT INTO google_slide_textboxes(slide_id, textbox_link, text)
              SELECT slide_id, textbox_link, text FROM join_t
              ON CONFLICT (textbox_link)
              DO 
                UPDATE SET text = EXCLUDED.text;
    '''
def create_table_google_slide_textboxes():
    return '''CREATE TABLE IF NOT EXISTS google_slide_textboxes ( 
                textbox_id SERIAL PRIMARY KEY, 
                textbox_link VARCHAR UNIQUE NOT NULL, 
                slide_id INT NOT NULL, 
                text VARCHAR NOT NULL, 
                created_at TIMESTAMP NOT NULL DEFAULT NOW(), 
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(), 
                CONSTRAINT fk_slide_id FOREIGN KEY(slide_id) REFERENCES google_slides(slide_id) ON DELETE CASCADE
            );
            ALTER TABLE google_slide_textboxes ADD COLUMN ts tsvector
            GENERATED ALWAYS AS (to_tsvector('english', text)) STORED;
	        CREATE INDEX ts_idx ON google_slide_textboxes USING GIN (ts);'''
