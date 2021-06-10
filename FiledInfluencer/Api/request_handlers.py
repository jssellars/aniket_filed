import json
import os
from datetime import datetime, timezone

import humps
from flask_restful import reqparse
from typing import Dict, List, Union
from werkzeug.datastructures import FileStorage

from FiledInfluencer.Api.aws_utils import AwsUtils
from FiledInfluencer.Api.db_query import InfluencerProfileQuery
from FiledInfluencer.Api.influencer_dataclass import DocumentDetails
from FiledInfluencer.Api.influencer_enum import AccountTypeEnum
from FiledInfluencer.Api.models import EmailTemplates, Influencers, Documents
from FiledInfluencer.Api.schemas import EmailTemplateResponse, InfluencersResponse, DocumentsResponse
from FiledInfluencer.Api.startup import session_scope


class InfluencerProfilesHandler:
    @staticmethod
    def convert_to_json(influencer: Influencers) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """
        details = json.loads(influencer.Details)

        pydantic_influencer = InfluencersResponse(
            Id=influencer.Id,
            Name=influencer.Name,
            Biography=influencer.Biography,
            Engagement=influencer.Engagement,
            ProfilePicture=details["profile_pic_url"],
            CategoryName=details["category_name"],
            AccountType=influencer.AccountType,
            IsVerified=influencer.IsVerified,
            Followers=influencer.Followers,
            MinEngagementPerPost=influencer.MinEngagementPerPost,
            MaxEngagementPerPost=influencer.MaxEngagementPerPost,
            Email=details.get('email_id'),
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(
            cls,
            name: str,
            last_influencer_id: int,
            engagement_rate: Dict,
            page_size: int,
            get_total_count: bool,
            engagement_per_post: Dict,
            account_type: int,
            is_verified: bool,
            followers: Dict,
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:

        # last_influencer_id was already sent in previous request
        last_influencer_id += 1
        global account_type_enum1, account_type_enum2, EngagementPerPost_filters

        Followers_filters = (
            Influencers.Followers >= followers["min_count"],
            Influencers.Followers <= followers["max_count"],
        )

        if engagement_per_post is not None:
            EngagementPerPost_filters = (
                Influencers.MinEngagementPerPost >= engagement_per_post["min_count"],
                Influencers.MaxEngagementPerPost <= engagement_per_post["max_count"],
            )

        Engagement_filters = (
            Influencers.Engagement >= engagement_rate["min_count"],
            Influencers.Engagement <= engagement_rate["max_count"],
        )

        if account_type is not None:
            if account_type == AccountTypeEnum.BUSINESS.value:
                account_type_enum1 = "Business"
                account_type_enum2 = "Business, Professional"

            elif account_type == AccountTypeEnum.PROFESSIONAL.value:
                account_type_enum1 = "Professional"
                account_type_enum2 = "Business, Professional"

            elif account_type == AccountTypeEnum.PERSONAL.value:
                account_type_enum1 = "Personal"
                account_type_enum2 = "Personal"

        # Initializing session to execute query
        query = InfluencerProfileQuery()

        # for infinite scrolling
        # offset queries are inefficient
        if get_total_count:
            results = query.get_total_count_query()

        elif name and engagement_per_post and is_verified and account_type is not None:
            results = query.get_name_engagementperpost_isverified_accountype_query(
                name,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post and account_type is not None:
            results = query.get_name_engagementperpost_accountype_query(
                name,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post and is_verified is not None:
            results = query.get_name_engagementperpost_isverified_query(
                name,
                EngagementPerPost_filters,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and is_verified and account_type is not None:
            results = query.get_name_isverified_accountype_query(
                name,
                is_verified,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and engagement_per_post and account_type is not None:
            results = query.get_isverified_engagementperpost_accountype_query(
                is_verified,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif engagement_per_post and account_type is not None:
            results = query.get_engagementperpost_accountype_query(
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and account_type is not None:
            results = query.get_name_accounttype_query(
                name,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post:
            results = query.get_name_engagementperpost_query(
                name, EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif engagement_per_post and is_verified is not None:
            results = query.get_engagementperpost_isverified_query(
                EngagementPerPost_filters,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and account_type is not None:
            results = query.get_isverified_accountype_query(
                is_verified,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and name is not None:
            results = query.get_isverified_name_query(
                is_verified, name, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif engagement_per_post:
            results = query.get_engagementperpost_query(
                EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif name:
            results = query.get_name_query(name, Followers_filters, last_influencer_id, page_size, Engagement_filters)

        elif account_type is not None:
            results = query.get_accounttype_query(
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified:
            results = query.get_isverified_query(
                is_verified, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        else:
            results = query.get_default_query(Followers_filters, last_influencer_id, page_size, Engagement_filters)

        if isinstance(results, dict):
            return results
        return [cls.convert_to_json(result) for result in results]


class EmailTemplateHandler:
    blank_field_error_msg = "This field cannot be left blank"

    @classmethod
    def email_template_parser(cls):
        """
        Parser the fields coming from the request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            type=str,
            required=False,
        )
        parser.add_argument(
            "subject",
            type=str,
            required=False,
        )
        parser.add_argument(
            "body",
            type=str,
            required=False,
        )

        parser.add_argument("campaign", type=int, required=True, help=cls.blank_field_error_msg)
        return parser

    @staticmethod
    def convert_to_json(email_template: EmailTemplates) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """

        pydantic_email_template = EmailTemplateResponse.from_orm(email_template)
        # Datetime is not JSON serializable
        json_email_template = pydantic_email_template.json()
        return humps.camelize(json.loads(json_email_template))

    @classmethod
    def get_email_templates(cls, user_id) -> List[Dict[str, str]]:
        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            results = session.query(EmailTemplates).filter(EmailTemplates.CreatedById == user_id)

        return [cls.convert_to_json(result) for result in results]

    @classmethod
    def populate_model(cls, data):
        email_template = EmailTemplates(
            Name=data["name"],
            Subject=data["subject"],
            Body=data["body"],
            CampaignId=data["campaign"],
            CreatedById=data["created_by"],
            CreatedAt=datetime.utcnow(),
        )
        return email_template

    @classmethod
    def write_to_db(cls, data):
        value = cls.populate_model(data)
        with session_scope() as session:
            session.add(value)
        value = cls.convert_to_json(value)
        return value


class DocumentHandler:

    @classmethod
    def max_document_size(cls, document: FileStorage) -> bool:
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

    @classmethod
    def document_parser(cls) -> reqparse.RequestParser:
        """
        Parser the fields coming from the request
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
    def convert_to_json(documents: Documents) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """

        pydantic_document = DocumentsResponse.from_orm(documents)
        # Datetime is not JSON serializable
        json_document = pydantic_document.json()
        return humps.camelize(json.loads(json_document))

    @classmethod
    def populate_model(cls, document_data: DocumentDetails) -> Documents:
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
        This Function makes sure to delete the document from the S3 Disk and also delete record of the file from database
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
