import flask
from flask import jsonify, request

from data import db_session
from data.congratulations import Congratulations

blueprint = flask.Blueprint(
    'congs_api',
    __name__,
    template_folder='templates'
)


# получение всех поздравлений
@blueprint.route('/api/congs')
def get_congs():
    db_sess = db_session.create_session()
    congs = db_sess.query(Congratulations).all()
    return jsonify(
        {
            'congratulations':
                [item.to_dict(only=('title', 'text', 'accepter.name', 'holiday.title'))
                 for item in congs]
        }
    )


# получение одного поздравления по id
@blueprint.route('/api/congs/<int:id>', methods=['GET'])
def get_one_cong(id):
    db_sess = db_session.create_session()
    cong = db_sess.query(Congratulations).get(id)
    if not cong:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'congratulations': cong.to_dict(only=('title', 'text', 'accepter.name', 'holiday.title'))
        }
    )


# добавление нового поздравления
@blueprint.route('/api/congs', methods=['POST'])
def create_cong():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'text', 'accepter_id', 'holiday_id', 'sender_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    cong = Congratulations(
        title=request.json['title'],
        text=request.json['text'],
        accepter_id=request.json['accepter_id'],
        sender_id=request.json['sender_id'],
        holiday_id=request.json['holiday_id']
    )
    db_sess.add(cong)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# удаление поздравления по id
@blueprint.route('/api/congs/<int:id>', methods=['DELETE'])
def delete_news(id):
    db_sess = db_session.create_session()
    congs = db_sess.query(Congratulations).get(id)
    if not congs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(congs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# редактирование поздравления
@blueprint.route('/api/congs/<int:id>', methods=['POST', 'GET'])
def change_job(id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty requests'})
    if request.method == 'GET':
        cong = db_sess.query(Congratulations).get(id)
        if not cong:
            return jsonify({'congratulations': {}, 'error': 'Not found'})
        return jsonify({'congratulations': cong.to_dict(only=('title', 'text', 'accepter.name', 'holiday.title'))})
    elif request.method == 'POST':
        cong = db_sess.query(Congratulations).get(id)
        if id != request.json['id']:
            return jsonify({'congratulations': {}, 'error': 'Bad request'})
        if not cong:
            return jsonify({'congratulations': {}, 'error': 'Invalid id'})
        cong.id = request.json['id']
        cong.title = request.json['title']
        cong.text = request.json['text']
        cong.accepter_id = request.json['accepter_id']
        cong.sender_id = request.json['sender_id']
        cong.holiday_id = request.json['holiday_id']
        db_sess.merge(cong)
        db_sess.commit()
        return jsonify({'result': 'OK'})
