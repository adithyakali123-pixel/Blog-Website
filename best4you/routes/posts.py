from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import (
    get_all_posts, get_post_by_id, get_posts_by_user,
    create_post, update_post, delete_post
)

posts_bp = Blueprint('posts', __name__)

CATEGORIES = {
    'coding':    'Coding Knowledge',
    'interview': 'Interview Prep',
    'placement': 'Placement Experience',
    'tech':      'Technical Article',
}


def login_required(f):
    """Simple login decorator."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@posts_bp.route('/post/<int:post_id>')
def view_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('main.home'))
    return render_template('post_detail.html', post=post, categories=CATEGORIES)


@posts_bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        content  = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        tags     = request.form.get('tags', '').strip()

        if not title or not content or not category:
            flash('Title, content and category are required.', 'error')
            return render_template('write.html', categories=CATEGORIES)

        if category not in CATEGORIES:
            flash('Invalid category selected.', 'error')
            return render_template('write.html', categories=CATEGORIES)

        post_id = create_post(session['user_id'], title, content, category, tags)
        flash('Your post has been published! 🎉', 'success')
        return redirect(url_for('posts.view_post', post_id=post_id))

    return render_template('write.html', categories=CATEGORIES)


@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('main.home'))

    if post['user_id'] != session['user_id']:
        flash('You can only edit your own posts.', 'error')
        return redirect(url_for('posts.view_post', post_id=post_id))

    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        content  = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        tags     = request.form.get('tags', '').strip()

        if not title or not content or not category:
            flash('Title, content and category are required.', 'error')
            return render_template('edit_post.html', post=post, categories=CATEGORIES)

        update_post(post_id, title, content, category, tags)
        flash('Post updated successfully! ✅', 'success')
        return redirect(url_for('posts.view_post', post_id=post_id))

    return render_template('edit_post.html', post=post, categories=CATEGORIES)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('main.home'))

    if post['user_id'] != session['user_id']:
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('posts.view_post', post_id=post_id))

    delete_post(post_id)
    flash('Post deleted.', 'success')
    return redirect(url_for('main.home'))


@posts_bp.route('/profile')
@login_required
def profile():
    my_posts = get_posts_by_user(session['user_id'])
    return render_template('profile.html', posts=my_posts, categories=CATEGORIES)
