from flask import Flask, jsonify
from flask_cors import CORS
from command_modules.korniszon_module.leaderboard import Leaderboard


app = Flask(__name__)
CORS(app)

leaderboard_obj = Leaderboard()
leaderboard_obj.load_leaderboard()
leaderboard_list = leaderboard_obj.leaderboard
# print(leaderboard_list)


@app.route('/ranking', methods=['GET'])
def get_ranking():
    return jsonify(leaderboard_list)


if __name__ == '__main__':
    app.run(debug=True)