from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import hash_password, verify_password, create_jwt_token
from app.db import get_db
from app.schemas import RegisterSchema, LoginSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db: Session = next(get_db())
    data = request.get_json()

    try:
        # Validate request data
        errors = RegisterSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        username = f"{data['first_name'].lower()}{data['last_name'].lower()}{data['dob'].replace('-', '')}"

# Check if email already exists
        existing_user = db.query(User).filter_by(email=data["email"]).first()
        if existing_user:
             return jsonify({"message": "Email already registered"}), 400

# Save user
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            email=data["email"],
            dob=data["dob"],
            username=username,
            password=hash_password(data["password"])
)
        db.add(new_user)
        db.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.rollback()  # Rollback in case of a database integrity issue
        return jsonify({"message": "Database integrity error. Possibly a duplicate entry."}), 400

    except SQLAlchemyError as e:
        db.rollback()  # Rollback for any other database-related error
        return jsonify({"message": "Database error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500

    finally:
        db.close()  # Ensure the session is closed


@auth_bp.route("/login", methods=["POST"])
def login():
    db: Session = next(get_db())
    data = request.get_json()
    try:
        errors = LoginSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        user = db.query(User).filter_by(email=data["email"]).first()
        if not user or not verify_password(data["password"], user.password):
            return jsonify({"message": "Invalid credentials"}), 401
        
        access_token = create_jwt_token(str(user.id),user.email)
        return jsonify(access_token=access_token), 200
    except IntegrityError:
        db.rollback()  # Rollback in case of a database integrity issue
        return jsonify({"message": "Database integrity error. Possibly a duplicate entry."}), 400

    except SQLAlchemyError as e:
        db.rollback()  # Rollback for any other database-related error
        return jsonify({"message": "Database error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500

    finally:
        db.close()  # Ensure the session is closed