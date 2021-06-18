from contextlib import contextmanager
from typing import ContextManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, alias
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Integer, String, BIGINT, NVARCHAR, Column, MetaData
from sqlalchemy.ext.automap import automap_base
import pymssql
from FiledEcommerce.Api.startup import fixtures
import pyodbc
import os


engine = create_engine('mssql+pymssql://filed_admin:dvserv3#rathena@stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com:1433/Dev3.Filed.ProductCatalogs2')
metadata = MetaData()

#PreLoaded Models

filed_business_owners = Table('FiledBusinessOwners', metadata, autoload=True, autoload_with=engine)
external_platforms = Table('ExternalPlatforms', metadata, autoload=True, autoload_with=engine)
filed_product_cat = Table('FiledProductCatalogs', metadata, autoload=True, autoload_with=engine)
platforms = Table('Platforms', metadata, autoload=True, autoload_with=engine)
filed_products = Table('FiledProducts', metadata, autoload=True, autoload_with=engine)
filed_variants = Table('FiledVariants', metadata, autoload=True, autoload_with=engine)
filed_product_conns = Table('FiledProductConnections', metadata, autoload=True, autoload_with=engine)
filed_variant_conns = Table('FiledVariantConnections', metadata, autoload=True, autoload_with=engine)
custom_properties = Table('CustomProperties', metadata, autoload=True, autoload_with=engine)
fpc_permissions = Table('FiledProductCatalogPermissions', metadata, autoload=True, autoload_with=engine)
filed_sets = Table('FiledSets', metadata, autoload=True, autoload_with=engine)
filed_set_variants = Table('FiledSetVariants', metadata, autoload=True, autoload_with=engine)

#columns for FiledBusinessOwners
cols = filed_business_owners.c
#Columns for ExternalPlatforms
ext_plat_cols = external_platforms.c
#Columns for FiledProductCatalogs
fpc = filed_product_cat.c
#columns for Platforms
pl = platforms.c
#columns for FiledProducts
fp_cols = filed_products.c
#columns for FiledProductConnections
fp_conns_cols = filed_product_conns.c
#columns for FiledVariants
fv_cols = filed_variants.c



''' Please remove above code after code cleanup is completed '''
from contextlib import contextmanager
from typing import ContextManager

from Core import fixtures, logging_config
from FiledEcommerce.Api import settings
from sqlalchemy.orm import Session

config = settings.core.get_settings(settings, 'dev3')
fixtures = fixtures.Fixtures(config)

logging_config.init(config)
logger = logging_config.get_logger(__name__)
logger.info("Configuration details", extra=logging_config.app_config_as_log_dict(config))


@contextmanager
def session_scope() -> ContextManager[Session]:
    """
    Context manager to gracefully handle sessions

    Copied from documentation
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    session = fixtures.sql_db_session()

    try:
        yield session
        # The objects within the session are expired upon commit,
        # set expire_on_commit to false to keep using them
        session.expire_on_commit = False
        session.commit()

    # intentional wide scope to rollback session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

