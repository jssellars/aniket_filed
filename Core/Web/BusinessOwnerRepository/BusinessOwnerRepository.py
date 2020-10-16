import typing
from datetime import datetime

from Core.Web.BusinessOwnerRepository.Models.BusinessOwnerModel import BusinessOwnerModel


class BusinessOwnerRepository:

    def __init__(self, session):
        self.__session = session()

    def get_permanent_token(self, business_owner_facebook_id: typing.AnyStr = None) -> typing.AnyStr:
        results = self.__session.query(BusinessOwnerModel).filter(
            BusinessOwnerModel.FacebookId == business_owner_facebook_id).all()

        token = [result.Token for result in results]

        self.__session.close()

        if token:
            return token[0]

    def get_permanent_token_by_page_id(self,
                                       business_owner_facebook_id: typing.AnyStr = None,
                                       page_id: typing.AnyStr = None) -> typing.AnyStr:
        results = (
            self.__session.query(BusinessOwnerModel)
                .filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id)
                .filter(BusinessOwnerModel.PageId == page_id)
                .all()
        )

        token = [result.Token for result in results]

        self.__session.close()

        if token:
            return token[0]

    def modify_user_token(self,
                          business_owner_facebook_id: typing.AnyStr = None,
                          new_permanent_business_owner_facebook_token: typing.AnyStr = None,
                          page_id: typing.AnyStr = None) -> typing.NoReturn:
        try:
            user_details = self.__session.query(BusinessOwnerModel). \
                filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id). \
                filter(BusinessOwnerModel.PageId == page_id). \
                one()
            user_details.Token = new_permanent_business_owner_facebook_token
            user_details.UpdatedAt = datetime.utcnow()
            self.__session.commit()
            self.__session.flush()
            self.__session.close()
        except:
            self.__session.rollback()

    def create_user_token(self,
                          business_owner_facebook_id: typing.AnyStr = None,
                          name: typing.AnyStr = None,
                          email: typing.AnyStr = None,
                          token: typing.AnyStr = None,
                          page_id: typing.AnyStr = None) -> typing.NoReturn:
        now = datetime.utcnow()
        entry = BusinessOwnerModel(
            FacebookId=business_owner_facebook_id,
            Name=name,
            Email=email,
            Token=token,
            PageId=page_id,
            CreatedAt=now,
            UpdatedAt=now
        )
        try:
            self.__session.add(entry)
            self.__session.commit()
            self.__session.close()
        except Exception as e:
            self.__session.rollback()
            raise e

    def user_already_exists(self,
                            business_owner_facebook_id: typing.AnyStr = None,
                            page_id: typing.AnyStr = None) -> bool:
        results = self.__session.query(BusinessOwnerModel). \
            filter(BusinessOwnerModel.FacebookId == business_owner_facebook_id). \
            filter(BusinessOwnerModel.PageId == page_id). \
            all()
        if len(results):
            return True
        return False

    def create_or_update_user(self,
                              business_owner_facebook_id: typing.AnyStr = None,
                              name: typing.AnyStr = None,
                              email: typing.AnyStr = None,
                              token: typing.AnyStr = None,
                              page_id: typing.AnyStr = None) -> typing.NoReturn:
        if self.user_already_exists(business_owner_facebook_id, page_id):
            self.modify_user_token(business_owner_facebook_id, token, page_id)
        else:
            self.create_user_token(business_owner_facebook_id, name, email, token, page_id)

    def delete_permissions(self, business_owner_facebook_id: typing.AnyStr) -> typing.NoReturn:
        try:
            self.__session.query(BusinessOwnerModel).filter(
                BusinessOwnerModel.FacebookId == business_owner_facebook_id).delete()
        except Exception as e:
            raise e
