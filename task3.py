n = int(input())  # количество строк в лесу
forest = [input().split() for _ in range(n)]

max_mushrooms = 0  # максимальное количество грибов, которые лесник сможет собрать

# расположение лесника
for j in range(3):
   if forest[0][j] != 'W':  # начинаем прогулку только если нет кустов кусачих
       visited = [[False] * 3 for _ in range(n)]  # матрица посещенных клеток
       count = 0  # количество собранных грибов
       stack = [(0, j)]  # стек для обхода клеток
       while stack:
           x, y = stack.pop()
           if 0 <= x < n and 0 <= y < 3 and not visited[x][y] and forest[x][y] == 'C':  # если клетка с грибочками
               count += 1  # увеличиваем количество собранных грибов
               visited[x][y] = True  # отмечаем клетку как посещенную
               stack.append((x + 1, y - 1))  # клетка слева
               stack.append((x + 1, y))  # клетка внизу
               stack.append((x + 1, y + 1))  # клетка справа
       max_mushrooms = max(max_mushrooms, count)  # обновляем максимальное количество грибов

print(max_mushrooms)  # выводим максимальное количество грибов, которые лесник сможет собрать за прогулку
