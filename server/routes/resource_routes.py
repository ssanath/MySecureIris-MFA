from flask import Blueprint, request, jsonify
from db import db
from bson.objectid import ObjectId

resource_bp = Blueprint("resources", __name__)
resources_collection = db["resources"]

# -------------------- Create Resource --------------------
@resource_bp.route("/create", methods=["POST"])
def create_resource():
    try:
        data = request.json
        print("🔥 Incoming data:", data)

        resource_type = data.get("type")
        owner_email = data.get("email")

        if not resource_type or not owner_email:
            print("⚠️ Missing fields")
            return jsonify({"success": False, "message": "Missing fields"}), 400

        # Count how many resources of this type user already has
        count = resources_collection.count_documents({
            "owner_email": owner_email,
            "type": resource_type
        })

        name = f"{resource_type}{count + 1}"

        new_resource = {
            "type": resource_type,
            "name": name,
            "owner_email": owner_email
        }

        result = resources_collection.insert_one(new_resource)

        # Add the inserted _id as string for frontend display
        new_resource["_id"] = str(result.inserted_id)

        print("✅ Created resource:", new_resource)
        return jsonify({
            "success": True,
            "message": f"{resource_type.capitalize()} created",
            "resource": new_resource
        }), 201

    except Exception as e:
        print("❌ ERROR during resource creation:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500

# -------------------- List Resources --------------------
@resource_bp.route("/list/<email>", methods=["GET"])
def list_resources(email):
    try:
        user_resources = list(resources_collection.find({"owner_email": email}))
        for res in user_resources:
            res["_id"] = str(res["_id"])  # Convert ObjectId to string
        return jsonify({"success": True, "resources": user_resources}), 200
    except Exception as e:
        print("❌ ERROR during list:", e)
        return jsonify({"success": False, "message": "Failed to list resources"}), 500

# -------------------- Delete Resource --------------------
@resource_bp.route("/delete/<name>", methods=["DELETE"])
def delete_resource(name):
    try:
        result = resources_collection.delete_one({"name": name})
        if result.deleted_count == 1:
            print(f"🗑️ Deleted resource: {name}")
            return jsonify({"success": True, "message": f"{name} deleted"}), 200
        print(f"⚠️ Resource not found: {name}")
        return jsonify({"success": False, "message": f"{name} not found"}), 404
    except Exception as e:
        print("❌ ERROR during delete:", e)
        return jsonify({"success": False, "message": "Delete error"}), 500
