import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
from src.constants import AWS_REGION, COGNITO_USER_POOL_ID, COGNITO_APP_CLIENT_ID


keys_url = f'https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json'
keys = None


def validate_jwt_token(token):
    # instead of re-downloading the public keys every time
    # we download them only once and reuse them for subsequent calls
    # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
    global keys
    if(keys is None):
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']
        
    # get the kid from the headers prior to verification
    token = token.replace('Bearer ', '')
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != COGNITO_APP_CLIENT_ID:
        print('Token was not issued for this audience')
        return False
        
    # now we can use the claims
    user_data = json.loads(claims['userData'])
    return claims, user_data