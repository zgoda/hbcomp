class ModelMixin(object):

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, unicode(self).encode('utf-8'))
