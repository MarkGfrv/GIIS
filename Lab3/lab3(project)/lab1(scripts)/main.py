import os

print("\n1. Алгоритм ЦДА\n2. Алгоритм Брезенхема\n3. Алгоритм Ву")
choice = input("Ваш выбор:")
if choice == '1':
    os.system('python DDA.py')
elif choice == '2':
    os.system('python Brezenhem.py')
elif choice == '3':
    os.system('python Vu.py')
