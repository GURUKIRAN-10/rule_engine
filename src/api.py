from flask import Flask, request, jsonify, render_template
from evaluator import Evaluator
from node import Node
from database import get_session, Rule

app = Flask(__name__)
evaluator = Evaluator()

VALID_ATTRIBUTES = {"age", "department", "salary", "experience"}

def validate_user_data(user_data):
    for attribute in user_data.keys():
        if attribute not in VALID_ATTRIBUTES:
            raise ValueError(f"Invalid attribute: '{attribute}'. Valid attributes are {VALID_ATTRIBUTES}.")

def dict_to_node(data):
    if data['node_type'] == 'operator':
        return Node(node_type=data['node_type'],
                    value=data['value'],
                    left=dict_to_node(data['left']),
                    right=dict_to_node(data['right']))
    else:
        return Node(node_type=data['node_type'], value=data['value'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate_rule():
    try:
        data = request.get_json()
        if not data or 'rule_ast' not in data or 'user_data' not in data:
            return jsonify({"error": "Invalid input: 'rule_ast' and 'user_data' are required."}), 400

        user_data = data['user_data']
        validate_user_data(user_data)

        rule_ast = data['rule_ast']
        rule_node = dict_to_node(rule_ast)

        result = evaluator.evaluate(rule_node, user_data)

        return jsonify({'result': result})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except KeyError as ke:
        return jsonify({"error": f"Missing key: {str(ke)}."}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred while evaluating the rule: {str(e)}"}), 500

@app.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()
        if not data or 'rule_string' not in data:
            return jsonify({"error": "Invalid input: 'rule_string' is required."}), 400

        rule_string = data['rule_string']
        session = get_session()
        
        if not rule_string:
            return jsonify({"error": "Rule string cannot be empty."}), 400

        new_rule = Rule(rule_string=rule_string)
        session.add(new_rule)
        session.commit()

        return jsonify({"message": "Rule created successfully", "rule_id": new_rule.id}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred while creating the rule: {str(e)}"}), 500

@app.route('/modify_rule/<int:rule_id>', methods=['PUT'])
def modify_rule_api(rule_id):
    try:
        data = request.get_json()
        session = get_session()

        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            return jsonify({"error": "Rule not found."}), 404

        if 'new_value' in data:
            new_rule_string = data['new_value']
            if not new_rule_string:
                return jsonify({"error": "New rule string cannot be empty."}), 400

            rule.rule_string = new_rule_string  

        session.commit()

        return jsonify({'message': 'Rule modified successfully', 'modified_rule': rule.rule_string})

    except Exception as e:
        return jsonify({"error": f"An error occurred while modifying the rule: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
