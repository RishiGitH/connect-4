
from utils.config import conf




def get_row(game, col):
	for row in range(conf.row_count):
		if game[row][col] == 0:
			return row
	return False



def check_winning(game, coin):

	for col in range(conf.column_count-3):
		for row in range(conf.row_count):
			if game[row][col] == coin and game[row][col+1] == coin and game[row][col+2] == coin and game[row][col+3] == coin:
				return True


	for col in range(conf.column_count):
		for row in range(conf.row_count-3):
			if game[row][col] == coin and game[row+1][col] == coin and game[row+2][col] == coin and game[row+3][col] == coin:
				return True

	for col in range(conf.column_count-3):
		for row in range(conf.row_count-3):
			if game[row][col] == coin and game[row+1][col+1] == coin and game[row+2][col+2] == coin and game[row+3][col+3] == coin:
				return True


	for col in range(conf.column_count-3):
		for row in range(3, conf.row_count):
			if game[row][col] == coin and game[row-1][col+1] == coin and game[row-2][col+2] == coin and game[row-3][col+3] == coin:
				return True
