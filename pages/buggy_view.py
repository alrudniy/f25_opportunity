from django.http import HttpResponse

def buggy_view(request):
    """
    This is a buggy view that will raise a ZeroDivisionError.
    """
    a = 1
    b = 0
    result = a / b
    return HttpResponse(f"This should not be reached. Result: {result}")
