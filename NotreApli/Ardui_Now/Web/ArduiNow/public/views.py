from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory
from flask.templating import render_template
from flask_security.decorators import roles_required, login_required,current_user

bp_public = Blueprint('public',__name__, static_folder='../static')

@bp_public.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('capteur_bp.principale'))
    else:
        return render_template('home.html')


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])

@bp_public.route('/contact')
def contact():
    return render_template('contact.html')

@bp_public.route('/mentions')
def mentions():
    return render_template('mentions.html')

@bp_public.route('/plan')
def plan():
    return render_template('plan.html')

@bp_public.route('/login')
def login():
    return render_template('login.html')
