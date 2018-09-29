# coding=utf-8


from datetime import datetime
from app import db


class Express(db.Model):
    """快递表"""
    __tablename__ = 'express'
    # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    upload_time = db.Column(db.DateTime, comment=u'上传时间', default=datetime.now())
    express_order = db.Column(db.String(60), unique=True, index=True, comment=u'快递单号', default="")
    carriers = db.Column(db.String(60), comment=u'承运商', default="")
    user_label = db.Column(db.String(60), index=True, comment=u'用户标签', default="")
    serial_id = db.Column(db.String(100),index=True,comment=u'查询批次号')
    blong_user = db.Column(db.String(100),index=True,comment=u'上传用户')
    took_time = db.Column(db.DateTime, index=True, comment=u'揽收时间')
    confirm_time = db.Column(db.DateTime, index=True, comment=u'签收时间')
    last_time = db.Column(db.DateTime, comment=u'最后更新时间')
    state = db.Column(db.String(30), comment=u'快递状态', default="")
    results = db.Column(db.String(255), comment=u'查询结果', default="")

    url = db.Column(db.String(255), comment=u'查询url', default='')
    item_tag = db.Column(db.String(255), comment=u'查询标识', default="")
    update_time = db.Column(db.DateTime, index=True, comment=u'信息更新时间')

    def __repr(self):
        return 'Express:{}'.format(self.express_order)


# if __name__ == '__main__':
#     db.create_all()
