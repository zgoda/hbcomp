from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required

from hbapp.profile import profile_bp
from hbapp.profile.forms import ProfileForm
from hbapp.models import User, db


@profile_bp.route('/<int:user_id>', endpoint='details', methods=['POST', 'GET'])
@login_required
def details(user_id):
    user = User.query.get_or_404(user_id)
    form = ProfileForm()
    if form.validate_on_submit():
        form.populate_obj(obj=user)
        db.session.add(user)
        db.session.commit()
        flash('Your profile data has been saved', category='success')
        return redirect(url_for('profile.details', user_id=user_id))
    form = ProfileForm(obj=user)
    ctx = {
        'user': user,
        'form': form,
    }
    return render_template('profile/details.html', **ctx)
