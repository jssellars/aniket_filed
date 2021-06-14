from io import BytesIO
from typing import Union

import boto3
import botocore

from FiledInfluencer.Api.AWSDocuments.aws_dataclass import DocumentDetails


class AwsUtils:
    AWS_REGION_NAME = "eu-west-1"
    AWS_ACCESS_KEY_ID = "AKIAQYAGGBZNXAKLJSAT"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_S3_BUCKET_NAME = "bucket-influencer-service-danish"

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=AwsUtils.AWS_REGION_NAME,
            aws_access_key_id=AwsUtils.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AwsUtils.AWS_SECRET_ACCESS_KEY,
        )

    def upload_to_s3(self, document_details: DocumentDetails, acl: str = "private") -> bool:
        """
        This Function tries to upload the document to the S3 Disk.

        @param document_details: This will contain all the details for the document to be uploaded
        @param acl: Permission Type
        @return: True
        """

        if not document_details:
            return False

        try:
            self.s3.put_object(
                Body=BytesIO(document_details.document_content),
                Bucket=AwsUtils.AWS_S3_BUCKET_NAME,
                Key=document_details.location,
                ACL=acl,
            )
            return True

        except botocore.exceptions.ClientError as e:
            return False

    def download_from_s3(self, key: str) -> Union[str, bool]:
        """
        This Function tries to download the document from the S3 Disk.

        @param key: This is the location where the document is stored in AWS S3 bucket
        @return: downloadable URL for the document
        """

        try:
            document_url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': AwsUtils.AWS_S3_BUCKET_NAME, 'Key': key},
                ExpiresIn=300)
            return document_url
        except botocore.exceptions.ClientError as e:
            return False

    def delete_from_s3(self, key: str) -> bool:
        """
        This Function tries to delete the document from the S3 Disk.

        @param key: This is the location where the document is stored in AWS S3 bucket
        @return: True
        """

        try:
            self.s3.delete_object(Bucket=AwsUtils.AWS_S3_BUCKET_NAME, Key=key)
            return True
        except botocore.exceptions.ClientError as e:
            return False
