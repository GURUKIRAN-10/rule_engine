class Evaluator:
    def evaluate(self, rule_node, user_data):
        return self._evaluate_node(rule_node, user_data)

    def _evaluate_node(self, node, user_data):
        if node.is_operand():
            return self._evaluate_operand(node.value, user_data)
        elif node.is_operator():
            left_eval = self._evaluate_node(node.left, user_data)
            right_eval = self._evaluate_node(node.right, user_data)
            return self._evaluate_operator(node.value, left_eval, right_eval)

    def _evaluate_operand(self, operand, user_data):
        try:
            var, op, value = operand.split()
            value = int(value)
            user_value = user_data.get(var)

            if user_value is None:
                raise ValueError(f"Attribute '{var}' not found in user data.")

            if op == '>':
                return user_value > value
            elif op == '<':
                return user_value < value
            elif op == '=':
                return user_value == value
            elif op == '>=':
                return user_value >= value
            elif op == '<=':
                return user_value <= value
            else:
                raise ValueError(f"Operator '{op}' is not supported.")

        except ValueError as e:
            print(f"Error evaluating operand: {e}")
            return False

    def _evaluate_operator(self, operator, left, right):
        if operator == 'AND':
            return left and right
        elif operator == 'OR':
            return left or right
        else:
            raise ValueError(f"Operator '{operator}' is not supported.")
