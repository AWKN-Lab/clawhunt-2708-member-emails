# -*- coding: utf-8 -*-
"""虚构测试数据：只用平台描述里给出的示例收件人与企业。

收件人：张三（虚构）；企业：示例科技有限公司。不写真实电话与邮箱地址，
地址类内容一律用 {{变量}} 占位，由调用方在发送时填入。
"""

from __future__ import annotations

FICTIONAL_RECIPIENT = "张三（虚构）"
FICTIONAL_COMPANY = "示例科技有限公司"

# 变量占位值：仅用于渲染演示，{{...}} 本身不含任何真实地址。
PLACEHOLDER_VALUES = {
    "{{member_name}}": FICTIONAL_RECIPIENT,
    "{{company_name}}": FICTIONAL_COMPANY,
    "{{member_portal_url}}": "{{member_portal_url}}",
    "{{activation_url}}": "{{activation_url}}",
    "{{staff_login_account}}": "{{staff_login_account}}",
    "{{set_password_url}}": "{{set_password_url}}",
    "{{training_url}}": "{{training_url}}",
}

# 员工开通通知里绝不出现的明文密码（测试用它证明模板未泄露密码）。
FORBIDDEN_PLAINTEXT_PASSWORD = "TempPass-0000"
