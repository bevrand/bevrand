from flask import Blueprint, jsonify
import api


coverage_blueprint = Blueprint('coverage', __name__, )


@coverage_blueprint.route('/report/', methods=['GET'])
def print_coverage():
    api.cov.stop()
    api.cov.save()
    api.cov.html_report()
    return jsonify({
        'status': 'success',
        'message': 'creating report!'
    })
