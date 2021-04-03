from django_blog.roles import canCreate

def canCreateNewPost_renderer(request):
    return ({'CurrentUserCanPost' : canCreate(request.user)})
