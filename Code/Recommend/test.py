import torch
import torch.nn as nn
import torch.optim as optim

# 假设用户特征和图书特征的维度分别为10和20
input_size_user = 10
input_size_book = 20
# 假设输出为推荐的图书数量
output_size = 5
# 定义神经网络模型
class BookRecommendationModel(nn.Module):
	def __init__(self):
		super(BookRecommendationModel, self).__init__()
		self.fc_user = nn.Linear(input_size_user, 64) # 用户特征线性层
		self.fc_book = nn.Linear(input_size_book, 64) # 图书特征线性层
		self.fc_combined = nn.Linear(128, 64) # 合并后的线性层
		self.fc_output = nn.Linear(64, output_size) # 输出层

	def forward(self, user_features, book_features):
		user_output = torch.relu(self.fc_user(user_features)) # 用户特征线性层 + ReLU激活函数
		book_output = torch.relu(self.fc_book(book_features)) # 图书特征线性层 + ReLU激活函数
		combined_features = torch.cat((user_output, book_output), dim=1) # 合并用户和图书特征
		combined_output = torch.relu(self.fc_combined(combined_features)) # 合并后的线性层 + ReLU激活函数
		output = torch.softmax(self.fc_output(combined_output), dim=1) # 输出层 + Softmax激活函数
		return output

# 创建模型实例
model = BookRecommendationModel()
# 定义损失函数
criterion = nn.CrossEntropyLoss()
# 定义优化器
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 假设有一批用户特征和图书特征的训练数据
# user_features_tensor为用户特征的Tensor，shape为(batch_size, input_size_user)
# book_features_tensor为图书特征的Tensor，shape为(batch_size, input_size_book)
# targets_tensor为目标标签，即用户真实喜欢的图书索引，shape为(batch_size,)
# 这里的索引应该是0到output_size-1之间的整数
# 这里为了简化示例，使用了随机生成的数据
user_features_tensor = torch.randn(32, input_size_user)
book_features_tensor = torch.randn(32, input_size_book)
targets_tensor = torch.randint(0, output_size, (32,))

# 训练模型
num_epochs = 10
for epoch in range(num_epochs):
	# 前向传播
	outputs = model(user_features_tensor, book_features_tensor)
	# 计算损失
	loss = criterion(outputs, targets_tensor)
	# 反向传播
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()

	print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

# 保存模型
torch.save(model.state_dict(), 'book_recommendation_model.pth')
