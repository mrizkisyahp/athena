import asyncio

from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient


async def main():
    llm = LLMClient()

    communication = CommunicationDepartment(llm)

    response = await communication.chat(
        "Introduce yourself as Athena in one sentence."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())