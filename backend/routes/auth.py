### backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import (
    User,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /register
# ---------------------------------------------------------------------------


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account.

    Returns the created user on success.  Raises **400** if the email is
    already taken.
    """
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------------------------------------------------------------------------
# POST /login
# ---------------------------------------------------------------------------


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with email and password.

    Returns a JWT bearer token on success.  Raises **401** if the credentials
    are invalid.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


# ---------------------------------------------------------------------------
# GET /me
# ---------------------------------------------------------------------------


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return current_user
