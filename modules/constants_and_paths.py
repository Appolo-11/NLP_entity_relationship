path_to_read = '/home/echukhrova/nlp_project/PMC_Dataset/PMC{DIR_ID}XXXX/'
path_to_save = '/home/echukhrova/nlp_project/PMC_Dataset/refd_PMC{DIR_ID}XXXX/'
pmc_gz_path = '/home/echukhrova/nlp_project/PMC_Dataset/PMC{DIR_ID}XXXXX_json_ascii.tar.gz'
csv_path = '/home/echukhrova/nlp_project/labeled_tables/PMC{DIR_ID}'

ignorance_sec_types = ['REF', 'METHODS', 'COMP_INT']

with open("/home/echukhrova/nlp_project/dicts/food_refactored.txt") as f:
  food_list = [line.strip() for line in f]
with open("/home/echukhrova/nlp_project/dicts/bac_refactored.txt") as f:
  bacteria_list = [line.strip() for line in f]

gut_list = ['gut', 'digestive', 'intestine', 'intestines', 'intestinal', 'digest']
micro_list = ['microbiota', 'microbiome']
check_sec_types = ['TITLE', 'ABSTRACT']