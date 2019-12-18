from flask_sqlalchemy import Model as BaseModel


class ModelMixin(object):

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }


class Model(BaseModel, ModelMixin):
    pass
