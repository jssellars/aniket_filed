import typing
from datetime import datetime

from Core.Web.BusinessOwnerRepository.Models.BusinessOwnerModel import BusinessOwnerModel


class BusinessOwnerRepository:

    def __init__(self, session):
        self.__session = session()

    def get_permanent_token(self, business_owner_facebook_id: typing.AnyStr = None) -> typing.AnyStr:
        results = self.__session.query(BusinessOwnerModel).filter(
            BusinessOwnerModel.facebook_id == business_owner_facebook_id).all()

        token = [result.token for result in results]

        self.__session.close()

        if token:
            return token[0]

    def get_permanent_token_by_page_id(self,
                                       business_owner_facebook_id: typing.AnyStr = None,
                                       page_id: typing.AnyStr = None) -> typing.AnyStr:
        results = self.__session.query(BusinessOwnerModel). \
            filter(BusinessOwnerModel.facebook_id == business_owner_facebook_id). \
            filter(BusinessOwnerModel.page_id == page_id). \
            all()

        token = [result.token for result in results]

        self.__session.close()

        if token:
            return token[0]

    def modify_user_token(self,
                          business_owner_facebook_id: typing.AnyStr = None,
                          new_permanent_business_owner_facebook_token: typing.AnyStr = None,
                          page_id: typing.AnyStr = None) -> typing.NoReturn:
        try:
            user_details = self.__session.query(BusinessOwnerModel). \
                filter(BusinessOwnerModel.facebook_id == business_owner_facebook_id). \
                filter(BusinessOwnerModel.page_id == page_id). \
                one()
            user_details.token = new_permanent_business_owner_facebook_token
            user_details.updated_at = datetime.utcnow()
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
        entry = BusinessOwnerModel(facebook_id=business_owner_facebook_id,
                                   name=name,
                                   email=email,
                                   token=token,
                                   page_id=page_id,
                                   created_at=now,
                                   updated_at=now)
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
            filter(BusinessOwnerModel.facebook_id == business_owner_facebook_id). \
            filter(BusinessOwnerModel.page_id == page_id). \
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
                BusinessOwnerModel.facebook_id == business_owner_facebook_id).delete()
        except Exception as e:
            raise e
