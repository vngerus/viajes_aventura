import re
from typing import Optional

def validar_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    
    # Patrón básico de validación de email
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email.strip()))

def validar_password(password: str, min_length: int = 6) -> tuple[bool, Optional[str]]:
    if not password:
        return False, "La contraseña no puede estar vacía"
    
    if len(password) < min_length:
        return False, f"La contraseña debe tener al menos {min_length} caracteres"
    
    return True, None

def validar_nombre(nombre: str) -> tuple[bool, Optional[str]]:
    if not nombre or not nombre.strip():
        return False, "El nombre no puede estar vacío"
    
    if len(nombre.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if len(nombre.strip()) > 100:
        return False, "El nombre no puede exceder 100 caracteres"
    
    return True, None

def validar_precio(precio: float) -> tuple[bool, Optional[str]]:
    if precio < 0:
        return False, "El precio no puede ser negativo"
    
    if precio == 0:
        return False, "El precio debe ser mayor a cero"
    
    return True, None

def validar_stock(stock: int) -> tuple[bool, Optional[str]]:
    if stock < 0:
        return False, "El stock no puede ser negativo"
    
    return True, None

