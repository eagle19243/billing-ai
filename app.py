from flask import Flask, request, render_template
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/get_contracts', methods=['GET'])
def get_contracts_api():
    try:
        page = request.args.get('page')
        offset = request.args.get('offset')
        search_query = request.args.get('search_query')
        return utils.get_contracts(page, offset, search_query)
    except Exception:
        return {'contracts': []}


@app.route('/add_contract', methods=['POST'])
def add_contract_api():
    try:
        request_data = request.get_json()
        utils.add_contract(request_data)
        return {'message': 'Contract successfully added'}
    except Exception:
        return {'message': 'Could not add contract'}


@app.route('/update_contract', methods=['PUT'])
def update_contract_api():
    try:
        request_data = request.get_json()
        utils.update_contract(request_data)
        return {'message': 'Contract successfully updated'}
    except Exception:
        return {'message': 'Could not update contract'}


@app.route('/delete_contract', methods=['DELETE'])
def delete_contract_api():
    try:
        request_data = request.get_json()
        utils.delete_contract(request_data)
        return {'message': 'Contract successfully deleted'}
    except Exception:
        return {'message': 'Could not delete contract'}


@app.route('/get_categories', methods=['GET'])
def get_categories_api():
    try:
        contract_id = request.args.get('contract_id')
        page = request.args.get('page')
        offset = request.args.get('offset')
        search_query = request.args.get('search_query')
        return utils.get_categories(contract_id, page, offset, search_query)
    except Exception:
        return {'contracts': []}


@app.route('/add_category', methods=['POST'])
def add_category_api():
    try:
        request_data = request.get_json()
        utils.add_category(request_data)
        return {'message': 'Category successfully added'}
    except Exception:
        return {'message': 'Could not add category'}


@app.route('/update_category', methods=['PUT'])
def update_category_api():
    try:
        request_data = request.get_json()
        utils.update_category(request_data)
        return {'message': 'Category successfully updated'}
    except Exception:
        return {'message': 'Could not update category'}


@app.route('/delete_category', methods=['DELETE'])
def delete_category_api():
    try:
        request_data = request.get_json()
        utils.delete_category(request_data)
        return {'message': 'Category successfully deleted'}
    except Exception:
        return {'message': 'Could not delete category'}


@app.route('/add_category_to_contract', methods=['POST'])
def add_category_to_contract_api():
    try:
        request_data = request.get_json()
        utils.add_category_to_contract(request_data)
        return {'message': 'Category successfully added'}
    except Exception:
        return {'message': 'Could not add category'}


@app.route('/get_variations', methods=['GET'])
def get_variations_api():
    try:
        page = request.args.get('page')
        offset = request.args.get('offset')
        search_query = request.args.get('search_query')
        category_id = request.args.get('category_id')
        return utils.get_variations(category_id, page, offset, search_query)
    except Exception:
        return {'variations': []}


@app.route('/add_variation', methods=['POST'])
def add_variation_api():
    try:
        request_data = request.get_json()
        utils.add_variation(request_data)
        return {'message': 'Variation successfully added'}
    except Exception:
        return {'message': 'Could not add variation'}


@app.route('/update_variation', methods=['PUT'])
def update_variation_api():
    try:
        request_data = request.get_json()
        utils.update_variation(request_data)
        return {'message': 'Variation successfully updated'}
    except Exception:
        return {'message': 'Could not update variation'}


@app.route('/delete_variation', methods=['DELETE'])
def delete_variation_api():
    try:
        request_data = request.get_json()
        utils.delete_variation(request_data)
        return {'message': 'Variation successfully deleted'}
    except Exception:
        return {'message': 'Could not delete variation'}


@app.route('/get_clauses', methods=['GET'])
def get_clauses_api():
    try:
        contract_id = request.args.get('contract_id')
        category_id = request.args.get('category_id')
        variation_id = request.args.get('variation_id')
        tag = request.args.get('tag')
        page = request.args.get('page')
        offset = request.args.get('offset')
        search_query = request.args.get('search_query')

        if page or offset or search_query:
            return utils.get_clauses_web(page, offset, search_query)

        elif tag is not None:
            tag = tag.strip()
        return utils.get_clauses(contract_id, category_id, variation_id, tag)
    except Exception:
        return {'clauses': []}


@app.route('/get_tags', methods=['GET'])
def get_tags_api():
    try:
        category_id = request.args.get('category_id')
        variation_id = request.args.get('variation_id')
        return utils.get_tags(category_id, variation_id)
    except Exception:
        return {'tags': []}


@app.route('/add_clause', methods=['POST'])
def add_clause_api():
    try:
        request_data = request.get_json()
        clause_definition = request_data.get('clause_definition')
        clause_tag = request_data.get('clause_tag')
        if clause_definition is None or clause_tag is None:
            return {'message': 'Missing data'}
        return utils.add_clause(clause_definition, clause_tag)
    except Exception:
        return {'message': 'Could not add clause'}


@app.route('/update_clause', methods=['POST'])
def update_clause_api():
    try:
        request_data = request.get_json()
        utils.update_clause(request_data)
        return {'message': 'Clause successfully updated'}
    except Exception:
        return {'message': 'Could not update clause'}


@app.route('/delete_clause', methods=['DELETE'])
def delete_clause_api():
    try:
        request_data = request.get_json()
        utils.delete_clause(request_data)
        return {'message': 'Clause successfully deleted'}
    except Exception:
        return {'message': 'Could not delete clause'}


@app.route('/add_clause_to_category', methods=['POST'])
def add_clause_to_category_api():
    try:
        request_data = request.get_json()
        return utils.add_clause_to_category(request_data)
    except Exception:
        return {'message': 'Could not add clause'}


@app.route('/get_stats', methods=['GET'])
def get_stats_api():
    try:
        return utils.get_stats()
    except Exception:
        return {'message': 'Could not get stats'}


if __name__ == "__main__":
    staging = False
    if staging:
        app.run(host='0.0.0.0', port=5002, debug=True)
    else:
        app.run(host='0.0.0.0', port=5001)
