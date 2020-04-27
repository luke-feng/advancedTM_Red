import argparse
import os
import random
import csv

def process_hipe(in_filepath, out_filepath):

    unknown_gt_ids = 0   # counter of ground truth entity ids that are not in the wiki_name_id.txt
    ent_id_changes = 0
    with open(in_filepath) as fin, open(out_filepath, "w") as fout:
        in_mention = False   # am i inside a mention span or not
        first_document = True
        for line in fin:
            l = line.split('\t')
            if len(l) == 10:
                if in_mention and not ('I' in l[1]):
                    # if I am in mention but the current line does not continue the previous mention
                    # then print MMEND and be in state in_mention=FALSE
                    # end of the mention
                    fout.write("MMEND\n")
                    in_mention = False

                elif "EndOfLine" in l[9]:
                    # new line
                    fout.write("*NL*\n")
                elif 'B' in l[1]:  # this is a new mention
                    wikidata_id = l[7] 
                    fout.write("MMSTART_"+wikidata_id+"\n")   # TODO check here if entity id is inside my wikidump
                                                       # if not then omit this mention
                    fout.write(l[0]+"\n")  # write the word
                    in_mention = True
                elif l[1] == "NE-COARSE-LIT":
                    continue
                else:
                    # words that continue a mention len(l) == 10: and l[1] contains 'I'
                    # or normal word outside of mention
                    fout.write(l[0].rstrip()+"\n")
            
            elif "# document_id" in line:
                if not first_document:
                    fout.write("DOCEND\n")
                # line = "# document_id = NZZ-1798-01-20-a-p0001\n"
                doc_title = line[len("# document_id = "):-1]
                fout.write("DOCSTART_"+doc_title.replace(' ', '_')+"\n")
                first_document = False
            else:
                continue             
        fout.write("DOCEND\n")  # until the last document


def split_dev_test(in_filepath):
    with open(in_filepath) as fin, open(args.output_folder+"temp_hipe_dev", "w") as fdev,\
            open(args.output_folder+"temp_hipe_test", "w") as ftest:
        fout = fdev
        for line in fin:
            if line.startswith("# language"):
                seed = random.randint(1,3)
                if seed == 3:
                    fout = ftest
                else:
                    fout = fdev
            fout.write(line)


def create_necessary_folders():
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aida_folder", default="/Users/chaofeng/end2end_neural_el/data/basic_data/test_datasets/HIPE/")
    parser.add_argument("--output_folder", default="/Users/chaofeng/end2end_neural_el/data/new_datasets/")
    return parser.parse_args()

def load_ID_mapping(mapping_path):
    mapping = {}
    with open(mapping_path, 'r') as tsvfile:
        for line in tsvfile:
            tokens = line.rstrip().split('\t')
            if len(tokens) == 2:
                mapping[tokens[1]] = tokens[0]
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping


def process_hipe_aida(in_filepath, out_filepath):
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
                            print('UNK', wiki_ID)
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
                fout.write("-DOCSTART-"+doc_title.replace(' ', '_')+"\n")
                first_document = False
            else:
                continue             

if __name__ == "__main__":
    args = _parse_args()
    create_necessary_folders()
    mapping_path ='/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wiki_name_map1.txt'
    process_hipe(args.aida_folder+"HIPE-data-v1.0-train-de.tsv", args.output_folder+"HIPE-data-v1.0-train-de.txt")
    process_hipe_aida(args.aida_folder+"HIPE-data-v1.0-train-de.tsv", args.output_folder+"HIPE-aida-train-de.txt")
    split_dev_test(args.aida_folder+"HIPE-data-v1.0-dev-de.tsv")
    process_hipe(args.output_folder+"temp_hipe_dev", args.output_folder+"HIPE-data-v1.0-dev-de.txt")
    process_hipe(args.output_folder+"temp_hipe_test", args.output_folder+"HIPE-data-v1.0-test-de.txt")
    process_hipe_aida(args.output_folder+"temp_hipe_dev", args.output_folder+"HIPE-aida-dev-de.txt")
    process_hipe_aida(args.output_folder+"temp_hipe_test", args.output_folder+"HIPE-aida-test-de.txt")

    os.remove(args.output_folder + "temp_hipe_dev")
    os.remove(args.output_folder + "temp_hipe_test")