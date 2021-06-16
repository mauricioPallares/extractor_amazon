data = [
    {'nombre': "camilo",
    'apellidos':"perez"},
    {'nombre': 'omar',
    'apellidos':"lopez"}
]
print(len(data))



def fun():
    return data.pop()

cliente = fun()

print(cliente['nombre'])
print(cliente['apellidos'])
print(len(data))