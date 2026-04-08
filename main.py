from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models
from auth import hash_password, verify_password, create_access_token, get_current_user
import random

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home API
@app.get("/")
def home():
    return {"message": "API working da 😄"}

# 🔥 REGISTER (WITH OTP + SUBSCRIPTION)
@app.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered ❌")

    hashed_pwd = hash_password(password)

    # 🔥 OTP GENERATE
    otp = str(random.randint(1000, 9999))
    print("OTP:", otp)

    # 🔥 CREATE USER
    new_user = models.User(
        email=email,
        password=hashed_pwd,
        is_active=True,
        otp_code=otp,
        otp_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔥 CREATE DEFAULT SUBSCRIPTION
    new_subscription = models.Subscription(
        user_id=new_user.id,
        plan="free",
        status="active"
    )

    db.add(new_subscription)
    db.commit()

    return {"message": "User created successfully 😄"}

# 🔐 VERIFY OTP
@app.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    if user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP ❌")

    user.otp_verified = True
    db.commit()

    return {"message": "OTP verified successfully ✅"}

# 🔑 LOGIN
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    if not user.otp_verified:
        raise HTTPException(status_code=400, detail="Verify OTP first ❌")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password ❌")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# 👤 PROFILE
@app.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    return {
        "message": "Profile fetched 😄",
        "user": current_user
    }

# 📁 CREATE PROJECT (WITH LIMIT)
@app.post("/create-project")
def create_project(
    name: str,
    description: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    # 🔥 GET SUBSCRIPTION
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user.id
    ).first()

    # 🔥 COUNT PROJECTS
    project_count = db.query(models.Project).filter(
        models.Project.owner_id == user.id
    ).count()

    # 🔥 APPLY LIMIT
    if subscription and subscription.plan == "free" and project_count >= 3:
        raise HTTPException(
            status_code=400,
            detail="Free plan limit reached. Upgrade to Pro 🚀"
        )

    new_project = models.Project(
        name=name,
        description=description,
        owner_id=user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created successfully 🚀"}

# 📁 GET MY PROJECTS
@app.get("/my-projects")
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    return db.query(models.Project).filter(
        models.Project.owner_id == user.id
    ).all()
@app.post("/upgrade-pro")
def upgrade_pro(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    # 🔥 UPDATE SUBSCRIPTION
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user.id
    ).first()

    subscription.plan = "pro"

    # 🔥 PAYMENT SIMULATION
    payment = models.Payment(
        user_id=user.id,
        amount=999,
        status="success"
    )

    db.add(payment)
    db.commit()

    return {"message": "Upgraded to Pro successfully 💰🚀"}
@app.get("/payment-history")
def payment_history(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # 🔥 user fetch
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    # 🔥 get payments
    payments = db.query(models.Payment).filter(
        models.Payment.user_id == user.id
    ).all()

    return payments
@app.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized ❌")

    return db.query(models.User).all()
@app.get("/admin/subscriptions")
def get_all_subscriptions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized ❌")

    return db.query(models.Subscription).all()
@app.get("/admin/payments")
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized ❌")

    return db.query(models.Payment).all()
@app.post("/notify")
def create_notification(
    title: str,
    message: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    notification = models.Notification(
        user_id=user.id,
        title=title,
        message=message
    )

    db.add(notification)
    db.commit()

    return {"message": "Notification created 🔔"}
@app.get("/my-notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()

    return db.query(models.Notification).filter(
        models.Notification.user_id == user.id
    ).all()