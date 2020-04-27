part 1: down essential wiki dumps

1 Download wikidata dumps from https://dumps.wikimedia.org/wikidatawiki/entities/
--latest-all.json.bz2 (52.6G)

2 Download wikipedia dumps from https://dumps.wikimedia.org/, including: 
--dewiki-20200420-page.sql.gz (261M)
--dewiki-20200420-page_props.sql.gz (73M)
--dewiki-20200420-page_restrictions.sql.gz (21M)
--dewiki-20200420-pages-articles.xml.bz2 (5.2G)

part 2: pre-processing with datapedia dumps

3 Import spl files into mysql. Geting restriction mapping from page_restrictions.sql, geting wikipedia page_id and page_title mapping from page.sql, geting wikipedia page_id and wikidata entity_id mapping from page_props.sql

python gen_redirction.py
python get_from_sql.py

4 Using WikiExtractor_01.py to extract articles from wikidumps (https://github.com/attardi/wikiextractor)
Using write_to_one_file.py to write all files into one file.

python WikiExtractor_01.py -o [output file path] -l input
python write_to_one_file.py

part 3: deal with wikidata dumps
6 Geting all entity_ID, name and description from wikidata dump
python get_wikidata_name_des.py

7 Change wikipedia page_id to wikidata entity_id
python change_wikiID.py

8 For all other entities not in wikipedia file, integrate them to wikipedia articles file.
python integrate_wikidata_wikipedia.py

part 4: train entity embedding
In this part, we almost followed (https://github.com/dalab/deep-ed ), but we have changed some parts of the code, and adapted it to en wiki data.
10 Install [Torch](http://torch.ch/) and other torch libraries.

11 Create a $DATA_PATH directoy 

12 Create wikipedia_p_e_m.txt
th data_gen/gen_p_e_m/gen_p_e_m_from_wiki.lua -root_data_dir $DATA_PATH

13 Create a file ent_wiki_freq.txt with entity frequencies
th entities/ent_name2id_freq/e_freq_gen.lua  -root_data_dir $DATA_PATH

14 Generate all entity disambiguation datasets in a CSV format needed in our training stage
mkdir $DATA_PATH/generated/test_train_data/
th data_gen/gen_test_train_data/gen_all.lua -root_data_dir $DATA_PATH

15 Create training data for learning entity embeddings
i) From Wiki canonical pages: 
th data_gen/gen_wiki_data/gen_ent_wiki_w_repr.lua -root_data_dir  $DATA_PATH

ii) From context windows surrounding Wiki hyperlinks: 
th data_gen/gen_wiki_data/gen_wiki_hyp_train_data.lua -root_data_dir $DATA_PATH

16 Compute the unigram frequency of each word in the Wikipedia corpus
th words/w_freq/w_freq_gen.lua -root_data_dir $DATA_PATH
 
17 Compute the restricted training data for learning entity embeddings by using only candidate entities from the relatedness datasets and all ED sets
i) From Wiki canonical pages: 
th entities/relatedness/filter_wiki_canonical_words_RLTD.lua  -root_data_dir  $DATA_PATH

ii) From context windows surrounding Wiki hyperlinks: 
th entities/relatedness/filter_wiki_hyperlink_contexts_RLTD.lua -root_data_dir $DATA_PATH

18 Now we train entity embeddings for the restricted set of entities
mkdir $DATA_PATH/generated/ent_vecs
th entities/learn_e2v/learn_a.lua -root_data_dir $DATA_PATH | log_train_entity_vecs

part 5: propressing with HIPE file
19 pre-procssing HIPE to AIDA and end2end EL requested file format
python prepro_hipe.py

20 converting datasets to tfrecords
python prepro_hipe_util.py

21 Training the Neural Network.
python3 -m model.train   --batch_size=4   --experiment_name=hipe  --training_name=group_global/global_model_v$v  --ent_vecs_regularization=l2dropout  --evaluation_minutes=10 --nepoch_no_imprv=6  --span_emb="boundaries"   --dim_char=50 --hidden_size_char=50 --hidden_size_lstm=150 --nn_components=pem_lstm_attention_global  --fast_evaluation=True  --all_spans_training=True  --attention_ent_vecs_no_regularization=True  --final_score_ffnn=0_0  --attention_R=10 --attention_K=100  --train_datasets=HIPE-data-v1.0-train-de  --el_datasets=HIPE-data-v1.0-train-de_z_HIPE-data-v1.0-dev-de_z_HIPE-data-v1.0-test-de --el_val_datasets=0  --global_thr=0.001 --global_score_ffnn=0_0
