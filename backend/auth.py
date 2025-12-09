from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

ADMIN_EMAILS = [
    "fabriciomacedo@bemol.com.br",
    "alinesantiago@bemol.com.br",
    "antonioguedes@bemol.com.br"
]
ADMIN_PASSWORD = "Bemol@2025"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    is_correct_username = credentials.username in ADMIN_EMAILS
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return credentials.username
