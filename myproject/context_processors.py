def global_context(request):
    context = {
        'user': request.user
    }
    return context
