import torch
from torch import nn

from .network import RecommendNet

print('\n')


def infer(borrow_list, book_list):
	model = RecommendNet(1)
	model.load_state_dict(torch.load('./Recommend/checkpoints/model_epoch_latest.pth'))

	model.eval()  # 设置为评估模式

	borrow_book = torch.tensor([borrow_list], dtype=torch.float32)
	book_list = torch.tensor([book_list], dtype=torch.float32)
	if borrow_book.shape[1] > 7:
		borrow_book = borrow_book[:, :7]  # 截断，利于产生较少的噪音
	else:
		borrow_book = torch.cat([borrow_book,
		                         torch.zeros(1, 7 - borrow_book.shape[1])], dim=1)

	output_list = []
	for i in range(book_list.shape[1]):
		input = torch.cat([borrow_book, book_list[:, i][None]], dim=1)

		# 对input进行归一化
		mean = input.mean()
		std = input.std()
		input = (input - mean) / std

		output_list.append(model(input).item())

	return output_list


def test():
	model = RecommendNet(1)
	model.load_state_dict(torch.load('./Recommend/checkpoints/model_epoch_latest.pth'))

	model.eval()  # 设置为评估模式

	borrow_list = [31, 665, 3074, 3581]
	book_list = [4829, 6646, 6703, 7487, 8072]
	rating = [3, 4, 4, 5, 5]

	borrow_book = torch.tensor([borrow_list], dtype=torch.float32)
	book_list = torch.tensor([book_list], dtype=torch.float32)
	if borrow_book.shape[1] > 7:
		borrow_book = borrow_book[:, :7]  # 截断，利于产生较少的噪音
	else:
		borrow_book = torch.cat([borrow_book,
		                         torch.zeros(1, 7 - borrow_book.shape[1])], dim=1)

	for i in range(book_list.shape[1]):
		input = torch.cat([borrow_book, book_list[:, i][None]], dim=1)

		# 对input进行归一化
		mean = input.mean()
		std = input.std()
		input = (input - mean) / std

		output = model(input)
		print(f'\033[35m[DEBUG]\033[0m | REAL : {rating[i]} | PREDICT : {output.item()}')


if __name__ == '__main__':
	test()
