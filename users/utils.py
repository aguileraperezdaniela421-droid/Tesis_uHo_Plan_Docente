def get_user_type(user):
    if not user.is_authenticated:
        return 'anonymous'
    if user.is_superuser:
        return 'superadmin'
    if user.is_staff:
        return 'admin_institucional'
    if user.groups.filter(name='Directivos').exists():
        return 'directivo'
    
    # Si no es ninguno de los anteriores, revisamos su perfil docente
    if hasattr(user, 'teacherprofile'):
        if user.teacherprofile.role == 'head':
            return 'jefe'
        elif user.teacherprofile.role == 'teacher':
            return 'profesor'
            
    return 'desconocido'