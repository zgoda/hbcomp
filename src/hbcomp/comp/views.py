from flask import render_template, flash, redirect, url_for
from flask_babel import gettext

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


@comp_bp.route('/<int:comp_id>', methods=['POST', 'GET'])
def details(comp_id):
    comp = Competition.query.get_or_404(comp_id)
    form = CompetitionForm()
    if form.validate_on_submit():
        comp = form.save(obj=comp)
        flash(gettext('Competition %(name)s has been changed', name=comp.title), category='success')
    form = CompetitionForm(obj=comp)
    ctx = dict(comp=comp, form=form)
    return render_template('comp/details.html', **ctx)
