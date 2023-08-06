from hashlib import sha256
import time
import torch
from datetime import datetime

def sha(string): return sha256(string.encode()).hexdigest()

def get_model_size(model):
    "return model size in mb"
    param_size = 0
    for param in model.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()

    size_all_mb = (param_size + buffer_size) / 1024**2
    return size_all_mb

def hash_model_weights(model):
    # we could use `named_parameters()` here as well
    return sha(str(list(model.parameters())))

def hash_train_data(data):
    # TODO
    # hashing the whole data probably does not make sense
    pass

def hash_training(model, owner, loss, epoch, date=datetime.now()):
    model_hash = hash_model_weights(model)
    size       = str(get_model_size(model))
    date       = str(date)
    loss       = '{:.3f}'.format(loss)
    epoch      = str(epoch)

    s = model_hash + owner + size + date + loss + epoch
    return sha(s)

def verify(model_hash, model_path, owner, loss, epoch, date):
    "verify if `model_hash` is correct"
    model = torch.load(model_path)
    return model_hash == hash_training(model, owner, loss, epoch, date)
