from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from typing import Type
from core.models import *
from api_v1.cvs.schemas_cvs import CVOrmCreate
from sqlalchemy.orm import selectinload


async def get_cvs(session=AsyncSession) -> any:
    result: Type[CVOrm] = await session.execute(select(CVOrm).order_by(CVOrm.id).options(
        selectinload(CVOrm.contact_info).options(selectinload(ContactInfo.social_links)),
        selectinload(CVOrm.skills), selectinload(CVOrm.tools), selectinload(CVOrm.courses),
        selectinload(CVOrm.education), selectinload(CVOrm.work_expirience),
        selectinload(CVOrm.languages), selectinload(CVOrm.personal_info), selectinload(CVOrm.photo)))
    return list(result.scalars().all())


async def get_my_cvs(session: AsyncSession, user) -> any:
    result: Type[CVOrm] = await session.execute(select(CVOrm).where(CVOrm.user_id == user).options(
        selectinload(CVOrm.contact_info).options(selectinload(ContactInfo.social_links)),
        selectinload(CVOrm.skills), selectinload(CVOrm.tools), selectinload(CVOrm.courses),
        selectinload(CVOrm.education), selectinload(CVOrm.work_expirience),
        selectinload(CVOrm.languages), selectinload(CVOrm.personal_info), selectinload(CVOrm.photo)))
    return list(result.scalars().all())


async def get_cv(session: AsyncSession, cv_id: int) -> any:
    return await session.get(CVOrm, cv_id)


async def get_cv_photo(session: AsyncSession, cv_id: int) -> any:
    stmt = select(CvPhoto).where(CvPhoto.cv_id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalar_one()
    return cv


async def get_contact_info(session: AsyncSession, cv_id: int) -> any:
    stmt = select(ContactInfo).where(ContactInfo.cv_id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalar_one()
    return cv


async def get_personal_info(session: AsyncSession, cv_id: int) -> any:
    stmt = select(PersonalInfo).where(PersonalInfo.cv_id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalar_one()
    return cv


async def get_social_links(session: AsyncSession, cv_id: int) -> any:
    stmt = select(SocialLinks).join(ContactInfo).where(ContactInfo.cv_id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_tools(session: AsyncSession, cv_id: int) -> any:
    stmt = select(Tools).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_skills(session: AsyncSession, cv_id: int) -> any:
    stmt = select(Skills).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_courses(session: AsyncSession, cv_id: int) -> any:
    stmt = select(Courses).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_education(session: AsyncSession, cv_id: int) -> any:
    stmt = select(Education).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_work_expirience(session: AsyncSession, cv_id: int) -> any:
    stmt = select(WorkExpirience).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def get_languages(session: AsyncSession, cv_id: int) -> any:
    stmt = select(Languages).join(CVOrm).where(CVOrm.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalars().all()
    return cv


async def create_cv(session: AsyncSession, cv_in: CVOrmCreate, user) -> any:
    cv = CVOrm(
        title=cv_in.title,
        user_id=user,
        contact_info=ContactInfo(email=cv_in.contact_info.email,
                                 phone=cv_in.contact_info.phone,
                                 social_links=[SocialLinks(link=link) for link in cv_in.contact_info.social_links]),
        photo=CvPhoto(url_image=cv_in.photo.url),
        personal_info=PersonalInfo(first_name=cv_in.personal_info.first_name,
                                   last_name=cv_in.personal_info.last_name,
                                   profession=cv_in.personal_info.profession,
                                   desired_salary=str(cv_in.personal_info.desired_salary),
                                   city=cv_in.personal_info.city,
                                   age=cv_in.personal_info.age
                                   ),
        tools=[Tools(name=tool.name) for tool in cv_in.tools],
        skills=[Skills(name=skill.name) for skill in cv_in.skills],
        education=[Education(university=institution.institution,
                             faculty=institution.faculty,
                             specialization=institution.specialization,
                             graduation_year=institution.graduation_year,
                             description=institution.description) for institution in cv_in.education],
        courses=[Courses(name=course.name,
                         institution=course.institution,
                         start_year=course.start_year,
                         end_year=course.end_year,
                         description=course.description) for course in cv_in.courses],
        work_expirience=[WorkExpirience(company_name=work.company_name,
                                        position=work.position,
                                        start_year=work.start_date,
                                        end_year=work.end_date,
                                        description=work.description) for work in cv_in.work_experience],
        languages=[Languages(name=language.name) for language in cv_in.languages]
    )
    session.add(cv)
    await session.commit()
    await session.refresh(cv)


async def update_cv(session: AsyncSession, cv_id: int, cv_in: CVOrmCreate, user: int) -> any:
    result: CVOrm = await session.execute(select(CVOrm).
    where(CVOrm.user_id == user,
          CVOrm.id == cv_id).
    options(
        selectinload(CVOrm.contact_info).options(selectinload(ContactInfo.social_links)),
        selectinload(CVOrm.skills), selectinload(CVOrm.tools), selectinload(CVOrm.courses),
        selectinload(CVOrm.education), selectinload(CVOrm.work_expirience),
        selectinload(CVOrm.languages), selectinload(CVOrm.photo), selectinload(CVOrm.personal_info)))
    cv = result.scalars().first()
    await session.delete(cv)

    updated_cv = CVOrm(
        title=cv_in.title,
        user_id=user,
        contact_info=ContactInfo(email=cv_in.contact_info.email,
                                 phone=cv_in.contact_info.phone,
                                 social_links=[SocialLinks(link=link) for link in cv_in.contact_info.social_links]),
        photo=CvPhoto(url_image=cv_in.photo.url),
        personal_info=PersonalInfo(first_name=cv_in.personal_info.first_name,
                                   last_name=cv_in.personal_info.last_name,
                                   profession=cv_in.personal_info.profession,
                                   desired_salary=cv_in.personal_info.desired_salary,
                                   city=cv_in.personal_info.city,
                                   age=cv_in.personal_info.age
                                   ),
        tools=[Tools(name=tool.name) for tool in cv_in.tools],
        skills=[Skills(name=skill.name) for skill in cv_in.skills],
        education=[Education(university=institution.institution,
                             faculty=institution.faculty,
                             specialization=institution.specialization,
                             graduation_year=institution.graduation_year,
                             description=institution.description) for institution in cv_in.education],
        courses=[Courses(name=course.name,
                         institution=course.institution,
                         start_year=course.start_year,
                         end_year=course.end_year,
                         description=course.description) for course in cv_in.courses],
        work_expirience=[WorkExpirience(company_name=work.company_name,
                                        position=work.position,
                                        start_year=work.start_date,
                                        end_year=work.end_date,
                                        description=work.description) for work in cv_in.work_experience],
        languages=[Languages(name=language.name) for language in cv_in.languages]
    )

    session.add(updated_cv)
    await session.commit()
    return updated_cv.id


async def delete_cv(session: AsyncSession, cv_id: int, user_id: int) -> None:
    row = await session.execute(select(CVOrm).where(CVOrm.id == cv_id, CVOrm.user_id == user_id))
    cv = row.scalar_one_or_none()
    await session.delete(cv)
    await session.commit()
