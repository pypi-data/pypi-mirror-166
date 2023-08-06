def SegmentMiddleware(get_response):

    def middleware(request):
        tracked = True

        if request.user.is_authenticated == True:
            if request.user.is_staff == True:
                tracked = False
                
        else:
            session = request.session
            # if request.session['ano']

        request.segment_tracking = tracked

        response = get_response(request)
        print(session.keys())
        return response

    return middleware