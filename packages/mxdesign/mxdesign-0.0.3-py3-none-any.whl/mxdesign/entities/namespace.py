"""Namespace"""
import re

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, CheckConstraint, column
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship, object_session

from mxdesign.entities.base import Base
from mxdesign.entities.variable import Variable

name_pattern = re.compile(r'[_A-Za-z][_A-Za-z0-9]*')


class Namespace(Base):
    """Namespace"""
    __tablename__ = 'namespace'

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('namespace.id'), nullable=True)
    name = Column(String(64), nullable=False)

    experiment = relationship('Experiment', back_populates='_namespace')
    parent = relationship('Namespace', remote_side=[id], backref='children')
    variables = relationship('Variable', back_populates='namespace', cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('experiment_id', 'parent_id', 'name'),
        CheckConstraint(column('name').regexp_match('^[_A-Za-z][_A-Za-z0-9]*$')),
    )

    def __getitem__(self, item):
        session = object_session(self)
        try:
            result = session.query(Variable) \
                .filter(Variable.namespace_id == self.id) \
                .filter(Variable.name == item) \
                .one()
        except NoResultFound as ex:
            result = Variable(namespace_id=self.id, name=item)
            session.add(result)
            session.commit()
        return result

    def __repr__(self):
        return 'Namespace(id={}, name={})'.format(
            self.id, self.name
        )
