# sqlalchemy-django-query

![](https://github.com/Shiphero/shbin/actions/workflows/pytest.yml/badge.svg)
![](https://github.com/Shiphero/shbin/actions/workflows/black.yml/badge.svg)


A module that implements a more Django like interface for SQLAlchemy
(currently < 1.4) query objects. 
It's still API compatible with the regular one but extends it with Djangoisms.


## Example

```python

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

class Blog(Base):
    name = Column(String)
    entries = relationship('Entry', backref='blog')

class Entry(Base):
    blog_id = Column(Integer, ForeignKey('blog.id'))
    pub_date = Column(Date)
    headline = Column(String)
    body = Column(String)


engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

# session with our class
session = Session(engine, query_cls=DjangoQuery)
session.query(Blog).filter_by(name__exact='blog1').one()
session.query(Blog).filter_by(name__contains='blog').all()
session.query(Entry).filter_by(pub_date__year=2011).one()
session.query(Blog).filter_by(entries__headline__exact='b2 headline 2').one()
```