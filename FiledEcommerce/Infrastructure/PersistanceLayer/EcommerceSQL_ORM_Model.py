from contextlib import contextmanager
from typing import ContextManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Integer, String, BIGINT, NVARCHAR, Column, MetaData
from sqlalchemy.ext.automap import automap_base
import pymssql
from FiledEcommerce.Api.startup import fixtures
import pyodbc
import os


engine = create_engine('mssql+pymssql://filed_admin:dvserv3#rathena@stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com:1433/Dev3.Filed.ProductCatalogs2',echo=True)
metadata = MetaData()

#PreLoaded Models

filed_business_owners = Table('FiledBusinessOwners', metadata, autoload=True, autoload_with=engine)
external_platforms = Table('ExternalPlatforms', metadata, autoload=True, autoload_with=engine)

#columns for FiledBusinessOwners
cols = filed_business_owners.c

#Columns for ExternalPlatforms
ext_plat_cols = external_platforms.c


