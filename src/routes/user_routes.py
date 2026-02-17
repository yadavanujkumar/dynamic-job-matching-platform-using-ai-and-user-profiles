from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

router = APIRouter()

# Mock database (replace with actual database integration)
mock_users_db = {}

# Secret key for JWT (use environment variable in production)
SECRET_KEY = "your_secret_key"


# Pydantic models
class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    skills: Optional[List[str]] = Field(default_factory=list)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    skills: Optional[List[str]] = None
    preferences: Optional[Dict] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    desired_location: Optional[str] = None


# Helper function to get current user from token
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Extract and validate JWT token from Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    try:
        # Remove 'Bearer ' prefix if present
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = mock_users_db.get(data['user_id'])
        if not current_user:
            raise HTTPException(status_code=401, detail="User not found")
        return current_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")


@router.post("/register", response_model=Dict)
async def register_user(user: UserRegister):
    """
    Register a new user with email and password.
    """
    # Check if email already exists
    if any(u['email'] == user.email for u in mock_users_db.values()):
        raise HTTPException(status_code=409, detail="Email already exists")
    
    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
    
    mock_users_db[user_id] = {
        'user_id': user_id,
        'name': user.name,
        'email': user.email,
        'password': hashed_password,
        'skills': user.skills,
        'profile': {}
    }
    
    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "email": user.email
    }


@router.post("/login", response_model=Dict)
async def login_user(credentials: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    user = next((u for u in mock_users_db.values() if u['email'] == credentials.email), None)
    
    if not user or not check_password_hash(user['password'], credentials.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = jwt.encode({
        'user_id': user['user_id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
    
    return {
        "message": "Login successful",
        "token": token,
        "user_id": user['user_id']
    }


@router.get("/profile", response_model=Dict)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile information.
    """
    return {
        'user_id': current_user['user_id'],
        'name': current_user['name'],
        'email': current_user['email'],
        'skills': current_user.get('skills', []),
        'profile': current_user.get('profile', {})
    }


@router.put("/profile", response_model=Dict)
async def update_user_profile(
    profile: UserProfile,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's profile information.
    """
    profile_data = profile.dict(exclude_unset=True)
    
    # Update skills if provided
    if profile.skills is not None:
        current_user['skills'] = profile.skills
    
    # Update other profile fields
    if 'profile' not in current_user:
        current_user['profile'] = {}
    
    current_user['profile'].update({k: v for k, v in profile_data.items() if v is not None and k != 'skills'})
    
    return {
        "message": "Profile updated successfully",
        "profile": current_user['profile'],
        "skills": current_user.get('skills', [])
    }