import string
from flask import Flask, jsonify, request
from flask_cors import CORS
from command_modules.korniszon_module.leaderboard import Leaderboard
from sql_database import Database
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
import os


app = Flask(__name__)
CORS(app)

load_dotenv()

database = Database()
leaderboard_obj = Leaderboard(database)
# print(leaderboard_list)

# http://127.0.0.1:8000/ranking?page=0&per_page=10&sort_by=user&order=DESC
@app.route('/ranking', methods=['GET'])
def get_ranking():
    # Get pagination parameters from request, default page is 0
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', "score", type=str)
    order = request.args.get('order', "DESC", type=str)
    # filter = request.args.get('filter', "score", type=str)

    # Calculate offset based on 0-indexed page
    offset = page * per_page

    # Load paginated data
    leaderboard_list = leaderboard_obj.load_leaderboard(
        offset=offset, 
        limit=per_page,
        sort_by=sort_by,
        order=order
        )

    # Get total count without loading all data
    total_query = f"""
        SELECT COUNT(*) as total 
        FROM {os.getenv('MAIN_TABLE_NAME')}_with_position
    """

    # in case database is empty
    total_items = database.fetch(total_query, fetch_one=True) or 0
    
    # Calculate total pages (0-based)
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

