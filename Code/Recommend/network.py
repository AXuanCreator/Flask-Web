import torch

from torch import nn

class RecommendNet(nn.Module):
	def __init__(self, embedding_size=1, embedding_dim=32):
		super(RecommendNet, self).__init__()

		self.user_embedding = nn.Embedding(embedding_size, embedding_dim)  # 向量展平
		self.book_embedding = nn.Embedding(embedding_size, embedding_dim)

		# FC层
		self.fc1 = nn.Linear(64*2, 128*2)
		self.fc2 = nn.Linear(128*2, 128)
		self.fc3 = nn.Linear(128, 64)

		# 激活函数
		self.relu = nn.ReLU()

	def forward(self, user_id, book_id):
		# user_embd = self.user_embedding(user_id)
		# book_embd = self.book_embedding(book_id)
		x = torch.cat([user_id, book_id], dim=0)  # 使两个矩阵在第一维度拼接

		# FORWARD
		x = self.relu(self.fc1(x))
		x = self.relu(self.fc2(x))
		output = self.relu(self.fc3(x))
		# output = self.relu(self.fc4(x))

		return output




