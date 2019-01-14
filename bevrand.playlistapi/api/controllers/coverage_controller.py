from flask import Blueprint, jsonify
import coverage


coverage_blueprint = Blueprint('coverage', __name__, )
COV = None


@coverage_blueprint.route('/report/', methods=['GET'])
def print_coverage():
    global COV
    COV.stop()
    COV.save()
    COV.html_report()
    return jsonify({
        'status': 'success',
        'message': 'creating report!'
    })


@coverage_blueprint.route('/start/', methods=['GET'])
def start_coverage():
    cov = coverage.Coverage(config_file=".coveragerc")
    cov.start()
    global COV
    COV = cov
    print(COV)
    return jsonify({
        'status': 'success',
        'message': 'starting coverage report!'
    })
