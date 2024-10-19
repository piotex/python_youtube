

lista = list(range(257))

max_len = 100

res = []
for i in range(1+int(len(lista)/max_len)):
    res.append(lista[i*max_len:(i+1)*max_len])

a = 0


