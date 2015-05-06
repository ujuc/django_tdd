from django.conf import settings
from djnago.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model

User = get_user_model()

from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## 쿠키를 설정하기 위해 도매인 접속이 필요하다.
        ## 404 페이지가 뜬다
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # 에디스가 사용자로 로그인한다
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
