# -*- coding:utf-8 -*-

from selenium import webdriver
from .base import FunctionalTest

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

        # 에디스는 메인 페이지를 방문한다.
        self.browser = edith_browser
        self.browser.get(self.server_url)
        self.get_item_inpu_box().send_keys('도움 요청\n')

        # '이 목록 공유' 옵션을 발견한다.
        share_box = self.browser.find_element_by_css_selector('inpu[name=email]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
            )
