import os
from modules.bioc2json_class import read_bioc_to_json
from modules.constants_and_paths import (
    path_to_read, 
    path_to_save,
    pmc_gz_path
)
from tqdm import tqdm

indicies = ["0" + str(i) for i in range(75,100,5)]
indicies.append("100")

for pmc_dir_id in indicies:
    cur_path_to_save = path_to_save.format(DIR_ID=pmc_dir_id)
    cur_path_to_read = path_to_read.format(DIR_ID=pmc_dir_id)
    print("read path ", cur_path_to_read)
    print("save path ", cur_path_to_save)
    
    
    if not os.path.exists(cur_path_to_save):
        print("\n ------------------------------------------")
        print(f"Create dir {cur_path_to_save} \n") 
        os.system(f"mkdir {cur_path_to_save}")

    if not os.path.exists(cur_path_to_read):
        print(f"Create dir {cur_path_to_read} \n") 
        os.system(f"mkdir {cur_path_to_read}")
        
        cur_gz_path = pmc_gz_path.format(DIR_ID=pmc_dir_id)
        print("\n ------------------------------------------")
        print(f"Untar {cur_gz_path} \n")
        os.system(f"tar -xf {cur_gz_path} --directory {cur_path_to_read}")
    
    json_lst = os.listdir(cur_path_to_read)
    print("\n ------------------------------------------")
    print(f"Convert bioc to json \n")
    for json_name in tqdm(json_lst):
        read_bioc_to_json(cur_path_to_read, cur_path_to_save, 
                        file_full_name=json_name,
                        new_format='json')

    print("\n ============================================")
    print(f"REMOVE {cur_path_to_read} \n")
    os.system(f"rm -rf {cur_path_to_read}")
    
