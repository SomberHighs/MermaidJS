import asyncio
from aiosmtpd.controller import Controller

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        print("---------- MESSAGE RECEIVED ----------")
        print(f"Envelope From: {envelope.mail_from}")
        print(f"Envelope To: {envelope.rcpt_tos}")
        print("Message Data:")
        # Decode bytes to string for printing
        print(envelope.content.decode('utf8', errors='replace'))
        print("--------------------------------------")
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    print("Starting Debug SMTP server on localhost:1025...")
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    controller.start()

    # Keep the script running
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        controller.stop()
