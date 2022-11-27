# -*- coding:utf-8 -*-
#Input: slices of vulnerability types (4 files in SLICES_DIR)
#		dictionary of vulnerabilities found in NVD src code, given by dealfile.py
#Output: the LABEL_SOURCE_DIR directory of labels for each kind of vul.
import pickle
import os
import sys
sys.path.append('..')
from Implementation.ProjectDir import SLICES_DIR, LABEL_SOURCE_DIR
from make_label import is_number, trim_sentence_list, trim_slice_lists

# Get dict when being imported or executed
with open('./vul_context_func.pkl','rb') as f:
	NVD_vul_line_dict = pickle.load(f)
f.close()

def make_label(slicelists, _dict):	
	_labels = {}
    
	# if slicelists[0] == '':
	# 	del slicelists[0]
	# if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
	# 	del slicelists[-1]
	
	trim_slice_lists(slicelists)

	for slice in slicelists:
		sentences = slice.split('\n')

		if sentences == []:
			continue
		
		trim_sentence_list(sentences)
	
		slicename = sentences[0]
		label = 0
		key = './' + ('/').join(slicename.split(' ')[1].split('/')[-4:])  #key in label_source
		if key not in _dict.keys():
			_labels[slicename] = 0
			continue
		if len(_dict[key]) == 0:
			_labels[slicename] = 0
			continue
		sentences = sentences[1:]
		for sentence in sentences:
			if (is_number(sentence.split(' ')[-1])) is False:
				continue
			linenum = int(sentence.split(' ')[-1])  
			vullines = _dict[key]
			if linenum in vullines:
				label = 1
				_labels[slicename] = 1
				break 
		if label == 0:
			_labels[slicename] = 0	

	return _labels

# write to label file - main function for each kind of slice
def write_label_to_file(slicelists, target_label_file, filemode = 'wb'):
	label_list = make_label(slicelists, NVD_vul_line_dict)
	
	with open(target_label_file, filemode) as f:
		pickle.dump(label_list, f)
	f.close()


if __name__ == '__main__':

	#print(_dict)

	# slice = './data_source/linux_kernel/'  #slice code of software
	# label_path = './C/label_source/linux_kernel/'   #labels
	
    for file in os.listdir(SLICES_DIR):
        print(file)
        abs_file_path = os.path.join(SLICES_DIR, file)
        file_name = file.split('.')[0]
        target_file_path = os.path.join(LABEL_SOURCE_DIR, file_name + '_label.pkl')
        
        f = open(abs_file_path, 'r')
        slicelists = f.read().split('------------------------------')
        f.close()

        write_label_to_file(slicelists, target_file_path)
