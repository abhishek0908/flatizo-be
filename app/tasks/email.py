# Email sending logic moved from utils/email.py

import os
import logging
import httpx
import datetime
from typing import Optional
import asyncio
from app.celery_app.celery_worker import task

# You may want to use python-dotenv for local development
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

async def send_otp_email(recipient_email: str, recipient_name: str, otp: str) -> dict:
    """
    Send an OTP email using Brevo transactional email API.
    If the email is not sent successfully, raises an exception and OTP should NOT be sent/stored.
    Returns the response JSON on success.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Your OTP Code - Flatizo</title>
        <!--[if mso]>
        <noscript>
            <xml>
                <o:OfficeDocumentSettings>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
        </noscript>
        <![endif]-->
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #333333;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 30px;
                text-align: center;
                color: white;
            }}
            
            .logo {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                letter-spacing: -0.5px;
            }}
            
            .tagline {{
                font-size: 16px;
                opacity: 0.9;
                margin: 0;
            }}
            
            .content {{
                padding: 50px 40px;
            }}
            
            .greeting {{
                font-size: 20px;
                color: #2c3e50;
                margin-bottom: 25px;
                font-weight: 600;
            }}
            
            .message {{
                font-size: 16px;
                color: #555555;
                margin-bottom: 35px;
                line-height: 1.7;
            }}
            
            .otp-container {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                margin: 35px 0;
                box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
            }}
            
            .otp-label {{
                color: white;
                font-size: 14px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
                opacity: 0.9;
            }}
            
            .otp-code {{
                background-color: rgba(255, 255, 255, 0.95);
                color: #2c3e50;
                font-size: 36px;
                font-weight: bold;
                padding: 20px 30px;
                border-radius: 8px;
                letter-spacing: 8px;
                margin: 0 auto;
                display: inline-block;
                font-family: 'Courier New', monospace;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }}
            
            .validity {{
                color: white;
                font-size: 13px;
                margin-top: 15px;
                opacity: 0.9;
            }}
            
            .instructions {{
                background-color: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px 25px;
                margin: 30px 0;
                border-radius: 0 8px 8px 0;
            }}
            
            .instructions h3 {{
                color: #2c3e50;
                font-size: 16px;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            
            .instructions ul {{
                margin: 0;
                padding-left: 20px;
                color: #555555;
            }}
            
            .instructions li {{
                margin-bottom: 8px;
                font-size: 14px;
            }}
            
            .security-notice {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 20px;
                margin: 30px 0;
            }}
            
            .security-notice .icon {{
                color: #856404;
                font-size: 18px;
                margin-right: 10px;
            }}
            
            .security-notice p {{
                color: #856404;
                font-size: 14px;
                margin: 0;
                display: flex;
                align-items: flex-start;
            }}
            
            .footer {{
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 30px 40px;
                text-align: center;
            }}
            
            .footer p {{
                margin: 0 0 15px 0;
                font-size: 14px;
                line-height: 1.5;
            }}
            
            .footer .company-info {{
                opacity: 0.8;
                font-size: 12px;
                margin-top: 20px;
            }}
            
            .support-link {{
                color: #3498db;
                text-decoration: none;
                font-weight: 500;
            }}
            
            .support-link:hover {{
                text-decoration: underline;
            }}
            
            @media only screen and (max-width: 600px) {{
                .email-container {{
                    width: 100% !important;
                    margin: 0 !important;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .content {{
                    padding: 30px 20px;
                }}
                
                .footer {{
                    padding: 25px 20px;
                }}
                
                .otp-code {{
                    font-size: 28px;
                    letter-spacing: 4px;
                    padding: 15px 20px;
                }}
                
                .logo {{
                    font-size: 28px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">Flatizo</div>
                <p class="tagline">Your trusted property platform</p>
            </div>
            
            <div class="content">
                <div class="greeting">Hello {recipient_name},</div>
                
                <div class="message">
                    We've received a request to verify your account. Please use the One-Time Password (OTP) below to complete your verification process.
                </div>
                
                <div class="otp-container">
                    <div class="otp-label">Your Verification Code</div>
                    <div class="otp-code">{otp}</div>
                    <div class="validity">This code expires in {10} minutes</div>
                </div>
                
                <div class="instructions">
                    <h3>How to use this code:</h3>
                    <ul>
                        <li>Enter this {len(otp)}-digit code in the verification field</li>
                        <li>Complete the process within {10} minutes</li>
                        <li>Do not share this code with anyone</li>
                    </ul>
                </div>
                
                <div class="security-notice">
                    <p>
                        <span class="icon">🔒</span>
                        <span>If you didn't request this verification, please ignore this email or contact our support team immediately.</span>
                    </p>
                </div>
                
                <div class="message">
                    If you're having trouble with the verification process, please don't hesitate to reach out to our <a href="mailto:support@flatizo.com" class="support-link">support team</a>.
                </div>
            </div>
            
            <div class="footer">
                <p>Thank you for choosing Flatizo!</p>
                <p>This is an automated message, please do not reply to this email.</p>
                <div class="company-info">
                    <p>© 2025 Flatizo. All rights reserved.</p>
                    <p>Questions? Contact us at <a href="mailto:support@flatizo.com" class="support-link">support@flatizo.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    payload = {
        "sender": {"name": "Flatizo", "email": "abhishekudiya09@gmail.com"},
        "to": [{"email": recipient_email, "name": recipient_name}],
        "subject": "Your OTP Code for Flatizo",
        "htmlContent": html_content,
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }
    # Configure timeout settings (30 seconds total, 10 seconds for connection)
    timeout = httpx.Timeout(30.0, connect=10.0)
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(BREVO_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            logging.info(f"OTP email sent successfully to {recipient_email}")
            return response.json()
    except httpx.ReadTimeout:
        logging.error(f"Timeout while sending OTP email to {recipient_email}")
        raise Exception("Email service timeout. Please try again later.")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error while sending OTP email: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Failed to send email: {e.response.status_code}")
    except httpx.RequestError as e:
        logging.error(f"Request error while sending OTP email: {str(e)}")
        raise Exception("Failed to connect to email service. Please try again later.")
    except Exception as e:
        logging.error(f"Unexpected error while sending OTP email: {str(e)}")
        raise Exception("Failed to send OTP email. Please try again later.")


# Celery task wrapper for the async function
@task
def send_otp_email_task(recipient_email: str, recipient_name: str, otp: str) -> dict:
    """
    Celery task wrapper for send_otp_email async function.
    This allows the email sending to be processed in the background.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            send_otp_email(recipient_email, recipient_name, otp)
        )
        return result
    finally:
        loop.close()
