import argparse
import os
import random
import preprocessing.util as util

def process_hipe(in_filepath, out_filepath):

    # _, wiki_id_name_map = util.load_wiki_name_id_map(lowercase=False)
    #_, wiki_id_name_map = util.entity_name_id_map_from_dump()
    entityNameIdMap = util.EntityNameIdMap()
    entityNameIdMap.init_compatible_ent_id()
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
    parser.add_argument("--aida_folder", default="../data/basic_data/test_datasets/HIPE/")
    parser.add_argument("--output_folder", default="../data/new_datasets/")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    create_necessary_folders()
    process_hipe(args.aida_folder+"HIPE-data-v1.0-train-de.tsv", args.output_folder+"HIPE-data-v1.0-train-de.txt")

    split_dev_test(args.aida_folder+"HIPE-data-v1.0-dev-de.tsv")
    process_hipe(args.output_folder+"temp_hipe_dev", args.output_folder+"HIPE-data-v1.0-dev-de.txt")
    process_hipe(args.output_folder+"temp_hipe_test", args.output_folder+"HIPE-data-v1.0-test-de.txt")

    os.remove(args.output_folder + "temp_hipe_dev")
    os.remove(args.output_folder + "temp_hipe_test")