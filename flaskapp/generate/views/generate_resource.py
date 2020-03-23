from flask.views import MethodView
from flask import jsonify
from flaskapp.extensions.api import api
from flaskapp.generate.views.blueprint import generate
from patientgenerator.generator import generate_bundle

class FHIRGenerateAPI(MethodView):
    def get(self, _version):
        return jsonify(generate_bundle())


generate_view = FHIRGenerateAPI.as_view('generate')

api.add_url_rule(
    generate.url_prefix,
    view_func=generate_view,
    methods=['GET'],
)

api.add_url_rule(
    generate.url_prefix + '/',
    view_func=generate_view,
    methods=['GET'],
)
