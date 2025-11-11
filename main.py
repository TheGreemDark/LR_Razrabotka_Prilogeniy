from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db import SessionLocal
from models import User

def show_users_with_addresses():
    with SessionLocal() as session:
        stmt = select(User).options(selectinload(User.addresses))
        for user in session.execute(stmt).scalars():
            print(user.name, [a.city for a in user.addresses])

if __name__ == "__main__":
    show_users_with_addresses()