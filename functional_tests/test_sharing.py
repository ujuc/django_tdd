# -*- coding:utf-8 -*-

from selenium import webdriver
from .base import FunctionalTest
from .home_and_list_pages import HomePage

def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # 에디스가 사용자로 로그인한다.
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # 그녀의 친구인 오니도 목록 사이트를 보고 있다.
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # 에디스는 메인 페이지를 방문해서 목록 작성을 시작한다.
        self.browser = edith_browser
        list_page = HomePage(self).start_new_list('도움 요청')

        # '이 목록 공유' 옵션을 발견한다.
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # 리스트를 공유한다.
        # 오니와 공유했다는 것을 표시하기위해 페이지 갱신
        list_page.share_list_with('oniciferous@example.com')
