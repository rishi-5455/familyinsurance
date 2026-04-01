from app import mongo


class ClaimModel:
    @staticmethod
    def collection():
        return mongo.db.claims

    @staticmethod
    def create(data):
        return ClaimModel.collection().insert_one(data)

    @staticmethod
    def find_by_claim_id(claim_id):
        return ClaimModel.collection().find_one({"claimId": claim_id})

    @staticmethod
    def update_status(claim_id, status):
        return ClaimModel.collection().update_one({"claimId": claim_id}, {"$set": {"status": status}})

    @staticmethod
    def list_by_user(user_id):
        return list(ClaimModel.collection().find({"userId": user_id}))
    
    @staticmethod
    def list_all():
        return list(ClaimModel.collection().find({}))