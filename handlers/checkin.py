from handlers.base import AppHandler



class CheckIn(AppHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = self.request.cookies.get('visits','0')
        if visits.isdigit():
            visits = int(visits) + 1
        else:
            visits = 0
        if visits > 10:
            self.write('Wow! You\'ve been here a lot. You may need to get a different hobby')
        else:
            self.write('You have visited %s times' %visits)
        self.response.headers.add_header('Set-Cookie', 'visits=%s' %visits)
