def validate_registration(password, confirm_password, service, email):
    if password != confirm_password:
        return "Пароли не совпадают"
    if service.is_email_taken(email):
        return "Эта почта уже зарегистрирована"
    return None
