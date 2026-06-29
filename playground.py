import asyncio

from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel


async def main():

    llm = LLMClient()

    communication = CommunicationDepartment(llm)

    athena = AthenaKernel(communication)

    response = await athena.chat(
        "Who are you? Answer in one sentence."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())