def test_schedule_page_loads(schedule_page):
    """TC-UI-01: Страница расписания загружается"""
    schedule_page.open()
    assert "teachers.skyeng.ru" in schedule_page.get_current_url()
    assert "login" not in schedule_page.get_current_url()


def test_schedule_tab_is_visible(schedule_page):
    """TC-UI-02: Вкладка «Расписание» отображается"""
    assert schedule_page.is_schedule_tab_visible()


def test_create_lesson_button_is_visible(schedule_page):
    """TC-UI-03: Элементы управления расписанием отображаются"""
    assert schedule_page.are_buttons_visible()
    assert schedule_page.is_week_label_visible()
    assert schedule_page.is_day_label_visible()


def test_week_view_is_available(schedule_page):
    """TC-UI-04: Отображение дней недели в расписании"""
    assert schedule_page.has_day_of_week()


def test_page_has_no_critical_errors(schedule_page):
    """TC-UI-05: На странице нет критических ошибок"""
    assert schedule_page.has_no_errors()
