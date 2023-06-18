def language(request):
    return {'current_language': request.session.get('language')}