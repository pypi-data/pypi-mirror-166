"""Trial"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship, object_session

from mxdesign.entities.value import Value
from mxdesign.entities.base import Base


class Trial(Base):
    """Trial"""
    __tablename__ = 'trial'

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)

    experiment = relationship('Experiment', back_populates='trials')  # type: 'Experiment'
    values = relationship('Value', back_populates='trial', cascade='all, delete-orphan')  # type: 'Value'

    def set(self, key, value, namespace=None, **kwargs):
        """Sets a variable.

        Parameters
        ----------
        key: str
        value: typing.Any
        namespace: Namespace
        Returns
        -------
        value: Value
        """
        if namespace is None:
            namespace = self.experiment.namespace
        var = namespace[key]
        # create or update the variable
        return var(value, trial_id=self.id, **kwargs)

    def get(self, key, namespace=None, **kwargs):
        """Gets a variable.

        Parameters
        ----------
        key: str
        namespace: Namespace
        Returns
        -------
        value: Value
        """
        if namespace is None:
            namespace = self.experiment.namespace
        var = namespace[key]  # type: 'Variable'
        session = object_session(self)
        query = session.query(Value) \
            .filter(Value.trial_id == self.id) \
            .filter(Value.variable_id == var.id)
        try:
            values = query \
                .filter(Value.step.is_(None)) \
                .one()
        except (NoResultFound, MultipleResultsFound) as ex:
            values = query \
                .filter(Value.step.isnot(None)) \
                .all()
        return values

    def __repr__(self):
        return 'Trial(id={})'.format(
            self.id,
        )
