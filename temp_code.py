start = int(input("Escribe el inicio del rango: "))
end = int(input("Escribe el final del rango: "))

for num in range(start, end +1):
	if num > 1 and all(num % i != 0 for i in range(2,num)):
		print(num)