"""
Admin Routes

Handles user management for admin users.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.routes.auth import admin_required
from app.services.user_service import UserService
from app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/users')
@admin_required
def manage_users():
    """Admin page for managing users."""
    user_service = UserService()
    users = user_service.get_all_users()
    return render_template('admin.html', users=users)


@bp.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    """Add a new user."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        flash('Username and password are required', 'error')
        return redirect(url_for('admin.manage_users'))
    
    # Check if user already exists
    user_service = UserService()
    existing_user = user_service.get_user_by_username(username)
    
    if existing_user:
        flash(f'User "{username}" already exists', 'error')
        return redirect(url_for('admin.manage_users'))
    
    # Create new user
    new_user = User(username)
    new_user.set_password(password)
    
    if user_service.add_user(new_user):
        flash(f'User "{username}" added successfully', 'success')
    else:
        flash('Error adding user', 'error')
    
    return redirect(url_for('admin.manage_users'))


@bp.route('/users/edit', methods=['POST'])
@admin_required
def edit_user():
    """Edit an existing user."""
    old_username = request.form.get('old_username', '').strip()
    new_username = request.form.get('new_username', '').strip()
    new_password = request.form.get('new_password', '')
    
    if not old_username or not new_username:
        flash('Username is required', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user_service = UserService()
    user = user_service.get_user_by_username(old_username)
    
    if not user:
        flash(f'User "{old_username}" not found', 'error')
        return redirect(url_for('admin.manage_users'))
    
    # Update user
    user.username = new_username
    if new_password:  # Only update password if provided
        user.set_password(new_password)
    
    if user_service.update_user(old_username, user):
        flash(f'User updated successfully', 'success')
    else:
        flash('Error updating user', 'error')
    
    return redirect(url_for('admin.manage_users'))


@bp.route('/users/delete', methods=['POST'])
@admin_required
def delete_user():
    """Delete a user."""
    username = request.form.get('username', '').strip()
    
    if not username:
        flash('Username is required', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user_service = UserService()
    
    if user_service.delete_user(username):
        flash(f'User "{username}" deleted successfully', 'success')
    else:
        flash('Error deleting user', 'error')
    
    return redirect(url_for('admin.manage_users'))


@bp.route('/users/reset-password', methods=['POST'])
@admin_required
def reset_password():
    """Reset (blank) a user's password."""
    username = request.form.get('username', '').strip()
    
    if not username:
        flash('Username is required', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user_service = UserService()
    user = user_service.get_user_by_username(username)
    
    if not user:
        flash(f'User "{username}" not found', 'error')
        return redirect(url_for('admin.manage_users'))
    
    # Set blank password (empty string)
    user.set_password('')
    
    if user_service.update_user(username, user):
        flash(f'Password reset for user "{username}"', 'success')
    else:
        flash('Error resetting password', 'error')
    
    return redirect(url_for('admin.manage_users'))
