from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import create_user, get_user_by_username, verify_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm', '').strip()

        # Validation
        if not all([name, username, email, password, confirm]):
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html')

        # Save to DB
        success, result = create_user(name, username, email, password)
        if success:
            session['user_id']   = result
            session['user_name'] = name
            session['username']  = username
            flash(f'Welcome, {name.split()[0]}! Your account has been created. 🎉', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(result, 'error')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please enter username and password.', 'error')
            return render_template('login.html')

        user = get_user_by_username(username)
        if user and verify_password(password, user['password'], user['salt']):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            session['username']  = user['username']
            flash(f'Welcome back, {user["name"].split()[0]}! 👋', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
