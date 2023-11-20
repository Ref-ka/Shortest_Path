from random import randint
from algorithm import Graph
from os import path

# vertexes_count = int(input('Input the number of vertexes'))


def make_graph(vertex_count, save, save_file=None):
    generated_connections = {}
    for i in range(vertex_count):
        generated_connections[i] = []
        for j in range(vertex_count):
            if j != i:
                weight = randint(0, 10)
                if weight != 0 and randint(0, 2) != 0 and randint(0, 3) == 0:
                    generated_connections[i].append([j, weight])
    if save:
        save_to_txt(generated_connections, save_file)
    return generated_connections


def save_to_txt(generated_connections, save_file=None):
    number = 0
    while True:
        if path.exists(f'presets\\preset{str(number) if number != 0 else ""}.txt'):
            number += 1
        else:
            break
    with open(f'presets\\preset{number}.txt', 'w') as file:
        for i in generated_connections:
            for line in generated_connections[i]:
                file.write(f'{i} {line[0]} {line[1]}\n')
    # print(generated_connections)


def graph_test(v_count, amount):
    counter = 0
    while True:
        if not v_count:
            vertex_count = randint(3, 10)
        else:
            vertex_count = v_count
        generated_connections = make_graph(vertex_count, 0)
        g = Graph(vertex_count)
        for vertex in generated_connections:
            for line in generated_connections[vertex]:
                g.add_edge(vertex, line[0], line[1])
        counter += 1
        if counter == amount:
            return False
        # print(g.spfa(randint(0, vertex_count - 1)))


while True:
    answer = str(input('Make or test? '))
    if answer == 'make':
        make_graph(int(input('Vertex count: ')), 1,
                   int(input('New file or rewrite preset.txt (0 and 1 respectively): ')))
    elif answer == '0':
        break
    else:
        graph_test(int(input()), int(input()))
