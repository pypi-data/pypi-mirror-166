import re
import json

#Just a comment

def is_slide_not_skipped(slide) -> bool:
    slide_properties = slide.get('slideProperties')
    if 'isSkipped' in slide_properties:
        if slide_properties.get('isSkipped') == True:
            return False
    return True

def is_slide_bios(slide) -> bool:
    if len(slide.get(
            'pageElements')) > 5:  # the number of 5 comes from the assumptions that the bios should have at 5 pages elemenets(Name, Title and AND Title, Overview, Core focus and key skills)
        return True
    return False

def delete_skipped_slides(slides) -> list:
    return list(filter(is_slide_not_skipped, slides))

def delete_slides_no_bios(slides) -> list:
    return list(filter(is_slide_bios, slides))

def preprocess_text(text):
    no_special_chars = remove_special_characters(text)
    no_space_text = remove_consecutive_spaces(no_special_chars)
    return no_space_text

def remove_special_characters(text): #keeps only characters, numbers, dots, comma, new line, slashes
    return re.sub('[^a-zA-Z0-9 \.\,\/\\n\(\)\|]', '', text)
'''
def remove_consecutive_new_lines(text):
    return re.sub('[\\n]+', '\\n', text)
'''

def remove_consecutive_spaces(text):
    return re.sub('[\s+]', ' ', text)

def page_elements_to_dict(slide):
    page_elements = slide.get('pageElements')
    dict = {}
    for count, page_element in enumerate(page_elements):
        try:
            page_element_id = page_element.get('objectId')
            if 'shape' in page_element:
                shape = page_element.get('shape')
                if 'text' in shape:
                    text_elements = page_element.get('shape').get('text').get('textElements')
                    content = ""
                    for text_element in text_elements:
                        if 'textRun' in text_element:
                            text = text_element.get('textRun').get('content') # ignore special characters
                            content += text
                    content = content.strip()
                    if content != "":
                        dict[page_element_id] = preprocess_text(content)
            else:
                continue
        except Exception as e:
            print(e)
    return dict


def convert_bio_slides_to_dict(slides):
    slides_bio_dict = {}
    for slide in slides:
        slides_bio_dict[slide.get('objectId')] = page_elements_to_dict(slide)
    return slides_bio_dict

def preprocess_raw_file(raw_file_path):
    try:
        with open(raw_file_path) as raw_file:
            raw_data = json.load(raw_file)
        slides = raw_data.get('slides')
        slides = delete_skipped_slides(slides)
        slides = delete_slides_no_bios(slides)
        slides = convert_bio_slides_to_dict(slides)
        return slides
    except Exception as e:
        print('Could not preprocess the data due to issue: ' + str(e))
        return None