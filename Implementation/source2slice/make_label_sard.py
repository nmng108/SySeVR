## coding:utf-8
#Input: slices of vulnerability types (4 files in SLICES_DIR)
#		dictionary of vulnerabilities found in SARD src code, given by getVulLineForCounting.py
#Output: the LABEL_SOURCE_DIR directory of labels for each kind of vul.
import os
import pickle
import sys
sys.path.append('..')
from Implementation.ProjectDir import SLICES_DIR, LABEL_SOURCE_DIR, SARD_SOURCE_DATA
from make_label import is_number, trim_sentence_list, trim_slice_lists

def get_SARD_vul_line_number_dictionary(dict_file = SARD_SOURCE_DATA + "/contain_all.txt"):
    f = open(dict_file, 'r')
    vullines = f.read().split('\n')
    f.close()

    _dict = {}
    for i in range(0, len(vullines) - 1):
        vulline = vullines[i]
        filename_details = vulline.split(' ')[0].split('/') # except [-1] element is a C file name
        key = filename_details[-4] + filename_details[-3] + filename_details[-2] + '/' + filename_details[-1]
        linenum = int(vulline.split(' ')[-1])
        if key not in _dict.keys():
            _dict[key] = [linenum]
        else:
            _dict[key].append(linenum)

    return _dict

# Get dict when being imported or executed
SARD_vul_line_dict = get_SARD_vul_line_number_dictionary()


def make_label(slicelists, _dict):
    labels = []
    
    trim_slice_lists(slicelists)
    
    for slicelist in slicelists:
        sentences = slicelist.split('\n')
            
        if sentences == []:
            continue
        
        trim_sentence_list(sentences)
            
        slicename = sentences[0].split(' ')[1].split('/')[-4] + sentences[0].split(' ')[1].split('/')[-3] + sentences[0].split(' ')[1].split('/')[-2] + '/' + sentences[0].split(' ')[1].split('/')[-1]
        sentences = sentences[1:]
        
        label = 0
        
        if slicename not in _dict.keys():
            labels.append(label)
            continue
        else:
            vulline_nums = _dict[slicename]
            for sentence in sentences:
                if (is_number(sentence.split(' ')[-1])) is False:
                    continue
                linenum = int(sentence.split(' ')[-1])
                if linenum not in vulline_nums:
                    continue
                else:
                    label = 1
                    break
        labels.append(label)
    
        return labels
           
# write to label file - main function for each kind of slice
def write_label_to_file(slicelists, target_label_file, filemode = 'wb'):
    label_list = make_label(slicelists, SARD_vul_line_dict)
    
    f = open(target_label_file, filemode)
    pickle.dump(label_list, f, True)
    f.close()


if __name__ == '__main__':
    for file in os.listdir(SLICES_DIR):
        print(file)
        abs_file_path = os.path.join(SLICES_DIR, file)
        file_name = file.split('.')[0]
        target_file_path = os.path.join(LABEL_SOURCE_DIR, file_name + '_label.pkl')
        
        f = open(abs_file_path, 'r')
        slicelists = f.read().split('------------------------------')[:-1]
        f.close()

        write_label_to_file(slicelists, target_file_path)
