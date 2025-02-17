from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, JSON, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database.config import DATABASE_URL


class DatabaseConnectionError(Exception):
    pass


class Database:
    def __init__(self, database_url=DATABASE_URL):
        try:
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
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f"Error connecting to database: {e}")

    def store_run_result(self, tool_name, result_data):
        try:
            self.session.execute(self.run_results
                                 .insert()
                                 .values(tool=tool_name, result=result_data))
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseConnectionError(f"Error storing run result: {e}")

    def fetch_tools(self):
        try:
            query = (self.session
                     .query(self.run_results.c.tool)
                     .distinct())
            return [row[0] for row in query.all()]
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f"Error fetching tools: {e}")

    def fetch_results(self, tool_name, filters=None):
        try:
            query = (self.session
                     .query(self.run_results)
                     .filter(self.run_results.c.tool == tool_name))
            if filters:
                for field, value in filters.items():
                    query = query.filter(self.run_results.c.result[field].ilike(f"%{value}%"))
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f"Error fetching results: {e}")

    def fetch_schema(self, tool_name):
        try:
            query = (select(self.run_results)
                     .where(self.run_results.c.tool == tool_name)
                     .limit(1))
            result = self.session.execute(query).fetchone()
            if result and result.result:
                return result.result
            return []
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f"Error fetching schema: {e}")