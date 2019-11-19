from app import db


class InventoryModel(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    invname = db.Column(db.String(55), nullable=False)
    invtype = db.Column(db.String(55), nullable=False)
    bp = db.Column(db.Float, nullable=False)
    sp = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rp = db.Column(db.Integer, nullable=False)
    sales = db.relationship('SalesModel', backref='inventory', lazy=True)

    @classmethod
    def update_stock(cls, inv_id, qty):
        case_inventory = InventoryModel.query.filter_by(id=inv_id).first()

        if case_inventory:
            if case_inventory.stock >= qty > 0:
                case_inventory.stock = case_inventory.stock - qty
                db.session.commit()
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def update_inventory(cls, id, invname=None, invtype=None, bp=None, sp=None, stock=None, rp=None):
        case_inventory = InventoryModel.query.filter_by(id=id).first()

        editable_records = [invname, invtype, bp, sp, stock, rp]

        if case_inventory:
            if invname:
                case_inventory.invname = invname
            if invtype:
                case_inventory.invtype = invtype
            if bp:
                case_inventory.bp = bp
            if sp:
                case_inventory.sp = sp
            if stock:
                case_inventory.stock = stock
            if rp:
                case_inventory.rp = rp

            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def getTypeCount(cls, name):
        record = InventoryModel.query.filter_by(invtype=name).count()
        return record
