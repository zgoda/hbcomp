from flask import render_template

from hbapp.profile import profile_bp
from hbapp.models import User


@profile_bp.route('/<int:user_id>', endpoint='details')
def public_details(user_id):
    user = User.query.get_or_404(user_id)
    ctx = {
        'user': user,
    }
    return render_template('profile/details.html', **ctx)
