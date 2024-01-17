import json
import os
from modules.functions import extract_text_from_json_by_sections
from modules.entity_finder_class import (
    ComplexPatternFinder, 
    EntityMatcher
)
from modules.constants_and_paths import (
    path_to_save as path_to_jsons,
    check_sec_types,
    gut_list,
    micro_list,
    csv_path,
)
from tqdm import tqdm
import pandas as pd

indicies = ["0" + str(i) for i in range(95,25,-5)]
# indicies.insert(0, "100")

em = EntityMatcher()
# Создание паттернов для матчера
em.create_pattern_dict("GUT", gut_list)
em.create_pattern_dict("BIOME", micro_list)
em.lemmatize_all_pattern_entities()


for pmc_dir_id in indicies:
    cpf = ComplexPatternFinder(entity_matcher=em)
    cpf2 = ComplexPatternFinder(entity_matcher=em)
    cur_json_path = path_to_jsons.format(DIR_ID=pmc_dir_id)
    print("\n ----------------------------------------------\n")
    print("save path ", cur_json_path)
    print("\n")
    
    
    refd_json_lst = os.listdir(cur_json_path)
    data_jsons = {}

    for infile_refd in tqdm(refd_json_lst):
        pmcid = infile_refd.split("_")[0]
        with open(f"{cur_json_path}{infile_refd}") as f:
            # all_texts[pmcid] = extract_text_from_json(json.load(f), ignorance_sec_types)
            data_json = json.load(f)
            cur_extracted_abstract = extract_text_from_json_by_sections(data_json, check_sec_types[1:])
            len_text = len(cur_extracted_abstract)
            if len_text > 1_000_000:
                print(f"---------- {pmcid} has TOO LONG ABSTRACT -------------")
                continue
            cpf.label_full_text_spacy(text=cur_extracted_abstract, text_id=pmcid)

            cur_extracted_title = extract_text_from_json_by_sections(data_json, check_sec_types[:1])
            len_text = len(cur_extracted_title)
            cpf2.label_full_text_spacy(text=cur_extracted_title, text_id=pmcid)
                
    pd.DataFrame(cpf.num_labels_for_text).to_csv(csv_path.format(DIR_ID=pmc_dir_id)+'_ABSTRACT'+".csv")
    pd.DataFrame(cpf2.num_labels_for_text).to_csv(csv_path.format(DIR_ID=pmc_dir_id)+'_TITLE'+".csv")
