import getopt
import sys

import pytorch_lightning as pl
import pickle as pkl

import torch

try:
    from config import Config
    from NCF import NCF
except ImportError:
    from .NCF import NCF
    from .config import Config


def train(num_users, num_items, train_ratings, all_beer_ids):
    model = NCF(num_users, num_items, train_ratings, all_beer_ids)
    trainer = pl.Trainer(max_epochs=Config.epochs, gpus=Config.gpus,
                         reload_dataloaders_every_n_epochs=Config.reload_dataloaders_every_n_epochs,
                         logger=Config.verbose,
                         enable_checkpointing=False,
                         callbacks=[
                             pl.callbacks.progress.TQDMProgressBar(refresh_rate=Config.progress_bar_refresh_rate)
                         ])
    if Config.verbose:
        print('Training the model...')

    trainer.fit(model)

    if Config.save_model:
        with open(Config.save_path, 'wb+') as f:
            pkl.dump(model, f, protocol=pkl.HIGHEST_PROTOCOL)
        if Config.verbose:
            print(f'The NFC model has been saved to the {Config.save_path}')

    return model


def retrain_model(model: NCF, new_train_ratings):
    model.ratings = new_train_ratings

    trainer = pl.Trainer(max_epochs=Config.retrain_epochs, gpus=Config.gpus,
                         reload_dataloaders_every_n_epochs=Config.reload_dataloaders_every_n_epochs,
                         enable_model_summary=False,
                         logger=Config.verbose,
                         enable_checkpointing=False,
                         callbacks=[
                             pl.callbacks.progress.TQDMProgressBar(refresh_rate=Config.progress_bar_refresh_rate)
                         ])
    if Config.verbose:
        print('Retraining the model...')

    trainer.fit(model)

    if Config.save_model:
        torch.save(model.state_dict(), Config.save_path)
        print(f'The NFC model has been saved to the {Config.save_path}')

    return model


def load_args(argv):
    _num_users = Config.DEFAULT_NUM_USERS
    _num_items = Config.DEFAULT_NUM_ITEMS
    try:
        opts, args = getopt.getopt(argv, "u:i:", ["num_users=", "num_items="])
        for opt, arg in opts:
            if opt in ['-u', '--num_users']:
                _num_users = int(arg)
            elif opt in ['-i', '--num_items']:
                _num_items = int(arg)
    except getopt.GetoptError:
        print('\033[91mERROR: Arguments (-u [--num_users][int], -i [--num_items][int]) are currently supported.\033[0m')
        sys.exit(2)
    except ValueError:
        print('\033[91mERROR: Arguments have to be integers\033[0m')
        sys.exit(3)

    return _num_users, _num_items


if __name__ == '__main__':
    num_users, num_items = load_args(sys.argv[1:])
    all_beer_ids = pkl.load(open('./nn/models/all_beer_ids.pkl', 'rb'))

    loaded_model = NCF(num_users, num_items, [], all_beer_ids)
    loaded_model.load_state_dict(torch.load(Config.load_path))
    loaded_model.eval()

    new_ratings = pkl.load(open('./nn/data/data.pkl', 'rb'))
    retrain_model(loaded_model, new_ratings)
