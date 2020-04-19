import argparse
import os
import random
import csv
in_filepath = '../end2end_neural_el/data/basic_data/test_datasets/HIPE/HIPE-data-v1.0-train-de.tsv'
out_filepath = '../end2end_neural_el/data/basic_data/test_datasets/HIPE/HIPE-aida-de.txt'
mapping_path ='../end2end_neural_el/deep-ed/basic_data/wiki_name_map.txt'
def load_ID_mapping(mapping_path):
    with open(mapping_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        mapping = {rows[1]:rows[0] for rows in reader}
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping


def process_hipe(in_filepath, out_filepath):
    mapping = load_ID_mapping(mapping_path)
    unknown_gt_ids = 0   # counter of ground truth entity ids that are not in the wiki_name_id.txt
    ent_id_changes = 0
    token = ''
    flag = ''
    NE = ''
    wiki_ID = ''
    wiki_Name = ''
    url = ''
    NE_l = []
    with open(in_filepath) as fin, open(out_filepath, "w") as fout:
        in_mention = False   # am i inside a mention span or not
        first_document = True
        for line in fin:
            l = line.split('\t')
            if len(l) == 10:
                if l[1] == "NE-COARSE-LIT":
                    continue
                else:
                    token = l[0]
                    if "Q" in l[7]:
                        wiki_ID = l[7]
                        if wiki_ID in mapping:
                            wiki_Name = mapping[wiki_ID]
                        else:
                            wiki_Name = "--UNK--"
                        if "B" in l[1]:
                            flag = "B"
                            in_mention = True
                            NE = l[0]
                        elif "I" in l[1]:
                            flag = "I"
                            NE = NE + " " + l[0]
                        url = "http://de.wikipedia.org/wiki/" + wiki_Name
                        new_line = (token, flag, wiki_Name, url, wiki_ID)
                        NE_l.append(new_line)
                    elif "NIL" in l[7]:
                        wiki_Name = "--NME--"
                        if "B" in l[1]:
                            flag = "B"
                            in_mention = True
                            NE = l[0]
                        elif "I" in l[1]:
                            flag = "I"
                            NE = NE + " " + l[0]
                        new_line = (token, flag, wiki_Name)
                        NE_l.append(new_line)
                    else:
                        if in_mention and not ('I' in l[1]):
                            # if I am in mention but the current line does not continue the previous mention
                            # then print MMEND and be in state in_mention=FALSE
                            # end of the mention
                            in_mention = False
                            token = l[0]
                            for n_l in NE_l:
                                if n_l[2] == "--NME--":
                                    fout.write(n_l[0] + '\t' + n_l[1] + '\t' + NE + '\t' + n_l[2]+ "\n")
                                else:
                                    fout.write(n_l[0] + '\t' + n_l[1] + '\t' + NE + '\t' + n_l[2]+ '\t' + n_l[3]+ '\t' + n_l[4]+ "\n")
                            NE_l = []
                            fout.write(token + '\n')
                            if "EndOfLine" in l[9]:
                                fout.write('\n')
                            
                        else: 
                            token = l[0]
                            fout.write(token + '\n')
                            if "EndOfLine" in l[9]:
                                fout.write('\n')
            
            elif "# document_id" in line:
                if not first_document:
                    fout.write("DOCEND\n")
                # line = "# document_id = NZZ-1798-01-20-a-p0001\n"
                doc_title = line[len("# document_id = "):-1]
                fout.write("DOCSTART_"+doc_title.replace(' ', '_')+"\n")
                first_document = False
            else:
                continue             

process_hipe(in_filepath, out_filepath)