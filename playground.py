import asyncio

from app.integrations.llm import llm_client


async def main():
    print("Talking to Athena...\n")

    response = await llm_client.generate(
        "Reply with exactly: Athena is online."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())