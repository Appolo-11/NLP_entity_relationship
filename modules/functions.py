# # # # # # #
# Functions #
# # # # # # #
def extract_text_from_json(json_data, ignorance_sec_types):
    all_text = ''
    for document in json_data.get('documents', []):
        for passage in document.get('passages', []):
            sec_type = passage.get('infons', {}).get('section_type', '')
            if sec_type in ignorance_sec_types:
                # print(f"Ignore type {passage.get('infons', {}).get('section_type', '')}")
                continue
            all_text += passage.get('text', '') + "\n"
                
    return all_text

def extract_text_from_json_by_sections(json_data, check_sec_types):
    all_text = ''
    for document in json_data.get('documents', []):
        for passage in document.get('passages', []):
            sec_type = passage.get('infons', {}).get('section_type', '')
            if sec_type in check_sec_types:
                all_text += passage.get('text', '') + "\n"
    return all_text
    
def extract_text_from_json_DIFFER_by_sections(json_data, ignorance_sec_types):
    all_text = {}
    for document in json_data.get('documents', []):
        for passage in document.get('passages', []):
            sec_type = passage.get('infons', {}).get('section_type', '')
            if sec_type in ignorance_sec_types:
                # print(f"Ignore type {passage.get('infons', {}).get('section_type', '')}")
                continue
            if all_text.get(sec_type, ''):
                all_text[sec_type] += passage.get('text', '') + "\n"
            else:
                all_text[sec_type] = passage.get('text', '') + "\n"
                
    return all_text

