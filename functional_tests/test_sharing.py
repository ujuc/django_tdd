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

        # 오니가 해당 목록에 접속한다.
        self.browser = oni_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        #그는 에디스의 목록을 확인한다.
        self.browser.find_element_by_link_text('도움 요청').click()

        # 리스트 페이지에서 해당 목록이 에디스 것임을 확인한다
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'edith@example.com'
        ))

        # 해당 리스트에 작업 아이템을 추가한다
        list_page.add_new_item('안녕 에디스!')

        # 에디스가 페이지를 새로고침하면 오니가 추가한 것을 볼 수 있다.
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('안녕 에디스', 2)
