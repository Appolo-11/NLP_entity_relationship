from bioc import biocjson
import json

class BioC2JSON:
    def node(this, node):
        json_node = {'refid': node.refid, 'role': node.role}
        return json_node

    def relation(this, rel):
        json_rel = {}
        json_rel['id'] = rel.id
        json_rel['infons'] = rel.infons
        json_rel['nodes'] = [this.node(n) for n in rel.nodes]
        return json_rel

    def location(this, loc):
        json_loc = {'offset': int(loc.offset), 'length': int(loc.length)}
        return json_loc

    def annotation(this, note):
        json_note = {}
        json_note['id'] = note.id
        json_note['infons'] = note.infons
        json_note['text'] = note.text
        json_note['locations'] = [this.location(l)
                                  for l in note.locations]
        return json_note

    def sentence(this, sent):
        json_sent = {}
        json_sent['infons'] = sent.infons
        json_sent['offset'] = int(sent.offset)
        json_sent['text'] = sent.text
        json_sent['annotations'] = [this.annotation(a)
                                    for a in sent.annotations]
        json_sent['relations'] = [this.relation(r)
                                  for r in sent.relations]
        return json_sent

    def passage(this, psg):
        json_psg = {}
        json_psg['infons'] = psg.infons
        json_psg['offset'] = int(psg.offset)
        json_psg['text'] =  psg.text
        json_psg['text'] =  psg.text if psg.text else ""
        json_psg['sentences'] = [this.sentence(s)
                                 for s in psg.sentences]
        json_psg['annotations'] = [this.annotation(a)
                                   for a in psg.annotations]
        json_psg['relations'] = [this.relation(r)
                                 for r in psg.relations]
        return json_psg

    def document(this, doc):
        json_doc = {}
        json_doc['id'] = doc.id
        json_doc['infons'] = doc.infons
        json_doc['passages'] = [this.passage(p)
                                for p in doc.passages]
        json_doc['relations'] = [this.relation(r)
                                 for r in doc.relations]
        return json_doc

    def collection(this, collection):
        json_collection = {}
        json_collection['source'] = collection.source
        json_collection['date'] = collection.date
        json_collection['key'] = collection.key
        json_collection['infons'] = collection.infons
        json_collection['documents'] = [this.document(d)
                                        for d in collection.documents]
        return json_collection



def read_bioc_to_json(path_to_read, path_to_save, file_full_name, new_format=''):
  name, format = file_full_name.split('.')
  # Deserialize ``fp`` to a BioC collection object.
  # print(f'Read file {file_full_name} from {path_to_read}')
  with open(path_to_read + file_full_name, 'r') as fp:
      collection = biocjson.load(fp)
  bioc2json = BioC2JSON()
  bioc_json = bioc2json.collection(collection)
  # print(f'Save file {name}_refd.{format} to {path_to_save}')
  if new_format:
      format = new_format
  with open(f"{path_to_save}{name}_refd.{format}", 'w') as f:
      json.dump(bioc_json, f, indent=4)
      print(file=f)