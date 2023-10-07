def user_scheme(user) -> dict:
     return {"id": str(user["_id"]),
             "username": user["username"]}
 
def users_scheme(users) -> list:
        return [user_scheme(user) for user in users]