from datetime import datetime
from typing import Optional, List

from facebook_business.adobjects.user import User
from facebook_business.exceptions import FacebookRequestError

from Core.Web.BusinessOwnerRepository.Models.BusinessOwnerModel import BusinessOwnerModel
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


class BusinessOwnerRepository:
    def __init__(self, facebook_config, session):
        self.__session = session()
        self.__facebook_config = facebook_config

    def get_permanent_token(self, business_owner_facebook_id: str) -> Optional[str]:
        results = (
            self.__session.query(BusinessOwnerModel)
            .filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id)
            .all()
        )

        tokens = [result.Token for result in results]

        self.__session.close()
        return self.__get_valid_token(tokens)

    def get_permanent_token_by_page_id(self, business_owner_facebook_id: str, page_id: str) -> None:
        results = (
            self.__session.query(BusinessOwnerModel)
            .filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id)
            .filter(BusinessOwnerModel.PageId == page_id)
            .all()
        )

        tokens = [result.Token for result in results]

        self.__session.close()

        return tokens[0] if tokens else None

    def modify_user_token(
        self,
        business_owner_facebook_id: str,
        new_permanent_business_owner_facebook_token: str,
        page_id: str,
    ) -> None:
        try:
            user_details = (
                self.__session.query(BusinessOwnerModel)
                .filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id)
                .filter(BusinessOwnerModel.PageId == page_id)
                .one()
            )
            user_details.Token = new_permanent_business_owner_facebook_token
            user_details.UpdatedAt = datetime.utcnow()
            self.__session.commit()
            self.__session.flush()
            self.__session.close()
        except:
            self.__session.rollback()

    def create_user_token(
        self,
        business_owner_facebook_id: str,
        name: str,
        email: str,
        token: str,
        page_id: str,
    ) -> None:
        now = datetime.utcnow()
        entry = BusinessOwnerModel(
            FacebookId=business_owner_facebook_id,
            Name=name,
            Email=email,
            Token=token,
            PageId=page_id,
            CreatedAt=now,
            UpdatedAt=now,
        )
        try:
            self.__session.add(entry)
            self.__session.commit()
            self.__session.close()
        except Exception as e:
            self.__session.rollback()
            raise e

    def user_already_exists(self, business_owner_facebook_id: str, page_id: str) -> bool:
        results = (
            self.__session.query(BusinessOwnerModel)
            .filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id)
            .filter(BusinessOwnerModel.PageId == page_id)
            .all()
        )
        if len(results):
            return True
        return False

    def business_owner_already_exists(self, business_owner_id: str) -> bool:
        return (
            len(
                self.__session.query(BusinessOwnerModel)
                .filter(BusinessOwnerModel.FacebookId == business_owner_id)
                .all()
            )
            > 0
        )

    def create_or_update_user(
        self,
        business_owner_facebook_id: str,
        name: str,
        email: str,
        token: str,
        page_id: str,
    ) -> None:
        if self.user_already_exists(business_owner_facebook_id, page_id):
            self.modify_user_token(business_owner_facebook_id, token, page_id)
        else:
            self.create_user_token(business_owner_facebook_id, name, email, token, page_id)

    def delete_permissions(self, business_owner_facebook_id: str) -> None:
        self.__session.query(BusinessOwnerModel).filter(
            BusinessOwnerModel.FacebookId == business_owner_facebook_id
        ).delete()

    def __get_valid_token(self, tokens: List[str]) -> Optional[str]:
        for token in tokens:
            try:
                GraphAPISdkBase(self.__facebook_config, token)
                User("me").api_get()
                return token
            except FacebookRequestError:
                self.__session.query(BusinessOwnerModel).filter(BusinessOwnerModel.Token == token).delete()
                self.__session.commit()
