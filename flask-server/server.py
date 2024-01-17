from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from logic import ConnectFourBoard, Play

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the ConnectFourBoard
w, h = 7, 6
connect = ConnectFourBoard(w, h)

@app.route("/")
def index():
    global connect
    connect = ConnectFourBoard(w, h)
    return render_template("index.html")

@socketio.on("positionClicked")
def handle_position_clicked(data):
    col = data.get("col")
    print(f"Received column: {col}")

   
    if connect.gameover():
        # Game over, emit an event to restart the game
        socketio.emit("gameOver", {"winner": connect.winner}, namespace="/")

    else:
        # Robot's move
        Play.RobotTurn(connect.state)
        socketio.emit("playerMove", {"col": connect.lastmove[0], "player": 2}, namespace="/")

        if connect.gameover():
            # Game over, emit an event to restart the game
            socketio.emit("gameOver", {"winner": connect.winner}, namespace="/")


if __name__ == "__main__":
    socketio.run(app, debug=True)






