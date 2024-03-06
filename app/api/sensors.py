from flask import Blueprint, jsonify, request
import logging
from threading import Thread
#from app.utils.rpi import Sensors
import datetime
#from app.utils.rpi import record_sensor_data
from datetime import datetime, timedelta
from app.recorded_data.tricorder import record_sensor_data

def register_sensors_routes(api_bp: Blueprint) -> None:

    def run_manual_sensor_background(csv_file_path, duration_seconds, hertz):
        '''Wrapper function to run sensor in a background thread.'''
        record_sensor_data(csv_file_path, duration_seconds)

    @api_bp.route('/sensors', methods=['GET'])
    def get_sensor() -> jsonify:
        try:
            sensor_id = request.args.get('sensor_id', type=int)
            time_stop = request.args.get('time_stop', type=int)
            hertz = request.args.get('hertz', type=int)

            #sensor = Sensors(sensor_id)
            csv_file_path = './sensor_data_' + datetime.now().strftime('%Y-%m-%dT%H:%M') + '.csv'
            run_manual_sensor_background(csv_file_path, time_stop, hertz)
            # thread = Thread(target=run_manual_sensor_background,
            #                 args=(sensor_id, time_stop, hertz))
            # thread.start()

            logging.info(f'Sensor data collection initiated: {request.args}')
            return jsonify({"message": "Sensor run initiated"}), 202

        except ValueError as e:
            logging.error(f"Error processing request: {e}")
            return jsonify({"error": str(e)}), 400
