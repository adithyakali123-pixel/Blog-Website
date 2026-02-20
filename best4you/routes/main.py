from flask import Blueprint, render_template, request
from database import get_all_posts

main_bp = Blueprint('main', __name__)

CATEGORIES = {
    'coding':    'Coding Knowledge',
    'interview': 'Interview Prep',
    'placement': 'Placement Experience',
    'tech':      'Technical Article',
}


@main_bp.route('/')
def home():
    category = request.args.get('category', '')
    posts = get_all_posts(category if category in CATEGORIES else None)
    recent = get_all_posts()[:4]
    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        categories=CATEGORIES,
        active_cat=category,
    )
