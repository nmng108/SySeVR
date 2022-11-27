from os import path

# Full path (absolute path)

IMPLEMENTATION_DIR = path.dirname(__file__)
SRC2SLICE_DIR = path.join(IMPLEMENTATION_DIR, 'source2slice')
DATA_PREPROCESS_DIR = path.join(IMPLEMENTATION_DIR, 'data_preprocess')
MODEL_DIR = path.join(IMPLEMENTATION_DIR, 'model')

ROOT_DIR = path.dirname(IMPLEMENTATION_DIR)

DATA_DIR = path.join(ROOT_DIR, "data")
SOURCE_DATA = path.join(DATA_DIR, "source_data")

NVD_SOURCE_DATA = path.join(SOURCE_DATA, "NVD")
NVD_DIFF = path.join(NVD_SOURCE_DATA, "diff")
NVD_FUNC_CODE = path.join(NVD_SOURCE_DATA, "func_code")

SARD_SOURCE_DATA = path.join(SOURCE_DATA, "SARD")

# Phase 1
JOERNINDEX_DIR = path.join(DATA_DIR, ".joernIndex")
SLICES_DIR = path.join(DATA_DIR, "slices")
LABEL_SOURCE_DIR = path.join(DATA_DIR, "label_source")
SLICE_LABEL_DIR = path.join(DATA_DIR, "slice_label")

# Phase 2
SLICE_HASH_DIR = path.join(DATA_DIR, "slice_hash")
LIST_DELETE_DIR = path.join(DATA_DIR, "list_delete")

CORPUS_DIR = path.join(DATA_DIR, "corpus")
CORPUS_TRAINSET_DIR = path.join(DATA_DIR, "trainset")
CORPUS_TESTSET_DIR = path.join(DATA_DIR, "testset")

WORD2VEC_DIR = path.join(DATA_DIR, "w2v_model")
W2V_MODEL_PATH = path.join(WORD2VEC_DIR, "wordmodel3")

VECTOR_DIR = path.join(DATA_DIR, "vectors")
MAIN_TRAINSET_DIR = path.join(DATA_DIR, "main_dl_model", "trainset")
MAIN_TESTSET_DIR = path.join(DATA_DIR, "main_dl_model", "testset")

# Phase 3
WEIGHT_PATH = path.join(DATA_DIR, "main_dl_model", "BGRU")
RESULT_PATH = path.join(DATA_DIR, "main_dl_model", "result", "BGRU")