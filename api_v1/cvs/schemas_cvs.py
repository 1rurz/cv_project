from pydantic import BaseModel, ConfigDict
from typing import List
from pydantic import BaseModel, Field

class CVOrmBase(BaseModel):
    __tablename__ = "cvs"
    title: str
    description: str
    user_id: int


class CVOrmCreate(BaseModel):
    title: str
    photo: 'Photo'
    personal_info: 'PersonalInfo'
    contact_info: 'ContactInfo'
    skills: List['Skill']
    tools: List['Tool']
    education: List['Education']
    courses: List['Course']
    work_experience: List['WorkExperience'] 
    languages: List['Language']

class Photo(BaseModel):
    url: str

class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    profession: str
    desired_salary: int 
    city: str
    age: str

class ContactInfo(BaseModel):
    email: str
    phone: str
    social_links: List[str] = []

class Skill(BaseModel):
    name: str

class Tool(BaseModel):
    name: str

class Education(BaseModel):
    institution: str
    faculty: str
    specialization: str
    graduation_year: int
    description: str = "" 

class Course(BaseModel):
    name: str
    institution: str
    start_year: int
    end_year: int
    description: str = "" 

class WorkExperience(BaseModel):
    company_name: str
    position: str
    start_date: str
    end_date: str
    description: str = "" 

class Language(BaseModel):
    name: str




class CVOrmUpdatePartial(CVOrmCreate):
    pass


class CVOrm(CVOrmBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    
    
class SocialLink(BaseModel):
        id: int
        link: str

class CVOrmUpdate(BaseModel):
    title: str
    photo: 'Photo'
    personal_info: 'PersonalInfo'
    contact_info: 'ContactInfo'
    skills: List['Skill']
    tools: List['Tool']
    education: List['Education']
    courses: List['Course']
    work_experience: List['WorkExperience'] 
    languages: List['Language']

    class Photo(BaseModel):
        url: str

    class PersonalInfo(BaseModel):
        first_name: str
        last_name: str
        profession: str
        desired_salary: str 
        city: str
        age: str

    
    
    
    class ContactInfo(BaseModel):
        email: str
        phone: str
        social_links: List['SocialLink']
        
    
    
    class Skill(BaseModel):
        id: int
        name: str

    class Tool(BaseModel):
        id: int
        name: str

    class Education(BaseModel):
        id: int
        institution: str
        faculty: str
        specialization: str
        graduation_year: int
        description: str = "" 

    class Course(BaseModel):
        id: int
        name: str
        institution: str
        start_year: int
        end_year: int
        description: str = "" 

    class WorkExperience(BaseModel):
        id: int
        company_name: str
        position: str
        start_date: str
        end_date: str
        description: str = "" 

    class Language(BaseModel):
        id: int
        name: str
