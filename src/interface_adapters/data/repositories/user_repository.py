from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text

from domain.ports.users import ClaimsPort, RolesOutputPort, UsersOutputPort
from frameworks.database.postgres_manager import PostgresqlManager
from interface_adapters.data.models.users import Role, User, UserClaim


class UserRepository:
    """Repository to handle user data."""

    def __init__(self, database_service: PostgresqlManager) -> None:
        self._db = database_service

    async def add_user(self, user: User) -> User:
        """Add a new user to the database."""
        await self._db.connect()
        async with self._db.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def add_user_claims(self, user_id: int, claims: list[int]) -> None:
        """Add claims to a user in the database and return the updated user."""
        await self._db.connect()
        async with self._db.session() as session:
            user_claims = [UserClaim(user_id=user_id, claim_id=claim_id) for claim_id in claims]
            session.add_all(user_claims)
            await session.commit()

    async def find_info_by_id(self, user_id: int) -> UsersOutputPort | None:
        """Find user info by user_id."""
        await self._db.connect()
        async with self._db.session() as session:
            query = (
                select(User)
                .filter(User.id == user_id)
                .options(
                    # Carregar relacionamentos (roles e claims)
                    joinedload(User.role),
                    joinedload(User.user_claims).joinedload(UserClaim.claim),
                )
            )
            result = await session.execute(query)
            if not (user := result.scalars().first()):
                return None

            user_dict = {
                "name": user.name,
                "email": user.email,
                "role": user.role.description if user.role else None,
                "claims": [
                    ClaimsPort(
                        description=claim.claim.description, active=claim.claim.active
                    )
                    for claim in user.user_claims
                    if claim.claim.active
                ]
                if user.user_claims
                else [],
            }

        return UsersOutputPort(**user_dict)

    async def find_user_by_id_using_raw(self, user_id: int) -> UsersOutputPort | None:
        """Find user by user_id using raw SQL."""
        sql_query = text("""
            SELECT 
                u.name AS user_name, 
                u.email AS user_email, 
                r.description AS role, 
                c.description AS claim_description,
                c.active AS claim_active
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            LEFT JOIN user_claims uc ON u.id = uc.user_id
            LEFT JOIN claims c ON uc.claim_id = c.id
            WHERE u.id = :user_id
        """)

        await self._db.connect()
        async with self._db.session() as session:
            result = await session.execute(sql_query, {"user_id": user_id})
            rows = result.fetchall()

            if not rows:
                return None

            user_data = {
                "name": rows[0].user_name,
                "email": rows[0].user_email,
                "role": rows[0].role,
                "claims": [
                    ClaimsPort(description=row.claim_description, active=row.claim_active)
                    for row in rows if row.claim_description
                ],
            }

            return UsersOutputPort(**user_data)

    async def find_by_role_id(self, role_id: int) -> RolesOutputPort | None:
        """Find user by role_id."""
        await self._db.connect()
        async with self._db.session() as session:
            query = select(Role).filter(Role.id == role_id)
            result = await session.execute(query)
            if not (role := result.scalars().first()):
                return None

            role_dict = {"description": role.description}

            return RolesOutputPort(**role_dict)
