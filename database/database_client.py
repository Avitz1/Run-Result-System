from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, JSON
from sqlalchemy.orm import sessionmaker
from database.config import DATABASE_URL


class Database:
    def __init__(self, database_url=DATABASE_URL):
        self.engine = create_engine(database_url)
        self.metadata = MetaData()
        self.run_results = Table(
            'run_results', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('tool', String, nullable=False, index=True),
            Column('result', JSON, nullable=False, index=True)
        )
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def store_run_result(self, tool_name, result_data):
        self.session.execute(self.run_results.insert().values(tool=tool_name, result=result_data))
        self.session.commit()

    def fetch_tools(self):
        query = self.session.query(self.run_results.c.tool).distinct()
        return [row[0] for row in query.all()]

    def fetch_results(self, tool_name, user_filter=None, tag_filter=None):
        query = self.session.query(self.run_results)
        query = query.filter(self.run_results.c.tool == tool_name)
        if user_filter:
            query = query.filter(self.run_results.c.result['user'].astext == user_filter)
        if tag_filter:
            query = query.filter(self.run_results.c.result['tag'].astext.like(f"%{tag_filter}%"))
        return query.all()
