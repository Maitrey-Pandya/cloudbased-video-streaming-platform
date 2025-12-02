import json
import boto3
import datetime
import rsa 
import base64
import time
import os

# --- CONFIGURATION (Ensure these lines exist above the handler) ---
# PARAMETER_NAME = "/vidstream/private_key" 
# KEY_PAIR_ID = os.environ.get('KEY_PAIR_ID_PLAYBACK')
# CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN') 
# ... (rest of configuration and helper functions)

def lambda_handler(event, context):
    try:
        # ... (signing logic happens here) ...

        # --- FRONTEND ORIGIN CONFIGURATION ---
        # NOTE: You must use the exact origin used by the frontend (localhost or domain)
        # We try to read the Origin header sent by the browser, otherwise default to a known value.
        origin = event.get('headers', {}).get('origin') or event.get('headers', {}).get('Origin') or 'http://localhost:5173'
        
        # 4. Return Cookies in MultiValueHeaders
        return {
            'statusCode': 200,
            'headers': {
                # 🛠️ THE CORS FIX: Overriding API Gateway failures
                "Access-Control-Allow-Origin": origin, 
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json",
            },
            'multiValueHeaders': {
                'Set-Cookie': [
                    f"CloudFront-Policy={policy_base64}; Domain={CLOUDFRONT_DOMAIN}; Path=/; Secure; SameSite=None",
                    f"CloudFront-Signature={signature_base64}; Domain={CLOUDFRONT_DOMAIN}; Path=/; Secure; SameSite=None",
                    f"CloudFront-Key-Pair-Id={KEY_PAIR_ID}; Domain={CLOUDFRONT_DOMAIN}; Path=/; Secure; SameSite=None"
                ]
            },
            'body': json.dumps({'message': 'Stream authorized successfully'})
        }

    except Exception as e:
        # ... (error handling remains the same) ...
        # Ensure the error response also includes CORS for debugging!
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }