from .base import Base
from typing import List
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column


class CVOrm(Base):
    __tablename__ = "cvs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    user = relationship("UserOrm", back_populates="cvs")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    photo: Mapped["CvPhoto"] = relationship(back_populates="cv",cascade="all, delete-orphan")
    personal_info: Mapped["PersonalInfo"] = relationship(back_populates="cv", cascade="all, delete-orphan")
    contact_info: Mapped["ContactInfo"] = relationship(back_populates="cv", cascade="all, delete-orphan")
    tools: Mapped[List["Tools"]] = relationship(back_populates="cv", cascade="all, delete-orphan")
    education: Mapped[List["Education"]] = relationship(back_populates="cv", cascade="all, delete-orphan")
    skills: Mapped[List["Skills"]] = relationship(back_populates="cv", cascade="all, delete-orphan")
    courses: Mapped[List["Courses"]] = relationship(back_populates="cv", cascade="all, delete-orphan")
    work_expirience: Mapped[List["WorkExpirience"]] = relationship(back_populates="cv", cascade="all, delete-orphan")
    languages: Mapped[List["Languages"]] = relationship(back_populates="cv", cascade="all, delete-orphan")

    def __str__(self):
        return str(self.__dict__)

class CvPhoto(Base):
    __tablename__ = "CvPhotos"
    photo_id = Column(Integer, primary_key=True, index=True)
    url_image = Column(String, nullable=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv = relationship("CVOrm", back_populates="photo")
    
    def __str__(self):
        return str(self.__dict__)
    
    
class PersonalInfo(Base):
    __tablename__ = "PersonalInfo"
    personal_info_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    profession = Column(String, nullable=False)
    desired_salary = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="personal_info")
    
    def __str__(self):
        return str(self.__dict__)
    

class SocialLinks(Base):
    __tablename__ = "SocialLinks"
    social_links_id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    contact_info_id = Column(Integer, ForeignKey("ContactInfo.contact_info_id"), nullable=False)
    contact_info: Mapped["ContactInfo"] = relationship(back_populates="social_links")
    
    def __str__(self):
        return str(self.__dict__)

class ContactInfo(Base):
    __tablename__ = "ContactInfo"
    contact_info_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    social_links: Mapped[List["SocialLinks"]] = relationship(back_populates="contact_info", cascade="all, delete-orphan")
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="contact_info")
    
    def __str__(self):
        return str(self.__dict__)


class Skills(Base):
    __tablename__= "Skills"
    skill_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cv_id: Mapped[int] = mapped_column(ForeignKey("cvs.id"))
    cv: Mapped["CVOrm"] = relationship(back_populates="skills")
    
    def __str__(self):
        return str(self.__dict__)
    
class Tools(Base):
    __tablename__ = "Tools"
    tool_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="tools")
    
    def __str__(self):
        return str(self.__dict__)
    
class Education(Base):
    __tablename__ = "Education"
    education_id = Column(Integer, primary_key=True, index=True)
    university = Column(String, nullable=False)
    faculty = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="education")
    
    def __str__(self):
        return str(self.__dict__)


class Courses(Base):
    __tablename__ = "Courses"
    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="courses")
    
    def __str__(self):
        return str(self.__dict__)


class WorkExpirience(Base):
    __tablename__ = "work_experience"
    work_experince_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="work_expirience")
    
    def __str__(self):
        return str(self.__dict__)
    
class Languages(Base):
    __tablename__ = "languages"
    language_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    cv: Mapped["CVOrm"] = relationship(back_populates="languages")
    
    def __str__(self):
        return str(self.__dict__)
