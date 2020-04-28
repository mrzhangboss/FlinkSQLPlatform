# -*- coding:utf-8 -*-
import json
import re
import attr
import logzero
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql.sqltypes import TypeDecorator
from typing import Optional, List, Type, Union
from re import _pattern_type
from fsqlfly.db_helper import ResourceName, ResourceTemplate, ResourceVersion, Connection, SchemaEvent
from fsqlfly.common import DBRes
from fsqlfly.db_helper import DBSession, DBDao, Session, SUPPORT_MODELS


class BlinkSQLType:
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'
    BYTES = 'BYTES'
    DECIMAL = 'DECIMAL'
    TINYINT = 'TINYINT'
    SMALLINT = 'SMALLINT'
    INTEGER = 'INTEGER'
    BIGINT = 'BIGINT'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    DATE = 'DATE'
    TIME = 'TIME'
    TIMESTAMP = 'TIMESTAMP'


class BlinkHiveSQLType(BlinkSQLType):
    INTERVAL = 'INTERVAL'
    ARRAY = 'ARRAY'
    MULTISET = 'MULTISET'
    MAP = 'MAP'
    RAW = 'RAW'


class BlinkTableType:
    sink = 'sink'
    source = 'source'
    both = 'both'


class DBSupportType:
    MySQL = 'MySQL'
    PostgreSQL = 'PostgreSQL'


class NameFilter:
    @classmethod
    def get_pattern(cls, s: str) -> List[Type[_pattern_type]]:
        s = s.replace('，', ',')
        patterns = [s.strip()] if ',' not in s else s.split(',')
        res = [re.compile(pattern=x + '$') for x in patterns]
        return res

    def __init__(self, include: str = '', exclude: str = ''):
        self.includes = self.get_pattern(include) if include else [re.compile(r'.*')]
        self.excludes = self.get_pattern(exclude) if exclude else []

    def __contains__(self, item: str) -> bool:
        if any(map(lambda x: x.match(item) is not None, self.includes)):
            if self.excludes and any(map(lambda x: x.match(item), self.excludes)):
                return False
            return True
        return False


@attr.s
class SchemaField:
    name: str = attr.ib()
    type: str = attr.ib()
    comment: Optional[str] = attr.ib(default=None)
    nullable: Optional[bool] = attr.ib(default=True)
    autoincrement: Optional[bool] = attr.ib(default=None)


@attr.s
class SchemaContent:
    name: str = attr.ib()
    type: str = attr.ib()
    database: Optional[str] = attr.ib(default=None)
    comment: Optional[str] = attr.ib(default=None)
    primary_key: Optional[str] = attr.ib(default=None)
    fields: List[SchemaField] = attr.ib(factory=list)
    partitionable: bool = attr.ib(default=False)


class UpdateStatus:
    def __init__(self):
        self.schema_inserted = 0
        self.schema_updated = 0
        self.name_inserted = 0
        self.name_updated = 0
        self.template_inserted = 0
        self.template_updated = 0
        self.version_inserted = 0
        self.version_updated = 0

    def update_schema(self, inserted: bool):
        self.schema_inserted += inserted
        self.schema_updated += not inserted

    def update_resource_name(self, inserted: bool):
        self.name_inserted += inserted
        self.name_updated += not inserted

    def update_template(self, inserted: bool):
        self.template_inserted += inserted
        self.template_updated += not inserted

    def update_version(self, inserted: bool):
        self.version_inserted += inserted
        self.version_updated += not inserted

    @property
    def info(self) -> str:
        return '\n'.join(['{}: {}'.format(x, getattr(self, x)) for x in dir(self) if x.endswith('ed')])


class BaseManager:
    use_comment = False
    use_primary = False
    renewable = True

    def __init__(self, connection_url: str, table_name_filter: NameFilter, db_type):
        self.connection_url = connection_url
        self.need_tables = table_name_filter
        self.db_type = db_type

    def run(self, target: Union[Connection, ResourceName, ResourceTemplate, ResourceVersion]) -> DBRes:
        if not self.renewable:
            return DBRes.api_error("{} is Not renewable".format(target.name))
        status = UpdateStatus()

        session = DBSession.get_session()
        if isinstance(target, (Connection, ResourceName)):
            if isinstance(target, ResourceVersion):
                target = target.connection
            self.update_connection(status, session, target)
        elif isinstance(target, ResourceTemplate):
            self.update_template(status, session, target.connection, target.schema_version, target.resource_name)
        elif isinstance(target, ResourceVersion):
            self.update_version(status, session, target.connection, target.schema_version, target.resource_name,
                                target.template)
        else:
            raise NotImplementedError("Not Suppport {}".format(type(target)))
        return DBRes(data=status.info)

    def update_connection(self, status: UpdateStatus, session: Session, connection: Connection):
        for content in self.update():
            schema = self.get_schema_event(schema=content, connection=connection)
            schema, i = DBDao.upsert_schema_event(schema, session=session)
            status.update_schema(i)
            self.update_resource_name(status, session, connection, schema)

    def update_resource_name(self, status: UpdateStatus, session: Session, connection: Connection, schema: SchemaEvent):
        resource_name = self.get_resource_name(connection, schema)
        resource_name, i = DBDao.upsert_resource_name(resource_name, session=session)
        status.update_resource_name(i)
        self.update_template(status, session, schema=schema, connection=connection, resource_name=resource_name)

    def update_template(self, status: UpdateStatus, session: Session, connection: Connection, schema: SchemaEvent,
                        resource_name: ResourceName):
        for template in self.get_template(schema=schema, connection=connection, resource_name=resource_name):
            template, i = DBDao.upsert_resource_template(template, session=session)
            status.update_template(i)
            self.update_version(status, session, schema=schema, connection=connection, resource_name=resource_name,
                                template=template)

    def update_version(self, status: UpdateStatus, session: Session, connection: Connection, schema: SchemaEvent,
                       resource_name: ResourceName, template: ResourceTemplate):
        version = self.get_default_version(connection, schema, resource_name, template)
        version, i = DBDao.upsert_resource_version(version, session=session)
        status.update_version(i)

    def get_schema_event(self, schema: SchemaContent, connection: Connection) -> SchemaEvent:
        return SchemaEvent(name=schema.name, info=schema.comment, database=schema.database,
                           connection_id=connection.id, comment=schema.comment, primary_key=schema.primary_key,
                           fields=json.dumps([attr.asdict(x) for x in schema.fields], ensure_ascii=False),
                           partitionable=schema.partitionable)

    def update(self) -> List[SchemaContent]:
        return list()

    def get_resource_name(self, connection: Connection, schema: SchemaEvent) -> ResourceName:
        raise NotImplementedError

    def get_template(self, connection: Connection, schema: SchemaEvent,
                     resource_name: ResourceName) -> List[ResourceTemplate]:
        raise NotImplementedError

    def get_default_version(self, connection: Connection, schema: SchemaEvent, name: ResourceName,
                            template: ResourceTemplate) -> ResourceVersion:
        raise NotImplementedError


class DatabaseManager(BaseManager):
    use_comment = True
    use_primary = True

    def _get_flink_type(self, typ: TypeDecorator) -> Optional[str]:
        from sqlalchemy.dialects.mysql.types import _StringType as M_STRING, BIT as M_BIT, TINYINT, DOUBLE as M_DOUBLE
        from sqlalchemy.dialects.postgresql import (DOUBLE_PRECISION as P_DOUBLE, BIT as P_BIT, VARCHAR, CHAR, TEXT,
                                                    JSON, BOOLEAN)
        from sqlalchemy.sql.sqltypes import (DATE, _Binary, INTEGER, SMALLINT, BIGINT, FLOAT, DECIMAL,
                                             DATETIME,
                                             TIMESTAMP, TIME)
        name = None
        types = BlinkSQLType
        if isinstance(typ, (M_STRING, VARCHAR, CHAR, TEXT, JSON)):
            name = types.STRING
        elif isinstance(typ, _Binary):
            name = types.BYTES
        elif isinstance(typ, BOOLEAN):
            name = types.BOOLEAN
        elif isinstance(typ, TINYINT):
            name = types.TINYINT
        elif isinstance(typ, SMALLINT):
            name = types.SMALLINT
        elif isinstance(typ, (P_BIT, M_BIT)):
            name = types.TINYINT
        elif isinstance(typ, INTEGER):
            name = types.INTEGER
        elif isinstance(typ, BIGINT):
            name = types.BIGINT
        elif isinstance(typ, FLOAT):
            name = types.FLOAT
        elif isinstance(typ, (M_DOUBLE, P_DOUBLE)):
            name = types.DOUBLE
        elif isinstance(typ, DECIMAL):
            name = "{}({},{})".format(types.DECIMAL, typ.precision, typ.scale)
        elif isinstance(typ, DATETIME) or isinstance(typ, TIMESTAMP):
            name = types.TIMESTAMP
        elif isinstance(typ, DATE):
            name = types.DATE
        elif isinstance(typ, TIME):
            name = types.TIME

        if name is None:
            logzero.logger.error("Not Support Current Type in DB {}".format(str(typ)))
            return None
        return name

    def update(self):
        from sqlalchemy.sql.sqltypes import INTEGER, SMALLINT, BIGINT
        engine = create_engine(self.connection_url)
        insp = inspect(engine)
        db_list = insp.get_schema_names()
        update_tables = []
        for db in db_list:
            for tb in insp.get_table_names(db):
                full_name = f'{db}.{tb}'
                if full_name in self.need_tables:
                    update_tables.append((db, tb))

        schemas = []

        for db, tb in update_tables:
            comment = insp.get_table_comment(table_name=tb, schema=db)['text'] if self.use_comment else None
            schema = SchemaContent(name=tb, database=db, comment=comment, type=self.db_type)
            columns = insp.get_columns(table_name=tb, schema=db)
            primary = insp.get_primary_keys(tb, db) if self.use_primary else None
            if primary and len(primary) == 1:
                schema.primary_key = primary[0]
                column = list(filter(lambda x: x['name'] == primary[0], columns))[0]
                if isinstance(column['type'], (INTEGER, SMALLINT, BIGINT)):
                    schema.partitionable = True

            fields = []
            for x in columns:
                field = SchemaField(name=x['name'], type=self._get_flink_type(x['type']),
                                    nullable=x['nullable'], autoincrement=x.get('autoincrement'))
                if field.type is None:
                    logzero.logger.error(
                        "Not Add Column {} in {}.{} current not support : {}".format(field.name, schema.database,
                                                                                     schema.name, str(x['type'])))
                else:
                    fields.append(field)

            fields.sort(key=lambda x: x.name)

            schema.fields.extend(fields)

            print(schema)
            schemas.append(schema)

        return schemas


class HiveManager(DatabaseManager):
    use_comment = False
    use_primary = False

    hive_types = set(list(x for x in dir(BlinkHiveSQLType) if not x.startswith('__')))

    def _get_flink_type(self, typ: TypeDecorator) -> Optional[str]:
        from sqlalchemy.sql.sqltypes import (VARCHAR, String, CHAR, BINARY)

        name = None
        types = BlinkHiveSQLType
        str_name = str(typ)

        if isinstance(typ, (VARCHAR, CHAR, String)):
            name = types.STRING
        elif isinstance(typ, BINARY):
            name = types.BYTES
        elif str_name in self.hive_types:
            name = str_name
        if name is None:
            logzero.logger.error("Not Support Current Type in DB {}".format(str(typ)))
            return None
        return name


class ElasticSearchManager(DatabaseManager):
    def _es2flink(self, typ: str) -> Optional[str]:
        types = BlinkSQLType
        if typ in ("text", "keyword"):
            return types.STRING
        elif typ == 'long':
            return types.BIGINT
        elif typ == 'integer':
            return types.INTEGER
        elif typ == 'byte':
            return types.TINYINT
        elif typ == 'short':
            return types.SMALLINT
        elif typ == 'float':
            return types.FLOAT
        elif typ == 'binary':
            return types.BYTES
        elif typ == 'boolean':
            return types.BOOLEAN
        elif typ == 'date':
            return types.DATE

    def update(self):
        assert 'elasticsearch' == self.db_type
        from elasticsearch import Elasticsearch
        es = Elasticsearch(hosts=self.connection_url)
        schemas = []
        for index in es.indices.get_alias('*'):
            if index not in self.need_tables:
                continue

            schema = SchemaContent(name=index, type=self.db_type)
            mappings = es.indices.get_mapping(index)

            fields = []
            for k, v in mappings[index]['mappings']['properties'].items():
                field = SchemaField(name=k, type=self._es2flink(v['type']),
                                    nullable=True)
                if field.type is None:
                    logzero.logger.error(
                        "Not Add Column {} in {}.{} current not support : {}".format(field.name, schema.database,
                                                                                     schema.name, str(v['type'])))
                else:
                    fields.append(field)

            fields.sort(key=lambda x: x.name)

            schema.fields.extend(fields)

            print(schema)
            schemas.append(schema)

        return schemas


class HBaseManager(DatabaseManager):
    def update(self):
        assert 'hbase' == self.db_type
        import happybase
        host, port = self.connection_url.split(':')
        connection = happybase.Connection(host, int(port), autoconnect=True)
        schemas = []
        for x in connection.tables():
            tab = x.decode()
            table = connection.table(tab)
            schema = SchemaContent(name=tab, type=self.db_type)
            fields = []
            for fm in table.families():
                fields.append(SchemaField(name=fm.decode(), type=BlinkHiveSQLType.BYTES, nullable=True))
            schema.fields.extend(fields)
            schemas.append(schema)
        return schemas


class CanalManager(BaseManager):
    renewable = False


class FileManger(BaseManager):
    renewable = False


class KafkaManger(BaseManager):
    renewable = False


SUPPORT_MANAGER = {
    'hive': HiveManager,
    'db': DatabaseManager,
    'kafka': KafkaManger,
    'hbase': HBaseManager,
    'elasticsearch': ElasticSearchManager,
    'canal': CanalManager,
    'file': FileManger
}


class ManagerHelper:
    @classmethod
    def is_support(cls, mode: str) -> bool:
        return mode == 'update'

    @classmethod
    def update(cls, model: str, pk: str):
        if model not in SUPPORT_MODELS:
            return DBRes.api_error(msg='{} not support'.format(model))
        session = DBSession.get_session()
        try:
            obj = DBDao.one(base=SUPPORT_MODELS[model], pk=int(pk), session=session)
            if isinstance(obj, Connection):
                name_filter = NameFilter(obj.include, obj.exclude)
                manager = SUPPORT_MANAGER[obj.type](obj.url, name_filter)
            elif isinstance(obj, ResourceName):
                name_filter = NameFilter(obj.get_include())
                manager = SUPPORT_MANAGER[obj.connection.type](obj.connection.url, name_filter)
            else:
                name_filter = NameFilter()
                typ = obj.connection.type
                manager = SUPPORT_MANAGER[typ](
                    obj.connection.url,
                    name_filter,
                    typ
                )

            return manager.run(obj)
        finally:
            session.close()
