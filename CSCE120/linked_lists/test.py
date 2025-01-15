

bal = 2 * 10 ** 6
son_money = 0
years = 0
print(f'bal: {bal}')
print(f'son: {son_money}')


while bal > 0:
    years += 1
    bal *= (1 + 0.08)
    bal -= 300 * 1000
    son_money += 300 * 1000
    print(f'year: {years}')
    print(f'bal: {bal}')
    print(f'son: {son_money}')



