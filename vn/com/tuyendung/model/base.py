from vn.com.tuyendung import db


class BaseMixin(object):
    def create_or_update(self):
        db.session.add(self)
        db.session.commit()
