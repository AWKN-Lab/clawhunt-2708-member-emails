# -*- coding: utf-8 -*-
"""ClawHunt #2708 样品测试：5 条验收标准逐条对照，外加内容完整性检查。

只用虚构测试数据。期望值按平台 AC 原文与任务描述手写，不调被测函数算。
"""

from __future__ import annotations

import re

from src.emails import (
    EMAIL_DEFS,
    EMAIL_KEYS,
    TEXT_FOOTER,
    render_footer,
    render_header,
    render_html,
    render_text,
    subject_table,
    variable_table,
)
from src.fixtures import (
    FICTIONAL_COMPANY,
    FICTIONAL_RECIPIENT,
    FORBIDDEN_PLAINTEXT_PASSWORD,
)

PHONE_RE = re.compile(r"1[3-9]\d{9}|\d{3,4}-\d{7,8}|\d{7,}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

ALL_HTML = {key: render_html(key) for key in EMAIL_KEYS}
ALL_TEXT = {key: render_text(key) for key in EMAIL_KEYS}
ALL_RENDERED = {**ALL_HTML, **ALL_TEXT}


# ---- AC1：4 封邮件都有 HTML 与纯文本两个版本，并使用同一套页眉页脚组件 ----


def test_all_four_have_html_and_text():
    assert EMAIL_KEYS == [
        "announcement",
        "activation_invite",
        "staff_onboarding",
        "activation_reminder",
    ]
    for key in EMAIL_KEYS:
        assert len(ALL_HTML[key]) > 200, key
        assert len(ALL_TEXT[key]) > 100, key
        assert ALL_HTML[key].startswith("<table")
        assert ALL_TEXT[key].startswith("会员空间平台")


def test_shared_header_footer_html_identical():
    header = render_header()
    footer = render_footer()
    for key in EMAIL_KEYS:
        assert ALL_HTML[key].startswith(header), key
        assert ALL_HTML[key].endswith(footer), key
    assert "会员空间平台" in header
    assert "本邮件由系统自动发送，请勿直接回复" in footer


def test_shared_footer_text_identical():
    for key in EMAIL_KEYS:
        assert ALL_TEXT[key].endswith(TEXT_FOOTER), key
    assert "会员空间平台 · 本邮件由系统自动发送，请勿直接回复。" in TEXT_FOOTER


def test_html_single_column_600px_table_inline_css():
    for key in EMAIL_KEYS:
        html = ALL_HTML[key]
        assert 'width="600"' in html, key
        assert "<table" in html, key
        assert "style=" in html, key
        assert "max-width:600px" in html, key


def test_each_html_has_title_heading():
    for key in EMAIL_KEYS:
        assert "<h1" in ALL_HTML[key], key
        assert EMAIL_DEFS[key]["subject"] in ALL_HTML[key] or key == "staff_onboarding", key


# ---- AC2：每封都有不超过 25 字的主题行及 2 个备选、不超过 40 字的预览文本 ----


def test_subject_length_all():
    for row in subject_table():
        assert len(row["subject"]) <= 25, (row["key"], row["subject"])
        assert len(row["subject"]) >= 5, (row["key"], row["subject"])
        for alt in row["alternates"]:
            assert len(alt) <= 25, (row["key"], alt)


def test_subject_alternates_count():
    for row in subject_table():
        assert len(row["alternates"]) == 2, row["key"]
        assert len({row["subject"], *row["alternates"]}) == 3, row["key"]


def test_preview_length_all():
    for row in subject_table():
        assert len(row["preview"]) <= 40, (row["key"], row["preview"])
        assert len(row["preview"]) >= 5, (row["key"], row["preview"])


def test_subject_preview_exact_lengths_documented():
    expected = {
        "announcement": (10, 16),
        "activation_invite": (9, 18),
        "staff_onboarding": (10, 18),
        "activation_reminder": (10, 18),
    }
    for row in subject_table():
        subject_len, preview_len = expected[row["key"]]
        assert len(row["subject"]) == subject_len, row
        assert len(row["preview"]) == preview_len, row


# ---- AC3：员工开通通知中不出现密码明文，只有设置密码链接变量 ----


def test_staff_no_plaintext_password():
    html = ALL_HTML["staff_onboarding"]
    text = ALL_TEXT["staff_onboarding"]
    assert FORBIDDEN_PLAINTEXT_PASSWORD not in html
    assert FORBIDDEN_PLAINTEXT_PASSWORD not in text
    assert "初始密码" not in html
    assert "初始密码" not in text
    assert "您的密码是" not in html
    assert "您的密码是" not in text


def test_staff_has_set_password_variable():
    assert "{{set_password_url}}" in ALL_HTML["staff_onboarding"]
    assert "{{set_password_url}}" in ALL_TEXT["staff_onboarding"]
    assert "设置登录密码" in ALL_HTML["staff_onboarding"]


def test_staff_no_password_value_patterns():
    combined = ALL_HTML["staff_onboarding"] + ALL_TEXT["staff_onboarding"]
    assert not re.search(r"密码[：:]\s*[A-Za-z0-9]", combined)
    assert not re.search(r"密码为\s*\S+", combined)


def test_staff_first_login_steps_present():
    for needle in ["第一步", "第二步", "第三步", "{{staff_login_account}}", "{{training_url}}"]:
        assert needle in ALL_HTML["staff_onboarding"], needle
        assert needle in ALL_TEXT["staff_onboarding"], needle


# ---- AC4：激活邀请写明链接 72 小时有效与过期后的处理方式 ----


def test_activation_invite_states_72h_validity():
    assert "72 小时内有效" in ALL_HTML["activation_invite"]
    assert "72 小时内有效" in ALL_TEXT["activation_invite"]


def test_activation_invite_expiry_handling():
    for needle in ["如果链接过期", "重新发送激活链接", "重新开通"]:
        assert needle in ALL_HTML["activation_invite"], needle
        assert needle in ALL_TEXT["activation_invite"], needle


def test_activation_invite_has_activation_url_variable():
    assert "{{activation_url}}" in ALL_HTML["activation_invite"]
    assert "{{activation_url}}" in ALL_TEXT["activation_invite"]


# ---- AC5：示例收件人与企业均为虚构，邮件中没有真实电话或邮箱地址 ----


def test_no_real_phone_numbers():
    for key, rendered in ALL_RENDERED.items():
        assert not PHONE_RE.search(rendered), key


def test_no_real_email_addresses():
    for key, rendered in ALL_RENDERED.items():
        assert not EMAIL_RE.search(rendered), key
        assert "@" not in rendered, key


def test_fictional_recipients_only():
    for key in EMAIL_KEYS:
        assert FICTIONAL_RECIPIENT in ALL_HTML[key], key
        assert FICTIONAL_COMPANY in ALL_HTML[key] or key == "staff_onboarding", key
        assert FICTIONAL_RECIPIENT in ALL_TEXT[key], key
    assert "张三（虚构）" == FICTIONAL_RECIPIENT
    assert "示例科技有限公司" == FICTIONAL_COMPANY


# ---- 内容完整性：上线公告、激活提醒、变量与触发条件 ----


def test_announcement_three_features():
    html = ALL_HTML["announcement"]
    for feature in ["资源对接", "知识库与 SOP 工作台", "商机流转"]:
        assert feature in html, feature
        assert feature in ALL_TEXT["announcement"], feature


def test_announcement_main_button_text():
    assert "查看会员权益" in ALL_HTML["announcement"]
    assert "{{member_portal_url}}" in ALL_HTML["announcement"]
    assert "查看会员权益" in ALL_TEXT["announcement"]


def test_announcement_qr_placeholder_and_steps():
    for needle in ["[二维码图片位：会员端入口]", "第一步", "第二步", "第三步"]:
        assert needle in ALL_HTML["announcement"], needle
        assert needle in ALL_TEXT["announcement"], needle


def test_reminder_gentle_tone_no_pressure():
    text = ALL_TEXT["activation_reminder"]
    assert "不着急，慢慢来" in text
    assert "随时可办" in text or "什么时候方便都可以办" in text
    for pressure in ["立即激活", "请尽快", "逾期将", "最后通牒", "否则将"]:
        assert pressure not in text, pressure
        assert pressure not in ALL_HTML["activation_reminder"], pressure


def test_each_email_has_variables_triggers_timing():
    for row in variable_table():
        assert len(row["variables"]) >= 3, row["key"]
        assert row["trigger"], row["key"]
        assert row["timing"], row["key"]
        for variable in row["variables"]:
            assert variable.startswith("{{") and variable.endswith("}}"), variable


def test_subject_and_variable_tables_cover_all_four():
    assert [row["key"] for row in subject_table()] == EMAIL_KEYS
    assert [row["key"] for row in variable_table()] == EMAIL_KEYS


def test_text_versions_mirror_html_key_content():
    assert "72 小时内有效" in ALL_TEXT["activation_invite"]
    assert "设置您的登录密码" in ALL_TEXT["staff_onboarding"]
    assert "会员空间平台正式上线" in ALL_TEXT["announcement"]
    assert "提醒：会员账号待激活" in ALL_TEXT["activation_reminder"]
