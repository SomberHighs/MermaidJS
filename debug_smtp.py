import asyncio
from aiosmtpd.controller import Controller

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        print("---------- MESSAGE RECEIVED ----------")
        print(f"Envelope From: {envelope.mail_from}")
        print(f"Envelope To: {envelope.rcpt_tos}")
        print("Message Data:")
        print(envelope.content.decode('utf8', errors='replace'))
        print("--------------------------------------")
        return '250 Message accepted for delivery'

async def main():
    print("Starting Debug SMTP server on localhost:1025...")
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    controller.start()
    
    # Keep running until cancelled
    try:
        # Create a future that never completes to keep the loop alive
        await asyncio.get_running_loop().create_future()
    except asyncio.CancelledError:
        print("\nStopping server...")
        controller.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
