def cicle_while (i):
	k=0
	if i<1:
		i=1
	while k<i:
		print (k*"*")
		k+=1



print("Hello World!")
print(" ")

for i in range (2,51):
	print (i)
	if i%2 == 0:
		print ("even")
	else:
		print ("odd")
	cicle_while (i)
	print(" ")


