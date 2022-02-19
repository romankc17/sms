from rest_framework.views import exception_handler


# customize validation check function
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print(response.data)
        # check if the type is class list or not
    #     if not type(response.data) is list:
    #         data_copy = response.data.copy()
    #         for key in response.data:
    #             response.data.pop(key)
            
    #         response.data['data']=data_copy
    #         response.data['status'] = 'error'
    #         response.data['message'] = "Validations failed"

    return response

