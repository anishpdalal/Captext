# project/server/entries/views.py

from random import randrange
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import Entry, User

entries_blueprint = Blueprint('entries', __name__)


class ListCreateEntryAPI(MethodView):
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
                            'text': entry.text,
                            'keywords': entry.keywords,
                            'url': entry.url,
                            'title': entry.title,
                            'created_on': entry.created_on.strftime('%m/%d/%Y'),
                            'status': 'success',
                            'message': 'created new entry'
                        }
                    else:
                        return make_response(
                                jsonify({'status': 'fail', 'message': 'Please provide url, title, and text'}))
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

    def get(self):
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
                    results = [self.to_dict(entry) for entry in
                               Entry.query.filter_by(user_id=user.id).order_by(Entry.created_on.desc()).all()]
                    response_object = {
                        'status': 'success',
                        'message': 'retrieved entries',
                        'results': results
                    }
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

    def get_recommendation(self, entry):
        recommendations = Entry.query.filter_by(url=entry.url).filter(Entry.user_id != entry.user_id).all()
        if recommendations:
            random_index = randrange(0, len(recommendations))
            recommendation = recommendations[random_index]
            return dict(url=recommendation.url, title=recommendation.title)
        else:
            return None

    def to_dict(self, entry):
        return dict(user_id=entry.user_id,
                    id=entry.id,
                    text=entry.text,
                    created_on=entry.created_on.strftime('%m/%d/%Y'),
                    categories=entry.keywords.split(", "),
                    url=entry.url,
                    title=entry.title,
                    recommendation=self.get_recommendation(entry))


list_create_entry_view = ListCreateEntryAPI.as_view('create_entry_api')

entries_blueprint.add_url_rule(
        '/entries',
        view_func=list_create_entry_view,
        methods=['GET', 'POST']
)
