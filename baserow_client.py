import requests
from env import URL, EMAIL, PASSWORD

BR_URL = URL + "/api/"

class BaserowClient:
    
    __token__ = None
    __token_status__ = None
    __get_headers__ = None
    __post_patch_headers__ = None
    
    def __init__(self):
        token_response = self.token_auth(EMAIL, PASSWORD)
        self.__token_status__ = token_response.status_code
        if self.__token_status__ == 200:
            self.__token__ = token_response.json()["token"]
            self.__get_headers__ = {"Authorization": f"JWT {self.__token__}"}
            self.__post_patch_headers__ = {**self.__get_headers__, "Content-Type": "application/json"}


    def is_token_valid(self):
        return self.__token_status__ == 200

    def get_settings(self):
        return requests.get(BR_URL + "settings/")

    """
    def create_user(self, name: str, email: str, password: str, language: str = "en", authenticate: bool = False, group_invitation_token: str = None, template_id: int = 0):
        user = {
            "name": name,
            "email": email,
            "password": password,
            "language": language,
            "authenticate": authenticate,
            "group_invitation_token": group_invitation_token,
            "template_id": template_id
        }
        return requests.post(BR_URL + "user/", json=user)


    def update_account(self, first_name: str, language: str):
        updated_account = {
            "first_name": first_name,
            "language": language,
        }
        return requests.patch(BR_URL + "user/account/", headers=self.__post_patch_headers__, json=updated_account)


    def change_password(self, headers: object, old_password: str, new_password: str):
        changed_password = {
            "old_password": old_password,
            "new_password": new_password
        }
        return requests.post(BR_URL + "user/change-password/", headers=headers, json=changed_password)

    
    def dashboard(self, headers: object):
        return requests.get(BR_URL + "user/dashboard/", headers=headers)


    #def reset_password(headers: object, client_session_id: object):

    
    """
    def token_auth(self, email: str, password: str):
        return requests.post(BR_URL + "user/token-auth/", json={"username": email, "password": password})
    
    
    def token_refresh(self, token: str):
        return requests.post(BR_URL + "user/token-refresh/", json={"token": token})
    
    
    def token_verify(self, token: str):
        return requests.post(BR_URL + "user/token-verify/", json={"token": token})
    
    
    def list_groups(self):
        return requests.get(BR_URL + "groups/", headers=self.__get_headers__)
    
    
    def create_group(self, name: str):
        return requests.post(BR_URL + "groups/", headers=self.__post_patch_headers__, json={"name": name})
    
    
    """
    def update_group(self, group_id: int, name: str):
        return requests.patch(BR_URL + f"groups/{group_id}/", headers=self.__post_patch_headers__, json={"name": name})
    
     
    def delete_group(self, group_id: int):
        return requests.delete(BR_URL + f"groups/{group_id}/", headers=self.__get_headers__)
    
    
    def leave_group(self, group_id: int):
        return requests.post(BR_URL + f"groups/{group_id}/leave/", headers=self.__post_patch_headers__)
    
    
    def update_group_user(self, group_user_id: int, permissions: str):
        return requests.post(BR_URL + f"groups/users/{group_user_id}/", headers=self.__post_patch_headers__, json={"permissions": permissions})
    
    
    def delete_group_user(self, group_user_id: int):
        return requests.delete(BR_URL + f"groups/users/{group_user_id}", headers=self.__get_headers__)
    
    
    def list_group_users(self, group_id: int):
        return requests.get(BR_URL + f"groups/users/group/{group_id}/", headers=self.__get_headers__)
    
    
    def get_application(self, application_id: int):
        return requests.get(BR_URL + f"applications/{application_id}/", headers=self.__get_headers__)
    """
    
    
    def list_all_applications(self):
        return requests.get(BR_URL + f"applications/", headers=self.__get_headers__)
    
    
    def create_application(self, group_id: int, name: str, type: str):
        application = {
            "name": name,
            "type": type
        }
        return requests.post(BR_URL + f"applications/group/{group_id}/", headers=self.__post_patch_headers__, json=application)
    
    
    def list_applications(self, group_id: int):
        return requests.get(BR_URL + f"applications/group/{group_id}/", headers=self.__get_headers__)
    
    
    """
    def get_database_table(self, table_id: int):
        return requests.get(BR_URL + f"database/tables/{table_id}/", headers=self.__get_headers__)
    
    
    def update_database_table(self, table_id: int, name: str):
        return requests.post(BR_URL + f"database/tables/{table_id}/", headers=self.__post_patch_headers__, json={"name": name})
    
    
    def delete_database_table(self, table_id: int):
        return requests.delete(BR_URL + f"database/tables/{table_id}/", headers=self.__get_headers__)
    
    
    def list_database_tables(self, database_id: int):
        return requests.get(BR_URL + f"database/tables/database/{database_id}/", headers=self.__get_headers__)    
    """
    
    def create_database_table(self, database_id: int, table: object):
        return requests.post(BR_URL + f"database/tables/database/{database_id}/", headers=self.__post_patch_headers__, json=table)
    
    
    """
    def get_database_table_field(self, field_id: int):
        return requests.get(BR_URL + f"database/fields/{field_id}/", headers=self.__get_headers__)
    
    
    def update_database_table_field(self, field_id: int, field: object):
        return requests.patch(BR_URL + f"database/fields/{field_id}/", headers=self.__post_patch_headers__, json=field)
    
    
    def delete_database_table_field(self, field_id: int):
        return requests.delete(BR_URL + f"database/fields/{field_id}/", headers=self.__get_headers__)
    
    
    def duplicate_table_field(self, field_id: int):
        return requests.delete(BR_URL + f"database/fields/{field_id}/duplicate/async/", headers=self.__get_headers__)
    
    
    def list_database_table_fields(self, table_id: int):
        return requests.get(BR_URL + f"database/fields/table/{table_id}/", headers=self.__get_headers__)
    """
    
    def create_database_table_field(self, table_id: int, field: object):
        return requests.post(BR_URL + f"database/fields/table/{table_id}/", headers=self.__post_patch_headers__, json=field)
    
    
    """
    def type_formula_field(self, table_id: int, formula: str, name: str):
        formula_dict = {
            "formula": formula,
            "name": name,
        }
        return requests.post(BR_URL + f"database/formula/{table_id}/type/", headers=self.__post_patch_headers__, json=formula_dict)
    

    def create_row(self, table_id: int, row: object, user_field_names=True):
        return requests.post(BR_URL + f"database/rows/table/{table_id}/?user_field_names={user_field_names}", headers=self.__post_patch_headers__, json=row)
    """
    