import cv2
import numpy as np

# Функция для генерации L-систем
def generate_l_system(axiom, rules, iterations):
    for _ in range(iterations):
        axiom = ''.join(rules.get(c, c) for c in axiom)
    return axiom

# Функция для рисования снежинки на большом холсте и последующей обрезке
def draw_and_crop_snowflake(axiom, angle, step_size, max_iterations):
    direction = 0
    x, y = 0, 0
    path = [(x, y)]
    stack = []

    # Генерация пути снежинки
    for iteration in range(max_iterations):
        for command in axiom:
            if command == 'F':
                x, y = x + step_size * np.cos(np.radians(direction)), y + step_size * np.sin(np.radians(direction))
                path.append((x, y))
            elif command == '+':
                direction += angle
            elif command == '-':
                direction -= angle
            elif command == '[':
                stack.append((x, y, direction))
            elif command == ']':
                x, y, direction = stack.pop()
            else:
                continue  # Пропуск неизвестных команд

        # Проверка размера снежинки
        min_x, min_y = np.min(path, axis=0)
        max_x, max_y = np.max(path, axis=0)
        if max_x - min_x > 500 or max_y - min_y > 500:
            break

    # Нормализация и центрирование пути
    path = np.array(path)
    path -= [min_x, min_y]
    scale = 500 / max(max_x - min_x, max_y - min_y)
    path *= scale
    path += (500 - np.max(path, axis=0)) / 2

    return path

# Список L-систем
l_systems = [
##    ("F--F--F", {"F": "F+F--F+F"}, 60),
##    ("F+F+F+F", {"F": "FF+F+F+F+FF"}, 90),
##    ("F+F+F+F", {"F": "FF+F++F+F"}, 90),
##    ("F+F+F+F", {"F": "F-F+F+F-F"}, 90),
##    ("F+F+F+F", {"F": "F+F-F-F+F"}, 90),
##    ("F+F+F", {"F": "F-F+F"}, 120),
##    ("X", {"X": "X+YF++YF-FX--FXFX-YF+", "Y": "-FX+YFYF++YF+FX--FX-Y"}, 60),#!!!
    ("F+F+F+F", {"F": "FF+F+F+F+F+F-F"}, 90),
##    ("F+F+F+F+F+F", {"F": "F+F-F-F+F"}, 60),
##    ("F+F+F+F+F+F", {"F": "FF+F++F+F"}, 60),
##    ("F+F+F+F+F", {"F": "F+F-F-F+F+F+F-F"}, 45),
##    ("X", {"X": "YX-F-F+XF-F+Y", "Y": "XF+F-F-YF-F+X"}, 90),
##    ("X", {"X": "YX-F-F+XF-F+Y", "Y": "XF-F-F-YF-F-X"}, 130)
]

# Выбор случайной L-системы
axiom, rules, angle = l_systems[np.random.randint(len(l_systems))]

# Генерация L-системы
generated_axiom = generate_l_system(axiom, rules, 4)

# Рисование снежинки
path = draw_and_crop_snowflake(generated_axiom, angle, 10, 10)

# Определяем внутренний и внешний цвета для градиента
inner_color = (255, 255, 128) 
outer_color = (255,128, 0)  

# Создание изображения с прозрачным фоном
image = np.zeros((500, 500, 4), dtype=np.uint8)

# Рисуем линии снежинки
line_thickness = 2
for i in range(1, len(path)):
    cv2.line(image, tuple(path[i-1].astype(int)), tuple(path[i].astype(int)), (255, 255, 255, 255), line_thickness)

# Создаем массив для градиентного фона с альфа-каналом
gradient_alpha = np.zeros((500, 500, 4), dtype=np.uint8)

# Создаем радиальный градиент от синего к белому
center_x, center_y = 250, 250  # Центр градиента
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        # Расстояние от центра
        distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        ratio = distance / max_distance
        ratio = np.clip(ratio, 0, 1)

        # Интерполяция между внутренним и внешним цветами
        gradient_color = tuple((np.array(inner_color) * (1 - ratio) + np.array(outer_color) * ratio).astype(int))
        gradient_alpha[y, x, :3] = gradient_color
        gradient_alpha[y, x, 3] = 255  # полностью непрозрачный для градиента

# Маска для линий снежинки
mask = image[:, :, 3] == 255

# Применяем градиент только к линиям снежинки
image[mask] = gradient_alpha[mask]

# Сохранение изображения в формате .webp
output_filename = "snowflake.webp"
cv2.imwrite(output_filename, image)
output_filename = "snowflake.png"
cv2.imwrite(output_filename, image)
# Отображение изображения
cv2.imshow('Snowflake', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
