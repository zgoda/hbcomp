from hbapp.profile import profile_bp


@profile_bp.route('/<int:profile_id>', endpoint='details')
def details(profile_id):
    return 'details'
