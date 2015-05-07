from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## 쿠기 설정을 위해서 도메인 접속이 필요하다.
        ## 404 페이지가 뜬다
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # 에디스가 사용자로 로그인한다
        self.create_pre_authenticated_session('edith@example.com')

        # 메인 페이지로 가서 목록 입력을 시작한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('그물 만들기\n')
        self.get_item_input_box().send_keys('쇼핑 하기\n')
        first_list_url = self.browser.current_url

        # 첫 번째 아이템을 위한 "나의 목록" 링크를 발견한다
        self.browser.find_element_by_link_text('나의 목록').click()

        # 그녀가 만든 목록에 첫 번째 아이템이 있는 것을 확인한다
        self.browser.find_element_by_link_text('그물 만들기').click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # 다른 목록도 확인하기도 한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('게임하기\n')
        second_list_url = self.browser.current_url

        # "나의 목록" 아래에 새로운 목록이 표시된다
        self.browser.find_element_by_link_text('나의 목록').click()
        self.browser.find_element_by_link_text('게임하기').click()
        self.assertEqual(self.browser.current_url, second_list_url)

        # 로그아웃한다. "나의 목록" 옵션이 사라진다
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_element_by_link_text('나의 목록'),
            []
        )
