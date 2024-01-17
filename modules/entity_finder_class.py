import spacy
from spacy.matcher import Matcher
from tqdm import tqdm
from time import time

# # # # # # #
#  Classes  #
# # # # # # #
class EntityMatcher:
    def __init__(self,load_model="en_core_web_sm"):
        self.nlp = spacy.load(load_model)
        self.matcher = Matcher(self.nlp.vocab)
        self.pattern_dict = {}
        self.lemmatized_pattern_dict = {}
        self.entity_ids = {}
        self.free_entity_id = 1
        self.matcher = Matcher(self.nlp.vocab)


    # Функция создания словаря паттернов для заданных имени категории и списка сущностей
    def create_pattern_dict(self, entity_name, entity_list):
        """Создает паттерны для сущностей из списка."""
        patterns = []
        for entity in entity_list:
            pattern = entity
            patterns.append(pattern)
            
        self.pattern_dict[entity_name] =  patterns
   
    # Функция для лемматизации сущности словярей
    def lemmatize_many_words_entity(self, entity_pattern):
        """Функция для лемматизации одного/нескольких слов с использованием spaCy."""
        return " ".join([self.nlp(word)[0].lemma_.lower() for word in entity_pattern.split()])

    # Function for creation lemmatized pattern dictionary and 
    # adding that entities to the matcher
    def lemmatize_all_pattern_entities(self):
        for entity_name, entity_list in tqdm(self.pattern_dict.items()):
            lemmatized_patterns = []
            for entity in tqdm(entity_list):
                # print(f"Entity is {entity}, entity_name is {entity_name}")
                lemmatized_entity = self.lemmatize_many_words_entity(entity)
                words = lemmatized_entity.split()
                lemmatized_pattern = [{"LOWER": word} for word in words]
                lemmatized_patterns.append(lemmatized_pattern)

            self.lemmatized_pattern_dict[entity_name] = lemmatized_patterns
            self.entity_ids[entity_name] = self.free_entity_id
            self.free_entity_id += 2
        self.update_pattern_matcher()

    # Function for adding new entities to matcher 
    def update_pattern_matcher(self):
        # Добавление паттернов к матчеру
        for entity_name, entity_patterns in self.lemmatized_pattern_dict.items():
            self.matcher.add(entity_name, entity_patterns)




class ComplexPatternFinder:
    def __init__(self, entity_matcher, labels=[1,3,-1]):
        # Загрузка модели для spaCy
        self.nlp = entity_matcher.nlp
        self.em = entity_matcher
        self.labels = labels
        self.init_num_labels()
        self.labeled_sentence_dataset = {"sentences": [], "labels": [], "sec_type": []}
        
        
    def init_num_labels(self):
        self.num_labels_for_text = {label:[] for label in self.labels}
        self.num_labels_for_text[-1] = []
        self.num_labels_for_text["text_id"] = []
        
    # Функция для разметки текста
    def label_text_spacy(self, text, sec_type=''):
        """
        Функция для разметки текста на основе паттернов еды и бактерий.
        Возвращает список токенов и соответствующий список меток для каждого предложения.
        """

        doc = self.nlp(text)

        for sentence in doc.sents:
            lemmatized_sent = " ".join([token.lemma_.lower() for token in sentence])
            # Инициализация списка меток
            sent_doc = self.nlp(lemmatized_sent)
            labels = [0] * len(sent_doc)
        
            # Поиск совпадений в тексте и присвоение меток
            matches = self.em.matcher(sent_doc)
            for match_id, start, end in matches:
                entities = self.em.lemmatized_pattern_dict.keys()
                entity_name = self.nlp.vocab.strings[match_id]
                label = self.em.entity_ids.get(entity_name, -1)
                for i in range(start, end):
                    labels[i] = label
            
            # Получение списка токенов и меток
            tokens = [token.text for token in sent_doc]
            self.labeled_sentence_dataset["sentences"].append(tokens)
            self.labeled_sentence_dataset["labels"].append(labels)
            self.labeled_sentence_dataset["sec_type"].append(sec_type)
            
            
    def _clean_all_labeled_text_data(self):
        confidence = input().lower()
        if confidence=='true':
            self.labeled_sentence_dataset = {"sentences": [], "labels": [], "sec_type": []}
            self.num_labels_for_text = {label:[] for label in self.labels}
            self.num_labels_for_text[-1] = []
            self.num_labels_for_text["text_id"] = []
        else:
            print("To clear labeled sentences data, please type `true` in stdin window")

    def __force_clean_all_labeled_text_data(self, confidence=False):
        if confidence:
            self.labeled_sentence_dataset = {"sentences": [], "labels": [], "sec_type": []}
            self.init_num_labels()
        else:
            print("To clear labeled sentences data, please set `confidence` to True")

    # Функция для разметки текста
    def label_full_text_spacy(self, text, text_id):
        """
        Функция для разметки текста на основе паттернов еды и бактерий.
        Возвращает список токенов и соответствующий список меток для каждого предложения.
        """

        doc = self.nlp(text, disable=['tok2vec', 'tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner'])


        labels = [0] * len(doc)

        start2 = time()
        num_labels = {label:0 for label in self.labels}
        num_labels[-1] = 0
        # Поиск совпадений в тексте и присвоение меток
        matches = self.em.matcher(doc)
        for match_id, start, end in matches:
            entity_name = self.nlp.vocab.strings[match_id]
            label = self.em.entity_ids.get(entity_name, -1)
            num_labels[label] += 1
            
        self.num_labels_for_text["text_id"].append(text_id)
        # Сохранение лейблов для проанализированого текста
        for label, count in num_labels.items():
            self.num_labels_for_text[label].append(count)