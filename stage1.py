import click
import torch

from stage1_utils.dataset import ImageFolderDataset
from net import StageNet

torch.backends.cudnn.benchmark = True


@click.command()
@click.option('--name', type=str)
@click.option('--dataset_root', default='../data/stage1_data')
@click.option('--image_size', default=(404, 404), type=(int, int))
@click.option('--epochs', default=20, type=int)
@click.option('--batch_size', default=8, type=int)
@click.option('--workers', default=8, type=int)
@click.option('--resume', type=click.Path(exists=True))
def main(name, dataset_root, image_size, epochs, batch_size, workers, resume):

    print('===> Prepare data loader')
    dataset_args = {'root': dataset_root, 'target_size': image_size}
    loader_args = {'num_workers': workers, 'pin_memory': True}

    train_loader = torch.utils.data.DataLoader(
        dataset=ImageFolderDataset(phase='train', **dataset_args),
        batch_size=batch_size, shuffle=True, **loader_args
    )
    validate_loader = torch.utils.data.DataLoader(
        dataset=ImageFolderDataset(phase='test', **dataset_args),
        batch_size=batch_size, **loader_args
    )
    trainval_loader = torch.utils.data.DataLoader(
        dataset=ImageFolderDataset(phase='all', **dataset_args),
        batch_size=batch_size, shuffle=True, **loader_args
    )

    print('===> Prepare model')
    net = StageNet(name='stage1_ResFCN' + name, pretrained=False, l1_weight=0)

    print('===> Start training')
    net.train(train_loader=train_loader,
              validate_loader=validate_loader,
              epochs=epochs)
    net.evaluate(data_loader=validate_loader, prefix='')


if __name__ == '__main__':
    main()
