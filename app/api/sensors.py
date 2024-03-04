from flask import Blueprint, jsonify, request
import logging
from threading import Thread
from app.utils.rpi import Sensors


def register_sensors_routes(api_bp: Blueprint) -> None:


    def run_manual_sensor_background(sensor, time_stop, hertz):
        '''Wrapper function to run sensor in a background thread.'''
        sensor.manual_run_sensor(time_stop=time_stop, hertz=hertz)

    
    @api_bp.route('/sensors', methods=['GET'])
    def get_sensor() -> jsonify:
        try:
            sensor_id = request.args.get('sensor_id', type=int)
            time_stop = request.args.get('time_stop', type=int)
            hertz = request.args.get('hertz', type=int)

            sensor = Sensors(sensor_id)

            thread = Thread(target=run_manual_sensor_background,
                            args=(sensor, time_stop, hertz))
            thread.start()

            logging.info(f'Sensor data collection initiated: {request.args}')
            return jsonify({"message": "Sensor run initiated"}), 202

        except ValueError as e:
            logging.error(f"Error processing request: {e}")
            return jsonify({"error": str(e)}), 400

