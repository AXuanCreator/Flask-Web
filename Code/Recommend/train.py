import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd

from network import RecommendNet
from Config import TrainConfig, BookRating
from Code.app import create_app

app = create_app()


class RecommendDataset(Dataset):
    def __init__(self, data):
        self.user_ids = data['user_id'].values
        self.book_ids = data['book_id'].values
        self.rating = data['rating'].values

    def __len__(self):
        return len(self.user_ids)

    def __getitem__(self, item):
        user_id = self.user_ids[item]
        book_id = self.book_ids[item]
        rating = self.rating[item]

        return torch.tensor(user_id, dtype=torch.float), torch.tensor(book_id, dtype=torch.float), torch.tensor(rating, dtype=torch.float)


def train():
    with app.app_context():
        book_rating_data = BookRating.query.limit(10000).all()

    data = {
        'user_id': [br.user_id for br in tqdm(book_rating_data, desc='User ID Load')],
        'book_id': [br.book_id for br in tqdm(book_rating_data, desc='Book ID Load')],
        'rating': [br.rating for br in tqdm(book_rating_data, desc='Rating Load')]
    }
    df = pd.DataFrame(data)  # 转为DataFrame

    dataset = RecommendDataset(df)

    # 64个记录为一批次，并打乱
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

    model = RecommendNet()
    criterion = nn.MSELoss()  # 损失函数
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # 优化器

    for epoch in tqdm(range(TrainConfig.epoch), desc="EPOCH : "):
        model.train()  # 训练模式
        for user_id, book_id, rating in data_loader:
            if len(user_id) != 64:
                continue
            optimizer.zero_grad()  # 清空梯度
            output = model(user_id, book_id)

            print(f'\033[35m[DEBUG]\033[0m | OUTPUT : {output.shape}')
            loss = criterion(output, rating)  # 损失函数MSE
            loss.backward()

            optimizer.step()  # 优化

            print(f'\033[35m[DEBUG]\033[0m | TRAIN : {epoch} | LOSS : {loss.item()}')


if __name__ == '__main__':
    train()
