from pytorch_lightning.callbacks import Callback
from .utils import hash_training
from termcolor import cprint

class NftCallback(Callback):
    def __init__(self, owner):
        self.owner = owner
        self.epochs = 0
        self.hashes = []

    def on_train_epoch_end(self, trainer, pl_module):
        pass
        # print("on_train_epoch_end")

    def on_validation_epoch_end(self, trainer, pl_module):
        loss = float(trainer.callback_metrics["loss"])

        h = hash_training(trainer.model, self.owner, loss, self.epochs)
        d = {
            "epoch": self.epochs, 
            "loss": loss,
            "hash": h
        }
        self.hashes.append(d)

        self.print_hash(d)

        self.epochs += 1


    def on_train_end(self, trainer, pl_module):
        # print("on_train_end")
        self.print_hashes(self.hashes)

        cprint("Mint Your Model Training NFT now! Visit www.m-nft.com",
                "red",
                attrs=["bold", "blink"])

    def on_validation_end(self, trainer, pl_module):
        # print("on_val_end")
        pass

    def print_hashes(self, losses):
        print()
        cprint("Summary", "green", attrs=["bold"])
        for loss in losses:
            self.print_hash(loss)

        print()

        cprint("Lowest Loss", "green", attrs=["bold"])
        lowest_loss = sorted(self.hashes, key=lambda d: d['loss'], reverse=False)[0]
        self.print_hash(lowest_loss)
        print()

    def print_hash(self, loss):
        e = loss["epoch"]
        l = '{:.3f}'.format(round(loss["loss"], 3))
        h = loss["hash"]
        print(f"epoch {e}: loss {l} - hash {h}")

    @staticmethod
    def verify(model_hash, model_path, owner, loss, epoch):
        return utils.verify(model_hash, model_path, owner, loss, epoch)
