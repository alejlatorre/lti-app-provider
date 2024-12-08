import asyncio

from app.models.database import async_session
from app.models.lti import LTIDeployment


async def create_test_deployment():
    """Create a test deployment"""
    async with async_session() as session:
        deployment = LTIDeployment(
            client_id="test_client",
            deployment_id="test_deployment",
            platform_issuer="https://canvas.instructure.com",
        )
        session.add(deployment)
        await session.commit()
        return deployment


if __name__ == "__main__":
    asyncio.run(create_test_deployment())
