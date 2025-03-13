from flask import Flask, jsonify, request
from flask_cors import CORS
from command_modules.korniszon_module.leaderboard import Leaderboard
from sql_database import Database
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

database = Database()
leaderboard_obj = Leaderboard(database)
# print(leaderboard_list)


@app.route('/ranking', methods=['GET'])
def get_ranking():

    # Get pagination parameters from request
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    offset = (page - 1) * per_page

    # Load paginated data
    leaderboard_list = leaderboard_obj.load_leaderboard(offset=offset, per_page=per_page)

    # Get total count without loading all data
    total_query = f"""
        SELECT COUNT(*) as total 
        FROM {os.getenv('MAIN_TABLE_NAME')}_with_position
    """

    # in case database is empty
    total_items = database.fetch(total_query, fetch_one=True) or 0
    
    total_pages = (total_items + per_page - 1) // per_page

    return jsonify({
        'pagination': {
            'current_page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages
        },
        'items': leaderboard_list
    })



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

