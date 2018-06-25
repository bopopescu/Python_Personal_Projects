import datetime

print('arquivo_{}'.format(datetime.date.today()))



li = []
print(len(li))
li = [1,2,3,4,5,6,7,8,9,10]
for idx,val in enumerate(li):
	print('Indice: {}; Valor: {}'.format(idx, val))

	# if val%2 == 0:
	# 	print('Removendo índice: {} com o valor: {}'.format(idx, val))
	# 	del li[idx]

	if val%2 == 0:
		print('Removendo índice: {} com o valor: {}'.format(idx, val))
		li.pop(idx)

	print('Quantidade de elementos na lista: {}'.format(len(li)))

print(len(li))