class ModelMixin(object):

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }