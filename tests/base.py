import base64
# user, passw = 'Costa', 'Kadavr8956'
# pair = f'{user}:{passw}'
#
# base = base64.b64encode(bytes(f'{user}:{passw}', 'utf-8')).decode()
# post = 'Q29zdGE6S2FkYXZyODk1Ng=='
#
# print(base == post)

credentials = base64.b64encode(b'Test_user:Password8956').decode('utf-8')
post = 'Basic VGVzdF91c2VyOlBhc3N3b3JkODk1Ng=='
print(credentials, post)
print(credentials == post)
