from requests import get, post, delete

print(get('http://localhost:5000/api/congs').json())
print(get('http://localhost:5000/api/congs/1').json())
# print(post('http://localhost:5000/api/congs',
#            json={'title': '8 марта',
#                  'text': 'Поздравляю !',
#                  'accepter_id': 3,
#                  'sender_id': 2,
#                  'holiday_id': 1}).json())

# print(delete('http://localhost:5000/api/congs/1').json())

print(post('http://localhost:5000/api/congs/2', json={'id': 2, 'title': 'Лучшее поздравление',
                                                      'text': 'Поздравляю от души', 'accepter_id': 2,
                                                      'sender_id': 2, 'holiday_id': 2}).json())
