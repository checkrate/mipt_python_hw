import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw'))
TRAIN_IMG_DIR = os.path.join(DATA_DIR, 'train', 'original')
TRAIN_MASK_DIR = os.path.join(DATA_DIR, 'train', 'mask')
TEST_IMG_DIR  = os.path.join(DATA_DIR, 'test',  'original')
TEST_MASK_DIR = os.path.join(DATA_DIR, 'test',  'mask')
RESULTS_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results', 'experiments.csv'))

# Classic CV parameters
CV = {
    'threshold_block': 51,
    'min_area': 100,
}

# ML (patch-based) parameters
ML = {
    'patch_size': 64,
    'stride': 32,
    'rf_params': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42,
    }
}

# DL (U-Net) parameters
DL = {
    'in_channels': 3,
    'out_channels': 1,
    'features': [64, 128, 256, 512],
    'lr': 1e-3,
    'batch_size': 8,
    'epochs': 20,
    'device': 'cuda' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu',
}