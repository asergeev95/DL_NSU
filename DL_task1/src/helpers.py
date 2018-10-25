import xml.etree.cElementTree as et
import pandas as pd
import re

def _parse(path):
    d = dict()
    root = et.parse(path)
    rows = root.findall('.//column')
    for row in rows:
        d.setdefault(list(row.attrib.values())[0],[]).append(row.text)
    df_xml = pd.DataFrame.from_dict(d)
    return df_xml
	
def get_parsed_data():
	data_train = pd.DataFrame()
	data_test = pd.DataFrame()

	path_train = ['src/tkk_train_2016.xml', 'src/bank_train_2016.xml']
	path_test = ['src/tkk_test_etalon.xml', 'src/banks_test_etalon.xml']

	for path in path_train:
		df = _parse(path)
		data_train = pd.concat([df, data_train], ignore_index=True)
	for path in path_test:
		df = _parse(path)
		data_test = pd.concat([df, data_test], ignore_index=True)
	return data_train, data_test

def define_label(row):
    if (row == '1').any():
        label = 1
    elif (row == '0').any():
            label = 0
    else:
        label = -1
    return label
	
def clear_text(text):
    text = text.lower().replace("ё", "е")
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()





