from biosearch.DataPlatform.API import google_slides_api as google_api
import biosearch.DataPlatform.DB.database_ops as db_api
from datetime import datetime
import preprocessing_functions as ps
import json
import os
from pathlib import Path

def write_dictionary_to_csv(full_file_path, dictionary_data,presentation_id):
    data_list = []
    for slide_id, text_items in dictionary_data.items():
        record = str(presentation_id) + ';' + slide_id
        for text_id, text in text_items.items():
            data_list.append(record + ';' + text_id + ';' + text)
    with open(full_file_path, 'w') as f:
        for line in data_list:
            f.write(f"{line}\n")

def save_data_to_json_file(full_path, data):
    try:
        with open(full_path, 'w',
                  encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print('Could not write file due to issue: ' + str(e))

def is_presentation_updated(db_presentation, api_presentation) -> bool:
    if db_presentation.get('revision_id') != api_presentation.get('revisionId'):
        return True
    return False
#'M5y2ytuyRmLSgQ'
def download_new_presentation_data(db_presentation):
    api_presentation = google_api.get_presentation(db_presentation.get('presentation_link'))
    if is_presentation_updated(db_presentation, api_presentation):
        db_api.update_google_presentation_revision_id(api_presentation.get('revisionId'))
        save_data_to_json_file(full_path= 'Data/raw_presentation_data_' + datetime.today().strftime('%Y-%m-%d_%H:%M:%S') + '.json',
                          data= api_presentation)

def preprocess_data(path_to_raw_data):
    return ps.preprocess_raw_file(path_to_raw_data)

def upload_file_to_temp_table(file_path):
    db_api.upload_file_to_temp_table(file_path)

def main():
    db_google_presentations = db_api.get_all_google_presentations()
    for db_presentation in db_google_presentations:
        download_new_presentation_data(db_presentation)
        preprocessed_slides = preprocess_data(sorted(Path('Data/').iterdir(), key=os.path.getmtime)[-1])
        write_dictionary_to_csv('data.csv', preprocessed_slides, 1)
        upload_file_to_temp_table('/Users/georgiosgkekas/ilabProjects/BioSearch/DataPlatform/data.csv')

if __name__ == '__main__':
    main()

