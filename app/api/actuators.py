from flask import Blueprint, jsonify, request
import logging


def register_actuators_routes(api_bp: Blueprint) -> None:
    """
    Register sensor routes with the provided API blueprint.
    :param api_bp: Blueprint to register the routes with.
    """

    @api_bp.route('/actuators', methods=['GET'])
    def get_actuators() -> jsonify:
        """
        Endpoint to retrieve actuators data based on a actuators ID.
        :return: JSON response containing actuators data.
        """
        try:
            # Your code here
            actuators = request.args.get('actuator_id', type=int)
            logging.info('Function executed successfully: {request.args}')
            data = {'test': 'successful', 'actuators': request.args}
        except Exception as e:
            logging.error('Error in some_function: %s', str(e))
        if actuators is not None:
            data = {'error': 'actuator_id is required'}
        return jsonify(data)
