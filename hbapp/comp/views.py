from flask import render_template, flash, redirect, url_for
from flask_babelex import gettext

from ..models import Competition
from ..comp import comp_bp
from ..comp.forms import CompetitionForm


@comp_bp.route('/create', methods=['POST', 'GET'])
def create():
    form = CompetitionForm()
    if form.validate_on_submit():
        comp = form.save()
        flash(gettext('Competition %(name)s has been created', name=comp.title), category='success')
        return redirect(url_for('comp.details', comp_id=comp.id))
    ctx = dict(form=form)
    return render_template('comp/form.html', **ctx)


@comp_bp.route('/<int:comp_id>')
def details(comp_id):
    ctx = dict(comp=Competition.query.get(comp_id))
    return render_template('comp/details.html', **ctx)
