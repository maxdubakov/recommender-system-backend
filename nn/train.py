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


def retrain_model(model: NCF, new_train_ratings):
    model.ratings = new_train_ratings

    trainer = pl.Trainer(max_epochs=Config.epochs, gpus=Config.gpus,
                         reload_dataloaders_every_n_epochs=Config.reload_dataloaders_every_n_epochs,
                         progress_bar_refresh_rate=Config.progress_bar_refresh_rate,
                         logger=Config.verbose)
    if Config.verbose:
        print('Retraining the model...')

    trainer.fit(model)

    if Config.save_model:
        torch.save(model.state_dict(), Config.save_path)
        print(f'The NFC model has been saved to the {Config.save_path}')

    return model


if __name__ == '__main__':
    all_beer_ids = pkl.load(open('./nn/models/all_beer_ids.pkl', 'rb'))
    loaded_model = NCF(33388, 77318, [], all_beer_ids)
    loaded_model.load_state_dict(torch.load('./nn/models/model_dict.pt'))
    loaded_model.eval()

    new_ratings = pkl.load(open('./nn/data/data.pkl', 'rb'))
    retrain_model(loaded_model, new_ratings)
