from NCF import NCF
import pytorch_lightning as pl
import pickle as pkl

from config import Config


def train(num_users, num_items, train_ratings, all_beer_ids):
    model = NCF(num_users, num_items, train_ratings, all_beer_ids)
    trainer = pl.Trainer(max_epochs=Config.epochs, gpus=Config.gpus,
                         reload_dataloaders_every_n_epochs=Config.reload_dataloaders_every_n_epochs,
                         progress_bar_refresh_rate=Config.progress_bar_refresh_rate,
                         logger=Config.verbose)
    if Config.verbose:
        print('Training the model...')

    trainer.fit(model)

    if Config.save_model:
        with open(Config.save_path, 'wb+') as f:
            pkl.dump(model, f, protocol=pkl.HIGHEST_PROTOCOL)
        if Config.verbose:
            print(f'The NFC model has been saved to the {Config.save_path}')

    return model


def load():
    with open(Config.load_path, 'rb') as f:
        model = pkl.load(f)
    return model
