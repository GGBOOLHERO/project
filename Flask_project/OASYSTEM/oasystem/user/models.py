from oasystem import db


class Base(db.Model):
    __abstract__ = True  # 将Base改成抽象类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 保存数据
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 修改操作
    def update(self):
        db.session.commit()

    # 删除
    def delete(self):
        db.session.delete(self)
        db.session.commit()


# ----------------------------职位模型类和员工模型类是一对多关系---------------------


# 职位模型类
class Position(Base):
    __tablename__ = 'position'  # 指定生成数据库表格的名称
    name = db.Column(db.String(32))  # 职位名称
    level = db.Column(db.Integer)  # 职级  例如 1,2,3
    # 设置关系属性，不会在数据库中生成相应的字段，只是用于方便查询。
    # 第一个参数:Person 关联的模型类名称
    # 第二个参数:backref='position' 反向链接，
    # persons 属性名称任意。一般要见名知意。
    persons = db.relationship('Person', backref='position')
    # 部门和职位外键
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))


# 员工模型类
class Person(Base):
    __tablename__ = 'person'
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(32), nullable=True)
    gender = db.Column(db.String(32), nullable=True, default='男')  # 设置默认值
    age = db.Column(db.Integer, nullable=True)
    jobnum = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    picture = db.Column(db.String(64), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    score = db.Column(db.Float, nullable=True)
    # 使用外键进行关联。
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    attendances = db.relationship('Attendance', backref='person')


# ------------------- 职位和权限是多对多的关系-----------------------
# 例如 部长职位 和 权限
# 人事部部长  新闻权限,考勤权限
# 研发部部长 新闻权限，考勤权限

permission_position = db.Table(
    'permission_position',  # 表格名称
    db.Column('position_id', db.Integer, db.ForeignKey('position.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Permission(Base):
    __tablename__ = 'permission'
    name = db.Column(db.String(32))  # 权限名称
    desc = db.Column(db.String(128))  # 权限描述

    # 设置关系属性
    positions = db.relationship(
        'Position',
        backref='permissions',
        secondary=permission_position  # 关联中间表格
    )


# --------------------------- 部门和职位一对多关系-------------------------------
class Department(Base):
    __tablename__ = 'department'
    name = db.Column(db.String(32))  # 部门名称
    desc = db.Column(db.Text)  # 描述
    # 部门和职位之间的查询关系
    positions = db.relationship('Position', backref='dept')


# 新闻模型类
class News(Base):
    __tablename__ = 'news'
    title = db.Column(db.String(64))
    author = db.Column(db.String(32))
    ntime = db.Column(db.Date)
    content = db.Column(db.Text)
    picture = db.Column(db.String(128), nullable=True)


# 考勤模型类
class Attendance(Base):
    __tablename__ = 'attendance'
    reason = db.Column(db.Text)  # 请假原因
    atype = db.Column(db.String(32))  # 考勤类型
    adate = db.Column(db.Float)  # 请假天数
    start_time = db.Column(db.Date)  # 请假开始时间
    end_time = db.Column(db.Date)  # 请假结束时间
    astauts = db.Column(db.String(32), default='申请中')  # 假条状态
    examine = db.Column(db.String(32), nullable=True, default='')  # 审核人， 可以是上级审核，也可以是考勤组审核
    # 设置和职员的关系
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

