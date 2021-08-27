# nlp-legal-data-automation
allowing users to automate cumbersome legal processes by reading and understanding legal documents and extracting relevant information from them.


Process: 

1. Raw data(case files) on web converted to HTML(s) and downloaded. 
2. Downloaded HTML(s) converted to JSON(s).
3. JSON(s) converted to text data for annotation.
4. Annotated data(ann files) converted to CoNLL format.
5. All CoNLL files combined into one file for BERT training.
6. BERT trained on one CoNLL file.
7. Trained model saved.
8. Original JSON(s) updated after using the model for prediction of entities - Acts, Cases, Sections, and Articles.
9. Updated JSON(S) used in elastic search.

BERT_model_version3.0: 
Latest trained model with highest accuracy.

Source:
	BERT_training_using_CoNLL:
	For training the BERT model in google collab.
	Input: CoNLL file
	Output: BERT trained model

	HTML_creation:
	Input: Excel file with link to be downloaded
	Output: HTML files
	
	HTML_to_JSON:
	Used to iteratively convert all HTML files in all folders to JSON files in a given court folder(includes 		equivalent citations field). JSON files' names are same as HTML(s).

	JSON_to_text_for_annotation:
	For BRAT input(txt files) from JSON – Script to extract para, sub-para, block quote - without sentence splitting 	errors.

	JSON_update_after_training:

	1. Extract_Paragraph_from_JSON(for update).ipynb:
	Acts as an input for JSON update script.
	Input: JSON files' path
	Output: CSV files' for each JSON

	2. BERT_JSON_update.ipynb
	Code to update the existing JSON with tagged entities as predicted by the BERT model.
	Input for JSON update:
		1. CSV with paragraphs, para_id, and content_id.
		2. JSON file to update.
	Output for JSON update: updated JSON file with tagged entities.

	ann_to_CoNLL_for_BERT:
	BRAT output data(.ann file with relationship linking) to CoNLL for BERT training.

	update_JSON_with_good_judges:
	Update the supreme court/hight court json files with the right judge name and corresponding judge id. 			Additionally, bench names with corresponding bench ids.
	input :
	1) Judge validation name JSON file (specific to the court)
	2) Bench validation names JSON file (specific to the court)
	3) Judges' ids JSON file (specific to the court) -- for Judge and bench

	output : updated json files with correct names and ids

Annotation service used: BRAT and Doccano annotation tools.
BRAT annotation tool hosted on AWS EC2 instance.

BERT model:
Bidirectional Encoder Representations from Transformers.
Includes two separate mechanisms — an encoder that reads the text input and a decoder that produces a prediction for the task. As opposed to directional models, which read the text input sequentially (left-to-right or right-to-left), the Transformer encoder reads the entire sequence of words at once. Therefore it is considered bidirectional. This characteristic allows the model to learn the context of a word based on all of its surroundings (left and right of the word).

CoNLL format:
CoNLL is the conventional name for TSV formats in NLP (TSV - tab-separated values).
The "CONLL" file type represents a corpus with one word per line, each word containing tab-separated columns with information about the word (for example: POS tags).
