from django.shortcuts import redirect


def group_check(view_func):
    def wrapper_func(self, *args, **kwargs):
        # print(request)
        print()
        department = "none"
        for group in self.request.user.groups.all():
            # print(group.name)
            if 'dep_' in group.name:
                department = group.name[4:]
                print(department)
                break
        return view_func(self, department, *args, **kwargs)
    
    return wrapper_func

