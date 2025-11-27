from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.USER.user_models import User

async def get_user_by_email_or_username(db: AsyncSession, identifier: str):
   query = await db.execute(select(User).where(User.email==identifier))
   return query.scalar_one_or_none()



