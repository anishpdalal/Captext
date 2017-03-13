# project/server/entries/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import Entry, User

entries_blueprint = Blueprint('entries', __name__)


class CreateEntryAPI(MethodView):
    """
    User Entry Creation resource
    """

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    user = User.query.filter_by(id=resp).first()
                    post_data = request.get_json()
                    if all([post_data.get('text'), post_data.get('url'), post_data.get('title')]):
                        entry = Entry(user_id=user.id,
                                      text=post_data.get('text'),
                                      keywords=post_data.get('keywords', None),
                                      url=post_data.get('url'),
                                      title=post_data.get('title'))

                        db.session.add(entry)
                        db.session.commit()
                        response_object = {
                            'user_id': user.id,
                            'text': post_data.get('text'),
                            'keywords': post_data.get('keywords', None),
                            'url': post_data.get('url'),
                            'title': post_data.get('title'),
                            'status': 'success',
                            'message': 'created new entry'
                            }
                    else:
                        return make_response(jsonify({'status': 'fail', 'message': 'Please provide url, title, and text'}))
                    return make_response(jsonify(response_object)), 200

                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403


create_entry_view = CreateEntryAPI.as_view('create_entry_api')

entries_blueprint.add_url_rule(
    '/entries',
    view_func=create_entry_view,
    methods=['POST']
)
