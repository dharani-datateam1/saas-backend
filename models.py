from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean



# USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200))
    is_active = Column(Boolean, default=True)
    otp_code = Column(String(10))
    otp_verified = Column(Boolean, default=False)
    projects = relationship("Project", back_populates="owner")
    role = Column(String(20), default="user")


# PROJECT TABLE
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(200))

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


# TASK TABLE 🔥
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))

    # 🔥 ADD THIS LINE (IMPORTANT)
    status = Column(String(50), default="pending")

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="tasks")
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    plan = Column(String(50), default="free")
    status = Column(String(50), default="active")
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    amount = Column(Integer)
    status = Column(String(50))
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String(100))
    message = Column(String(255))