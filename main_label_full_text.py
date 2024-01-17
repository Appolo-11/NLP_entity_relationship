import json
import os
from modules.functions import extract_text_from_json
from modules.entity_finder_class import (
    ComplexPatternFinder, 
    EntityMatcher
)
from modules.constants_and_paths import (
    path_to_save as path_to_jsons,
    ignorance_sec_types,
    food_list,
    bacteria_list,
    csv_path,
)
from tqdm import tqdm
import pandas as pd

indicies = ["0" + str(i) for i in range(95,25,-5)]
#indicies.append("100")

em = EntityMatcher()
# Создание паттернов для матчера
em.create_pattern_dict("FOOD", food_list)
em.create_pattern_dict("BACT", bacteria_list)
em.lemmatize_all_pattern_entities()


for pmc_dir_id in indicies:
    cpf = ComplexPatternFinder(entity_matcher=em)
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
            cur_extracted_text = extract_text_from_json(json.load(f), ignorance_sec_types)
            len_text = len(cur_extracted_text)
            if len_text > 1_000_000:
                for i in range(len_text//1_000_000 + ((len_text % 1_000_000)>0)):
                    cpf.label_full_text_spacy(text=cur_extracted_text[i:i+999_999], text_id=pmcid)
            else:
                cpf.label_full_text_spacy(text=cur_extracted_text, text_id=pmcid)
    
    
    df = pd.DataFrame(cpf.num_labels_for_text).to_csv(csv_path.format(DIR_ID=pmc_dir_id)+".csv")
