from app import mongo


class UserModel:
    @staticmethod
    def collection():
        return mongo.db.users

    @staticmethod
    def create(data):
        return UserModel.collection().insert_one(data)

    @staticmethod
    def find_by_email(email):
        return UserModel.collection().find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return UserModel.collection().find_one({"_id": user_id})

    @staticmethod
    def list_all():
        return list(UserModel.collection().find({}, {"password": 0}))
