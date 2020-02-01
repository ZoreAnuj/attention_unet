from utils import *
from model import AttentionUNet
from torchvision.utils import make_grid
from train import train_and_test
from loss import dice_coeff, FocalLoss
import torch.nn as nn


data_dir = 'data'
batch_size = 4
epochs = 100
dataloaders = get_data_loaders(data_dir, batch_size=batch_size)


def train():
    model = AttentionUNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    criterion = FocalLoss()

    trained_model = train_and_test(model, dataloaders, optimizer, criterion, num_epochs=epochs)

    return trained_model


def plot_prediction(model, dataloaders):

    dataiter = iter(dataloaders['test'])
    batch = dataiter.next()

    f = plt.figure(figsize=(20, 20))
    grid_img = make_grid(batch['mask'])
    grid_img = grid_img.permute(1, 2, 0)
    plt.imshow(grid_img)
    plt.title('Ground truth')
    plt.show()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = batch['image'].to(device)
    prediction = model(inputs).detach().cpu()

    f = plt.figure(figsize=(20, 20))
    grid_img = make_grid(prediction)
    grid_img = grid_img.permute(1, 2, 0)
    plt.imshow(grid_img)
    plt.title('Prediction')
    plt.show()


'''trained_model = train()
plot_prediction(trained_model, dataloaders)'''

plot_batch_from_dataloader(dataloaders, 4)

