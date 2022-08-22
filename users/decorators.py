from django.shortcuts import redirect


# Create a basic function for user not authenticated
def user_not_authenticated(function=None, redirect_url='/'):
    """
    :description: The main purpose of this decorator function is check if the user 
    is authenticated or not. If the user is authenticated then we need to redirect
    the user back to specified url. (USuaully Homepage) 

    :param functions: 

    :param redirect_url:
    """

    # Now create another function inside this function called decorator
    def decorator(view_func):
        # and then one more function called _wrapped_view
        def _wrapped_view(request, *args, **kwargs):
            # This will return the user to the homepage if the user is authenticated
            if request.user.is_authenticated:
                return redirect(redirect_url)

            # but if the above check doesn't work, we still need to return something. 
            # in this case it will be the view function
            return  view_func(request, *args, **kwargs)

        return _wrapped_view

    if function: # is not None
        # then return the decorator function that you want to use
        return decorator(function)

    return decorator