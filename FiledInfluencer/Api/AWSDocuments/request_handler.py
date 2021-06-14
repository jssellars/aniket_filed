import json
import os
from datetime import datetime, timezone

import humps
from flask_restful import reqparse
from typing import Dict, Union
from werkzeug.datastructures import FileStorage

from FiledInfluencer.Api.AWSDocuments.aws_dataclass import DocumentDetails
from FiledInfluencer.Api.AWSDocuments.aws_utils import AwsUtils
from FiledInfluencer.Api.AWSDocuments.models import Documents
from FiledInfluencer.Api.AWSDocuments.schemas import DocumentsResponse
from FiledInfluencer.Api.startup import session_scope


class DocumentParser:
    @staticmethod
    def get_parser() -> reqparse.RequestParser:
        """
        Parse the get request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "key",
            type=str,
            required=True,
        )
        return parser

    @staticmethod
    def post_parser() -> reqparse.RequestParser:
        """
        Parse the post request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "documents",
            type=FileStorage,
            required=True,
            location='files',
            action='append'
        )
        parser.add_argument(
            "campaign_name",
            type=str,
            required=True,
        )
        parser.add_argument(
            "campaign_id",
            type=int,
            required=True,
        )
        parser.add_argument(
            "is_contract",
            type=bool,
            required=True,
        )
        return parser

    @staticmethod
    def delete_parser() -> reqparse.RequestParser:
        """
        Parse the delete request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "key",
            type=str,
            required=True,
        )
        return parser


class DocumentHandler:
    @staticmethod
    def max_document_size(document: FileStorage) -> bool:
        """
        Checks if the size of the document does not exceed max file size ( 20 MB )
        @param document: Document we need to find size of
        @return: True if file size is within limit
        """
        document.seek(0, os.SEEK_END)
        document_length = document.tell()
        if document_length > 20 * 1024 * 1024:
            return False
        return True

    @staticmethod
    def convert_to_json(documents: Documents) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """

        pydantic_document = DocumentsResponse.from_orm(documents)
        # Datetime is not JSON serializable
        json_document = pydantic_document.json()
        return humps.camelize(json.loads(json_document))

    @staticmethod
    def populate_model(document_data: DocumentDetails) -> Documents:
        """
        This is used to Populate the Document object
        @param document_data: All the data needed for creating Documents object
        @return: Document object
        """
        documents = Documents(
            Name=document_data.document_name,
            Extension=document_data.document_content_type,
            Location=document_data.location,
            IsContract=document_data.is_contract,
            CreatedById=1,  # Todo: dynamic data using jwt token
            CreatedAt=datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + "Z",
            CreatedByFirstName="Ahmad Danish",  # Todo: dynamic data using jwt token
            CreatedByLastName="Khan",  # Todo: dynamic data using jwt token
            CampaignId=document_data.campaign_id,
        )
        return documents

    @classmethod
    def write_to_db(cls, document_data: DocumentDetails) -> Dict[str, str]:
        """
        This will save the DocumentDetails data into the database
        @param document_data: All the data needed for saving in the database
        @return: Saved Document in JSON Format
        """
        value = cls.populate_model(document_data)
        with session_scope() as session:
            session.add(value)
        return cls.convert_to_json(value)

    @staticmethod
    def extract_document_details(document: FileStorage, request_data: Dict) -> DocumentDetails:
        """
        This Function will extract all the details for the file and will also create a unique key location to store to
        S3 disk.

        @param request_data: A dictionary that has all the request data
        @param document: FileStorage is passed to extract information of document
        @return: dataclass of DocumentDetails
        """

        document.seek(0)
        content = document.read()
        name = document.filename
        name_list = name.split(".")
        document_name = ".".join(name_list[:-1])
        document_extn = name_list[-1]
        campaign = request_data["campaign_name"]

        document_details = DocumentDetails(
            document_content=content,
            document_name=document_name,
            document_content_type=document.content_type,
            document_extn=document_extn,
            location=f"{campaign}/{document_name}_{str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))}.{document_extn}",
            is_contract=request_data["is_contract"],
            campaign_id=request_data["campaign_id"],
        )
        return document_details

    @classmethod
    def upload_document(cls, request_data: Dict) -> Union[Dict[str, str], bool]:
        """
        This Function makes sure to upload the document to S3 and to save the information to the database

        @param request_data: A dictionary that has all the request data
        @return: Dictionary of saved data in Database
        """
        aws = AwsUtils()
        document = request_data["documents"][0]
        document_details = cls.extract_document_details(document, request_data)
        uploaded_data = aws.upload_to_s3(document_details, acl="private")
        # Todo: Authenticate
        if uploaded_data:
            return cls.write_to_db(document_details)
        return False

    @classmethod
    def download_document(cls, key: str) -> Dict[str, Union[str, bool]]:
        """
        This Function makes sure to get downloadable url of the document in S3 disk
        @param key: location of the document in S3
        @return: Dictionary containing downloadable url
        """
        aws = AwsUtils()
        result = {"url": aws.download_from_s3(key)}
        return result

    @classmethod
    def delete_document(cls, key: str) -> bool:
        """
        This Function makes sure to delete the document from the S3 Disk
        also delete record of the file from database

        @param key: location of the document in S3
        @return: True
        """
        aws = AwsUtils()
        result = aws.delete_from_s3(key)
        if result:
            with session_scope() as session:
                session.query(Documents).filter(Documents.Location == key).delete()
            return True
        else:
            return False
