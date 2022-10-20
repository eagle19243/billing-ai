import globals


def get_contracts(page, offset, search_query):
    if page and offset and search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM contract_type
                       WHERE name LIKE ?;"""

        query_data = ['%'+search_query+'%']
        cursor = globals.conn.execute(sql_query, query_data)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM contract_type
                       WHERE name LIKE ?
                       LIMIT ?, ?;"""

        query_data.extend([page, offset])
        cursor = globals.conn.execute(sql_query, query_data)
        contracts = [{'contract_id': row[0], 'contract_title': row[1]} for row in cursor]
        return {'contracts': contracts, 'total_pages': count//offset}

    elif page and offset and not search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM contract_type;"""

        cursor = globals.conn.execute(sql_query)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM contract_type
                       ORDER BY name
                       LIMIT ?, ?;"""

        query_data = [page, offset]
        cursor = globals.conn.execute(sql_query, query_data)
        contracts = [{'contract_id': row[0], 'contract_title': row[1]} for row in cursor]
        return {'contracts': contracts, 'total_pages': count//offset}

    else:
        sql_query = """SELECT *
                       FROM contract_type;"""

        cursor = globals.conn.execute(sql_query)
        contracts = [{'contract_id': row[0], 'contract_title': row[1]} for row in cursor]
        return {'contracts': contracts}


def add_contract(request_data):
    sql_query = """INSERT INTO contract_type(name)
                   VALUES(?);"""
    query_data = [request_data['contract_title']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def update_contract(request_data):
    sql_query = """UPDATE contract_type
                   SET name = ?
                   WHERE id = ?;"""
    query_data = [request_data['contract_title'], request_data['contract_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def delete_contract(request_data):
    sql_query = """DELETE FROM contract_type 
                   WHERE id=?"""
    query_data = [request_data['contract_id']]
    globals.conn.execute(sql_query, query_data)

    sql_query = """DELETE FROM contract_category 
                   WHERE contract_id=?"""
    query_data = [request_data['contract_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def get_categories(contract_id, page, offset, search_query):
    if page and offset and search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause_category
                       WHERE name LIKE ?;"""

        query_data = ['%'+search_query+'%']
        cursor = globals.conn.execute(sql_query, query_data)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause_category
                       WHERE name LIKE ?
                       LIMIT ?, ?;"""

        query_data.extend([page, offset])
        cursor = globals.conn.execute(sql_query, query_data)
        contracts = [{'category_id': row[0], 'category_name': row[1]} for row in cursor]
        return {'contracts': contracts, 'total_pages': count//offset}

    elif page and offset and not search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause_category;"""

        cursor = globals.conn.execute(sql_query)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause_category
                       ORDER BY name
                       LIMIT ?, ?;"""

        query_data = [page, offset]
        cursor = globals.conn.execute(sql_query, query_data)
        contracts = [{'category_id': row[0], 'category_name': row[1]} for row in cursor]
        return {'contracts': contracts, 'total_pages': count//offset}

    else:
        sql_query = """SELECT *
                       FROM clause_category clc, contract_category cnc
                       WHERE cnc.category_id = clc.id AND cnc.contract_id = ?;"""

        query_data = [contract_id]
        cursor = globals.conn.execute(sql_query, query_data)
        categories = [{'category_id': row[4], 'category_name': row[1]} for row in cursor]
        return {'contracts': categories}


def add_category(request_data):
    sql_query = """INSERT INTO clause_category(name)
                   VALUES(?);"""
    query_data = [request_data['category_name']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def update_category(request_data):
    sql_query = """UPDATE clause_category
                   SET name = ?
                   WHERE id = ?;"""
    query_data = [request_data['category_name'], request_data['category_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def delete_category(request_data):
    sql_query = """DELETE FROM clause_category 
                   WHERE id=?"""
    query_data = [request_data['category_id']]
    globals.conn.execute(sql_query, query_data)

    sql_query = """DELETE FROM contract_category 
                   WHERE category_id=?"""
    query_data = [request_data['category_id']]
    globals.conn.execute(sql_query, query_data)

    sql_query = """DELETE FROM clause_category_variation 
                   WHERE category_id=?"""
    query_data = [request_data['category_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def add_category_to_contract(request_data):
    for contract_id in request_data['contract_ids']:
        sql_query = """SELECT *
                       FROM contract_category
                       WHERE contract_id=? and category_id=?;"""
        query_data = [contract_id, request_data['category_id']]
        cursor = globals.conn.execute(sql_query, query_data)
        if len(cursor.fetchall()):
            continue

        sql_query = """INSERT INTO contract_category(contract_id, category_id)
                       VALUES(?, ?);"""
        query_data = [contract_id, request_data['category_id']]
        globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def get_variations(category_id, page, offset, search_query):
    if category_id:
        sql_query = """SELECT clv.id, clv.name
                       FROM clause_category_variation ccv, clause_variation clv
                       WHERE ccv.category_id = ? and ccv.variation_id = clv.id"""

        query_data = [category_id]
        cursor = globals.conn.execute(sql_query, query_data)
        variations = [{'variation_id': row[0], 'variation_name': row[1]} for row in cursor]
        return {'variations': variations}

    if page and offset and search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause_variation
                       WHERE name LIKE ?;"""

        query_data = ['%'+search_query+'%']
        cursor = globals.conn.execute(sql_query, query_data)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause_variation
                       WHERE name LIKE ?
                       LIMIT ?, ?;"""

        query_data.extend([page, offset])
        cursor = globals.conn.execute(sql_query, query_data)
        variations = [{'variation_id': row[0], 'variation_name': row[1]} for row in cursor]
        return {'variations': variations, 'total_pages': count//offset}

    elif page and offset and not search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause_variation;"""

        cursor = globals.conn.execute(sql_query)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause_variation
                       ORDER BY name
                       LIMIT ?, ?;"""

        query_data = [page, offset]
        cursor = globals.conn.execute(sql_query, query_data)
        variations = [{'variation_id': row[0], 'variation_name': row[1]} for row in cursor]
        return {'variations': variations, 'total_pages': count//offset}
    else:
        return {'variations': []}


def add_variation(request_data):
    sql_query = """INSERT INTO clause_variation(name)
                   VALUES(?);"""
    query_data = [request_data['variation_name']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def update_variation(request_data):
    sql_query = """UPDATE clause_variation
                   SET name = ?
                   WHERE id = ?;"""
    query_data = [request_data['variation_name'], request_data['variation_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def delete_variation(request_data):
    sql_query = """DELETE FROM clause_variation 
                   WHERE id=?"""
    query_data = [request_data['variation_id']]
    globals.conn.execute(sql_query, query_data)

    sql_query = """DELETE FROM clause_category_variation 
                   WHERE variation_id=?"""
    query_data = [request_data['variation_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def get_clauses(contract_id, category_id, variation_id, tag):
    if tag is not None and variation_id is not None:
        sql_query = """SELECT cl.id, cl.definition, cl.tag
                       FROM contract_type cnt, contract_category cnc, clause_category clc, clause_category_variation ccv, clause cl
                       WHERE cnt.id = ? and cnt.id = cnc.contract_id and clc.id = cnc.category_id and clc.id = ccv.category_id and ccv.category_id = ? and cl.id = ccv.clause_id and ccv.variation_id = ? and cl.tag = ?;"""
        query_data = [contract_id, category_id, variation_id, tag]

    elif tag is not None:
        sql_query = """SELECT cl.id, cl.definition, cl.tag
                       FROM contract_type cnt, contract_category cnc, clause_category clc, clause_category_variation ccv, clause cl
                       WHERE cnt.id = ? and cnt.id = cnc.contract_id and clc.id = cnc.category_id and clc.id = ccv.category_id and ccv.category_id = ? and cl.id = ccv.clause_id and cl.tag = ?;"""
        query_data = [contract_id, category_id, tag]

    elif variation_id is not None:
        sql_query = """SELECT cl.id, cl.definition, cl.tag
                       FROM contract_type cnt, contract_category cnc, clause_category clc, clause_category_variation ccv, clause cl
                       WHERE cnt.id = ? and cnt.id = cnc.contract_id and clc.id = cnc.category_id and clc.id = ccv.category_id and ccv.category_id = ? and cl.id = ccv.clause_id and ccv.variation_id = ?;"""
        query_data = [contract_id, category_id, variation_id]

    elif contract_id is not None and category_id is not None:
        sql_query = """SELECT cl.id, cl.definition, cl.tag
                       FROM contract_type cnt, contract_category cnc, clause_category clc, clause_category_variation ccv, clause cl
                       WHERE cnt.id = ? and cnt.id = cnc.contract_id and clc.id = cnc.category_id and clc.id = ccv.category_id and ccv.category_id = ? and cl.id = ccv.clause_id;"""
        query_data = [contract_id, category_id]

    cursor = globals.conn.execute(sql_query, query_data)
    clauses = [
        {'clause_id': row[0], 'clause_definition': row[1], 'clause_tag': row[2]} for
        row in cursor]
    return {'clauses': clauses}


def get_clauses_web(page, offset, search_query):
    if page and offset and search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause
                       WHERE definition LIKE ?;"""

        query_data = ['%'+search_query+'%']
        cursor = globals.conn.execute(sql_query, query_data)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause
                       WHERE definition LIKE ?
                       LIMIT ?, ?;"""

        query_data.extend([page, offset])
        cursor = globals.conn.execute(sql_query, query_data)
        clauses = [{'clause_id': row[0], 'clause_definition': row[1], 'clause_tag': row[2]} for row in cursor]
        return {'clauses': clauses, 'total_pages': count//offset}

    elif page and offset and not search_query:
        page = int(page)
        offset = int(offset)
        page *= offset
        sql_query = """SELECT COUNT(*)
                       FROM clause;"""

        cursor = globals.conn.execute(sql_query)
        count = [row[0] for row in cursor][0]

        sql_query = """SELECT *
                       FROM clause
                       ORDER BY id
                       LIMIT ?, ?;"""

        query_data = [page, offset]
        cursor = globals.conn.execute(sql_query, query_data)
        clauses = [{'clause_id': row[0], 'clause_definition': row[1], 'clause_tag': row[2]} for row in cursor]
        return {'clauses': clauses, 'total_pages': count//offset}
    else:
        return {'clauses': []}


def add_clause(clause_definition, clause_tag):
    sql_query = """INSERT INTO clause(definition, cleaned_definition, tag)
                   VALUES(?, ?, ?);"""
    query_data = [clause_definition, ' '.join(preprocess(clause_definition)), clause_tag]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()
    return {'message': 'Clause added successfully'}


def update_clause(request_data):
    sql_query = """UPDATE clause
                   SET definition = ?,
                       cleaned_definition = ?,
                       tag = ?
                   WHERE id = ?;"""
    query_data = [request_data['clause_definition'], ' '.join(preprocess(request_data['clause_definition'])),
                  request_data['clause_tag'], request_data['clause_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()
    return {'message': 'Clause successfully updated'}


def delete_clause(request_data):
    sql_query = """DELETE FROM clause 
                   WHERE id=?"""
    query_data = [request_data['clause_id']]
    globals.conn.execute(sql_query, query_data)

    sql_query = """DELETE FROM clause_category_variation 
                   WHERE clause_id=?"""
    query_data = [request_data['clause_id']]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()


def add_clause_to_category(request_data):
    clause_id = request_data.get('clause_id')
    category_id = request_data.get('category_id')
    variation_id = request_data.get('variation_id')
    if clause_id is None or category_id is None or variation_id is None:
        return {'message': 'Missing data'}

    sql_query = """SELECT *
                   FROM clause_category_variation
                   WHERE clause_id=? and category_id=? and variation_id=?;"""

    query_data = [clause_id, category_id, variation_id]
    cursor = globals.conn.execute(sql_query, query_data)
    if len(cursor.fetchall()):
        return {'message': 'Clause already present in the category'}

    sql_query = """INSERT INTO clause_category_variation(clause_id, category_id, variation_id)
                       VALUES(?, ?, ?);"""
    query_data = [clause_id, category_id, variation_id]
    globals.conn.execute(sql_query, query_data)
    globals.conn.commit()
    return {'message': 'Clause successfully added'}


def get_stats():
    sql_query = """SELECT COUNT(*)
                   FROM contract_type;"""
    cursor = globals.conn.execute(sql_query)
    contract_count = [row[0] for row in cursor][0]

    sql_query = """SELECT COUNT(*)
                   FROM clause_category;"""
    cursor = globals.conn.execute(sql_query)
    categories_count = [row[0] for row in cursor][0]

    sql_query = """SELECT COUNT(*)
                   FROM clause_variation;"""
    cursor = globals.conn.execute(sql_query)
    variations_count = [row[0] for row in cursor][0]

    sql_query = """SELECT COUNT(*)
                   FROM clause;"""
    cursor = globals.conn.execute(sql_query)
    clauses_count = [row[0] for row in cursor][0]

    return {'contracts_count': contract_count, 'categories_count': categories_count,
            'variations_count': variations_count, 'clauses_count': clauses_count, 'tags_count': 5}


def get_tags(category_id, variation_id):
    if variation_id:
        sql_query = """SELECT DISTINCT	tag
                       FROM clause_category clc, clause_category_variation ccv, clause cl
                       WHERE ccv.category_id = ? and cl.id = ccv.clause_id and ccv.variation_id = ?"""
        query_data = [category_id, variation_id]
    else:
        sql_query = """SELECT DISTINCT	tag
                       FROM clause_category clc, clause_category_variation ccv, clause cl
                       WHERE ccv.category_id = ? and cl.id = ccv.clause_id"""
        query_data = [category_id]

    cursor = globals.conn.execute(sql_query, query_data)
    tags = [row[0] for row in cursor if row[0] is not None]
    if '' in tags:
        tags.remove('')
    return {'tags': tags}


def get_contract_tags(contract_id):
    sql_query = """SELECT c.id, c.name, cl.tag
                   FROM category c, contract_category cc, clause_category_subcategory ccs, clause cl
                   WHERE cc.category_id = c.id and cc.contract_id = ? and ccs.category_id = c.id and cl.id = ccs.clause_id;"""

    query_data = [contract_id]
    cursor = globals.conn.execute(sql_query, query_data)

    response_data = {}
    for row in cursor:
        if row[0] not in response_data:
            response_data[row[0]] = {'category_id': row[0], 'category_name': row[1], 'tags': set()}
        else:
            response_data[row[0]]['tags'].add(row[2])

    tags = []
    for key in response_data:
        item = response_data[key]
        item['tags'] = list(item['tags'])
        item['tags'] = [tag for tag in item['tags'] if tag is not None]
        if '' in item['tags']:
            item['tags'].remove('')
        tags.append(item)
    return {'category_tags': tags}


def preprocess(text):
    text = text.lower()
    text = globals.punctuation_re.sub('', text.strip())
    text = text.replace('\n', ' ')
    return text
