import json
from typing import List

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Cc, Mail


class SendGridMailer:
    SENDGRID_API_KEY = "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"

    @classmethod
    def send_mail(
        cls,
        subject: str,
        to_emails: List[str],
        cc_emails: List[str] = None,
        plain_text_content: str = None,
        html_content: str = None,
        from_user: str = "login@filed.com",
    ) -> dict:
        sg = SendGridAPIClient(cls.SENDGRID_API_KEY)
        message = Mail(
            from_email=from_user,
            to_emails=to_emails,
            subject=subject,
            plain_text_content=plain_text_content,
            html_content=html_content,
        )

        if cc_emails:
            message.add_cc([Cc(cc) for cc in cc_emails])

        response = sg.send(message)
        return {
            "status_code": response.status_code,
            "body": json.loads(response.body) if response.body else None,
            "x_message_id": response.headers.get("X-Message-Id"),
        }
