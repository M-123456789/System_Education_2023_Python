print ("Программа возведения числа от 1 до 9 в степень от 1 до 512")

n=0
while n==0:
  n=int(input("Введите число: "))
  if n<1 or n>10:
    print("Введите число от 1 до 9.")
    n=0

p=0
while p==0:
  p=int(input("Введите степень: "))
  if p<1 or p>512:
    print("Введите степень от 1 до 512.")
    p=0

decimator = 10
#decimator = 1_000_000_000

m = [n]

if p > 1:
  for i in range (2, p+1):
    perenos = 0
#    print()
#    print("i =", i, "  m =", m, "  len(m) =", len(m))
    for ii in range (len(m)):
      k = perenos + m[ii]*n
#      print ("perenos = ", perenos,"  m = ", m, "  ii = ", ii, "  m[", ii, "] = ", m[ii], "  k = ", k)
      if k>=10 and ii<=len(m)-1:
        m[ii] = k%decimator
#        print ("k>10 and ii<=len(m)-1  ii = ", ii, "  m[", ii, "] = ", m[ii], "  k = ", k)
        perenos = k//decimator
#        print ("perenos = ", perenos)
      elif k<10:
        m[ii] = k
        perenos = 0
#       print ("k<10  ii = ", ii, "  m[", ii, "] = ", m[ii], "  k = ", k)
#      print ("m = ", m, "  ii = ", ii, "  m[", ii, "] = ", m[ii], "  k = ", k, "  perenos = ", perenos)
    if perenos>0:
      m.append(perenos)
#      print ("m = ", m)

print (n, " ^ ", p, " = ")
m.reverse()

k=0
for digit in m:
  print(digit, end="")

print()
print("Длина массива = ", len(m))
print("Массив =", m)

# 3 9 27 81 243 729
# 3
# 9
# 27  2 7
# 2*3+2=8 1
#        24  3  -> 2 4 3
# 12 9 -> 2*3+1  2 9
