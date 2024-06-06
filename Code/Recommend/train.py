import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd

from .network import RecommendNet
from Config import TrainConfig, BookRating, Borrow



class RecommendDataset(Dataset):
    def __init__(self, data):
        self.borrow_ids = data['borrow_book_list'].values
        self.book_ids = data['book_id'].values
        self.rating = data['rating'].values

    def __len__(self):
        return len(self.borrow_ids)

    def __getitem__(self, item):
        with app.app_context():
            borrow_list = self.borrow_ids[item]
            borrow_id = [borrow.book_id for borrow in borrow_list]

            book_id = self.book_ids[item]
            rating = self.rating[item]

        return torch.tensor(borrow_id, dtype=torch.float), torch.tensor(book_id, dtype=torch.float), torch.tensor(rating, dtype=torch.float)

def create_app():
    from Code.app import create_app
    return create_app()


def train():
    with app.app_context():
        book_rating_data = BookRating.query.all()

        data = {
            'borrow_book_list': [Borrow.query.filter_by(user_id=br.user_id) for br in
                                 tqdm(book_rating_data, desc='Borrow List Load')],
            'book_id': [br.book_id for br in tqdm(book_rating_data, desc='Book ID Load')],
            'rating': [br.rating for br in tqdm(book_rating_data, desc='Rating Load')]
        }
    df = pd.DataFrame(data)  # 转为DataFrame

    dataset = RecommendDataset(df)

    # 64个记录为一批次，并打乱
    data_loader = DataLoader(dataset, batch_size=1, shuffle=True)  # 暂不支持多批次训练

    model = RecommendNet(1)
    criterion = nn.MSELoss()  # 损失函数
    optimizer = optim.SGD(model.parameters(), lr=0.01)  # 优化器

    for epoch in tqdm(range(TrainConfig.epoch), desc="EPOCH : "):
        model.train()  # 训练模式
        epoch_loss = 0  # 累计损失

        for borrow_book, book_id, rating in tqdm(data_loader, desc="TRAIN : "):
            # if len(book_id) != 64:  # TODO:这个有点暴力了,需要加上如果borrow_book为None
            #     continue
            if borrow_book.shape[1] == 0:
                continue

            # 拼接两个张量
            if borrow_book.shape[1] > 7:
                borrow_book = borrow_book[:, :7]  # 截断，利于产生较少的噪音
            else:
                borrow_book = torch.cat([borrow_book,
                                         torch.zeros(1, 7 - borrow_book.shape[1])], dim=1)  # 补0，使其符合FC层的输入层要求

            input = torch.cat([borrow_book, book_id[None]], dim=1)

            # 对input进行归一化
            mean = input.mean()
            std = input.std()
            input = (input - mean) / std

            optimizer.zero_grad()  # 清空梯度
            output = model(input)

            loss = criterion(output, rating)  # 损失函数MSE
            loss.backward()
            optimizer.step()  # 优化

            epoch_loss += loss.item()


        print(f'\033[35m[DEBUG]\033[0m | TRAIN : {epoch + 1} | LOSS : {epoch_loss}')

        if (epoch + 1) % 5 == 0:
            torch.save(model.state_dict(), f'./Recommend/checkpoints/model_epoch_{epoch + 1}.pth')


if __name__ == '__main__':
    app = create_app()
    train()
