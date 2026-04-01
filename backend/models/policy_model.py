from app import mongo


class PolicyModel:
    @staticmethod
    def collection():
        return mongo.db.policies

    @staticmethod
    def create(data):
        return PolicyModel.collection().insert_one(data)

    @staticmethod
    def find_by_policy_id(policy_id):
        return PolicyModel.collection().find_one({"policyId": policy_id})

    @staticmethod
    def list_by_user(user_id):
        return list(PolicyModel.collection().find({"userId": user_id}))

    @staticmethod
    def list_all():
        return list(PolicyModel.collection().find({}))

    @staticmethod
    def update_status(policy_id, status):
        return PolicyModel.collection().update_one({"policyId": policy_id}, {"$set": {"status": status}})
