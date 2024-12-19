import os
import asyncio
from dotenv import load_dotenv
from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Quote, Candle

load_dotenv()

# Retrieve credentials from environment variables
user = os.getenv('TASTY_USER')
passw = os.getenv('TASTY_PASS')

async def main():
    # Initialize the session
    session = Session(user, passw)

    # Use async context manager if DXLinkStreamer supports it
    async with DXLinkStreamer(session) as streamer:
        subs_list = ['/ESH25:XCME']  # List of subscriptions

        # Subscribe to quotes asynchronously
        await streamer.subscribe(Quote, subs_list)
        print(f"Subscribed to quotes for symbols: {', '.join(subs_list)}")

        try:
            while True:
                # Await the next quote event
                quote = await streamer.get_event(Quote)
                print("Quote received:")
                print(quote)
        except asyncio.CancelledError:
            print("Quote streaming has been cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())