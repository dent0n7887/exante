from models import BaseModel
from sqlalchemy import INT, Column, JSON, Index


class DataModel(BaseModel):
    __tablename__ = 'tbl_data'
    id = Column('id', INT, primary_key=True, autoincrement=True)
    js = Column('js', JSON)
    sum = Column('sum', INT)
    __table_args__ = (
        Index('sum_index', sum),
    )

    def as_dict(self):
        return {
            'js': str(self.js)
        }