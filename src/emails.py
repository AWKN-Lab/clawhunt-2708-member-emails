# -*- coding: utf-8 -*-
"""ClawHunt #2708 (S4-BRAND-018) 样品：上线阶段 4 封邮件。

4 封邮件共用同一套页眉页脚组件（render_header / render_footer），每封都
有 HTML 与纯文本两个版本。HTML 按单栏 600 px、表格布局、内联 CSS 实现。
只用虚构测试数据：收件人张三（虚构）、示例科技有限公司；邮件中不出现
真实电话或邮箱地址，地址类内容一律用 {{变量}} 占位。
"""

from __future__ import annotations

BRAND = "会员空间平台"

HEADER_HTML = (
    '<table width="600" cellpadding="0" cellspacing="0" border="0" '
    'style="width:600px;max-width:600px;margin:0 auto;background:#ffffff;'
    'font-family:PingFang SC,Microsoft YaHei,sans-serif;">'
    '<tr><td style="padding:24px 32px 8px 32px;">'
    '<p style="margin:0;font-size:20px;font-weight:bold;color:#1a1a1a;">'
    "会员空间平台</p>"
    '<p style="margin:4px 0 0 0;font-size:13px;color:#666666;">'
    "产业资源连接平台 · 会员服务</p>"
    "</td></tr>"
)

FOOTER_HTML = (
    '<tr><td style="padding:16px 32px 24px 32px;border-top:1px solid #eeeeee;">'
    '<p style="margin:0;font-size:12px;color:#999999;">'
    "会员空间平台 · 本邮件由系统自动发送，请勿直接回复。</p>"
    '<p style="margin:4px 0 0 0;font-size:12px;color:#999999;">'
    "如需帮助，请联系您的会员服务负责人。</p>"
    "</td></tr></table>"
)

TEXT_FOOTER = (
    "\n——\n会员空间平台 · 本邮件由系统自动发送，请勿直接回复。\n"
    "如需帮助，请联系您的会员服务负责人。"
)


def render_header() -> str:
    """共用页眉组件：4 封邮件同一份 HTML。"""
    return HEADER_HTML


def render_footer() -> str:
    """共用页脚组件：4 封邮件同一份 HTML。"""
    return FOOTER_HTML


def _body_cell(inner_html: str) -> str:
    return (
        '<tr><td style="padding:8px 32px 16px 32px;">'
        + inner_html
        + "</td></tr>"
    )


def render_html(email_key: str) -> str:
    """渲染指定邮件的完整 HTML 版本。"""
    body = EMAIL_DEFS[email_key]["html_body"]
    return render_header() + _body_cell(body) + render_footer()


def render_text(email_key: str) -> str:
    """渲染指定邮件的纯文本版本（与 HTML 同一套页眉页脚文案）。"""
    definition = EMAIL_DEFS[email_key]
    header = "会员空间平台\n产业资源连接平台 · 会员服务\n\n"
    return header + definition["text_body"] + TEXT_FOOTER


def subject_table() -> list[dict]:
    """主题行与预览文本表：每封 1 个主题行 + 2 个备选 + 1 条预览文本。"""
    return [
        {
            "key": key,
            "subject": definition["subject"],
            "alternates": list(definition["alternates"]),
            "preview": definition["preview"],
        }
        for key, definition in EMAIL_DEFS.items()
    ]


def variable_table() -> list[dict]:
    """变量与触发条件说明表。"""
    return [
        {
            "key": key,
            "variables": list(definition["variables"]),
            "trigger": definition["trigger"],
            "timing": definition["timing"],
        }
        for key, definition in EMAIL_DEFS.items()
    ]


EMAIL_DEFS: dict[str, dict] = {
    "announcement": {
        "name": "会员上线公告",
        "subject": "会员空间平台正式上线",
        "alternates": ["您的会员空间全新上线", "会员权益已就绪，欢迎回来"],
        "preview": "三大功能上线，会员权益一次看清。",
        "variables": ["{{member_name}}", "{{company_name}}", "{{member_portal_url}}"],
        "trigger": "会员空间平台正式上线时，向全部会员企业发送",
        "timing": "上线当天上午发送一次",
        "html_body": (
            '<h1 style="margin:0 0 12px 0;font-size:18px;color:#1a1a1a;">'
            "会员空间平台正式上线</h1>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "张三（虚构），您好：示例科技有限公司的会员服务已升级。"
            "会员空间平台今天正式上线，对您最有用的三个功能是：</p>"
            '<ol style="margin:0 0 12px 0;padding-left:20px;font-size:14px;line-height:1.8;color:#333333;">'
            "<li>资源对接：发布需求，匹配对口的会员企业与商机。</li>"
            "<li>知识库与 SOP 工作台：常用流程与模板一次找齐。</li>"
            "<li>商机流转：跟进记录集中管理，不再散落在各处。</li>"
            "</ol>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "进入会员端的方式：打开微信扫一扫，扫描下方二维码图片位，"
            "按提示完成三步：第一步打开会员端，第二步确认企业信息，"
            "第三步查看会员权益。</p>"
            '<p style="margin:0 0 12px 0;font-size:14px;color:#666666;">'
            "[二维码图片位：会员端入口]</p>"
            '<p style="margin:0;font-size:14px;">'
            '<a href="{{member_portal_url}}" '
            'style="display:inline-block;padding:12px 24px;background:#1a5cff;'
            'color:#ffffff;text-decoration:none;border-radius:4px;">'
            "查看会员权益</a></p>"
        ),
        "text_body": (
            "会员空间平台正式上线\n\n"
            "张三（虚构），您好：示例科技有限公司的会员服务已升级。"
            "会员空间平台今天正式上线，对您最有用的三个功能是：\n"
            "一、资源对接：发布需求，匹配对口的会员企业与商机。\n"
            "二、知识库与 SOP 工作台：常用流程与模板一次找齐。\n"
            "三、商机流转：跟进记录集中管理，不再散落在各处。\n\n"
            "进入会员端的方式：打开微信扫一扫，扫描二维码图片位，"
            "按提示完成三步：第一步打开会员端，第二步确认企业信息，"
            "第三步查看会员权益。\n\n"
            "[二维码图片位：会员端入口]\n"
            "查看会员权益：{{member_portal_url}}\n"
        ),
    },
    "activation_invite": {
        "name": "会员账号激活邀请",
        "subject": "请激活您的会员账号",
        "alternates": ["您的会员账号已开通", "激活链接已发给您"],
        "preview": "链接72小时内有效，过期可重新获取。",
        "variables": ["{{member_name}}", "{{company_name}}", "{{activation_url}}"],
        "trigger": "为会员企业开通会员账号后，向该企业联系人发送",
        "timing": "账号开通后立即发送",
        "html_body": (
            '<h1 style="margin:0 0 12px 0;font-size:18px;color:#1a1a1a;">'
            "请激活您的会员账号</h1>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "张三（虚构），您好：已为示例科技有限公司开通会员账号。"
            "请点击下方链接完成激活，开始使用会员空间平台。</p>"
            '<p style="margin:0 0 12px 0;font-size:14px;">'
            '<a href="{{activation_url}}" '
            'style="display:inline-block;padding:12px 24px;background:#1a5cff;'
            'color:#ffffff;text-decoration:none;border-radius:4px;">'
            "激活会员账号</a></p>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "激活链接自发送起 72 小时内有效，请在有效期内完成激活。</p>"
            '<p style="margin:0;font-size:14px;line-height:1.8;color:#333333;">'
            "如果链接过期，请点击激活页上的“重新发送激活链接”，"
            "系统会向您重新发送一封新的激活邀请；也可以联系您的会员服务负责人，"
            "由负责人协助重新开通。</p>"
        ),
        "text_body": (
            "请激活您的会员账号\n\n"
            "张三（虚构），您好：已为示例科技有限公司开通会员账号。"
            "请点击下方链接完成激活，开始使用会员空间平台。\n\n"
            "激活链接：{{activation_url}}\n\n"
            "激活链接自发送起 72 小时内有效，请在有效期内完成激活。\n\n"
            "如果链接过期，请点击激活页上的“重新发送激活链接”，"
            "系统会向您重新发送一封新的激活邀请；也可以联系您的会员服务负责人，"
            "由负责人协助重新开通。\n"
        ),
    },
    "staff_onboarding": {
        "name": "员工工作台开通通知",
        "subject": "员工工作台已为您开通",
        "alternates": ["工作台账号开通通知", "首次登录指引已就绪"],
        "preview": "按步骤完成首次登录，培训资料已备好。",
        "variables": [
            "{{member_name}}",
            "{{staff_login_account}}",
            "{{set_password_url}}",
            "{{training_url}}",
        ],
        "trigger": "为员工开通工作台账号后，向该员工发送",
        "timing": "账号开通后立即发送",
        "html_body": (
            '<h1 style="margin:0 0 12px 0;font-size:18px;color:#1a1a1a;">'
            "员工工作台已为您开通</h1>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "张三（虚构），您好：您的工作台账号已开通，"
            "登录账号为 {{staff_login_account}}。</p>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "首次登录步骤：第一步点击下方链接设置您的登录密码，"
            "第二步用登录账号与新密码登录工作台，"
            "第三步完善个人资料并开始使用。</p>"
            '<p style="margin:0 0 12px 0;font-size:14px;">'
            '<a href="{{set_password_url}}" '
            'style="display:inline-block;padding:12px 24px;background:#1a5cff;'
            'color:#ffffff;text-decoration:none;border-radius:4px;">'
            "设置登录密码</a></p>"
            '<p style="margin:0;font-size:14px;line-height:1.8;color:#333333;">'
            "请点击以下链接设置您的登录密码：{{set_password_url}}。"
            "培训资料入口：{{training_url}}，建议首次登录后先看入门培训。</p>"
        ),
        "text_body": (
            "员工工作台已为您开通\n\n"
            "张三（虚构），您好：您的工作台账号已开通，"
            "登录账号为 {{staff_login_account}}。\n\n"
            "首次登录步骤：第一步点击下方链接设置您的登录密码，"
            "第二步用登录账号与新密码登录工作台，"
            "第三步完善个人资料并开始使用。\n\n"
            "请点击以下链接设置您的登录密码：{{set_password_url}}。\n"
            "培训资料入口：{{training_url}}，建议首次登录后先看入门培训。\n"
        ),
    },
    "activation_reminder": {
        "name": "激活提醒",
        "subject": "提醒：会员账号待激活",
        "alternates": ["您的激活链接快过期了", "还没激活？这里有帮助"],
        "preview": "温和提醒：激活只需一分钟，随时可办。",
        "variables": ["{{member_name}}", "{{company_name}}", "{{activation_url}}"],
        "trigger": "会员账号开通 72 小时内仍未激活时发送",
        "timing": "开通后 48 小时未激活发送一次，72 小时到期前再提醒一次",
        "html_body": (
            '<h1 style="margin:0 0 12px 0;font-size:18px;color:#1a1a1a;">'
            "提醒：会员账号待激活</h1>"
            '<p style="margin:0 0 12px 0;font-size:14px;line-height:1.8;color:#333333;">'
            "张三（虚构），您好：示例科技有限公司的会员账号还在等您激活，"
            "顺便提醒您一声。激活只需一分钟，什么时候方便都可以办，"
            "不着急，慢慢来。</p>"
            '<p style="margin:0 0 12px 0;font-size:14px;">'
            '<a href="{{activation_url}}" '
            'style="display:inline-block;padding:12px 24px;background:#1a5cff;'
            'color:#ffffff;text-decoration:none;border-radius:4px;">'
            "激活会员账号</a></p>"
            '<p style="margin:0;font-size:14px;line-height:1.8;color:#333333;">'
            "如果链接已经过期，点击激活页上的“重新发送激活链接”即可重新获取；"
            "如果暂时不需要，也可以先放着，等方便时再激活。</p>"
        ),
        "text_body": (
            "提醒：会员账号待激活\n\n"
            "张三（虚构），您好：示例科技有限公司的会员账号还在等您激活，"
            "顺便提醒您一声。激活只需一分钟，什么时候方便都可以办，"
            "不着急，慢慢来。\n\n"
            "激活链接：{{activation_url}}\n\n"
            "如果链接已经过期，点击激活页上的“重新发送激活链接”即可重新获取；"
            "如果暂时不需要，也可以先放着，等方便时再激活。\n"
        ),
    },
}

EMAIL_KEYS = list(EMAIL_DEFS.keys())
