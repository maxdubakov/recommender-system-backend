"""This is a config file which possesses all changeable variables"""


class Config(object):

    data_path = './data/beer_new_reviews.csv'
    retrain_data_path = './nn/data/data.pkl'
    num_workers = 4
    dataset_name = 'Beer'
    part_of_dataset_used = 1
    verbose = False
    num_negatives = 4
    hit_ratio = 10
    batch_size = 512
    embedding_dim = 16
    num_user_embeddings_coef = 2
    first_layer = embedding_dim * 2
    first_layer_nn = 64
    second_layer_nn = 32
    save_model = True
    epochs = 5
    retrain_epochs = 5
    gpus = 0
    reload_dataloaders_every_n_epochs = 0
    progress_bar_refresh_rate = 0
    checkpoint_callback = False
    date_cols = ['review_time']
    rank_latest = 'rank_latest'
    model_id = 'latest'
    save_path = f'./nn/models/model_{model_id}.pt'
    load_path = f'./nn/models/model_{model_id}.pt'

    DEFAULT_NUM_USERS = 33388
    DEFAULT_NUM_ITEMS = 77318

    def __init__(self, _num_negatives=4, _batch_size=512, _embedding_dim=8, _epochs=5, _first_layer=16):
        Config.set_num_negatives(_num_negatives)
        Config.set_batch_size(_batch_size)
        Config.set_embedding_dim(_embedding_dim)
        Config.set_epochs(_epochs)
        Config.set_first_layer(_first_layer)

    @staticmethod
    def set_num_negatives(_num_negatives):
        Config.num_negatives = _num_negatives

    @staticmethod
    def set_batch_size(_batch_size):
        Config.batch_size = _batch_size

    @staticmethod
    def set_embedding_dim(_embedding_dim):
        Config.embedding_dim = _embedding_dim

    @staticmethod
    def set_epochs(_epochs):
        Config.epochs = _epochs

    @staticmethod
    def set_first_layer(_first_layer):
        Config.first_layer = _first_layer
