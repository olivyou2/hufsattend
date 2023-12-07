from account import account
from attendlib import attendlib

account_id = "202302931"
account_password = "50e534d558d698b8dd3d47157983b21b390780cdc87d189f40362d2d712323d1cbae54b6fcde0da0442962daeb86c2122b5bc251402897e064d050d85e3e6460"

account_instance = account(account_id, account_password)
lssns = account_instance.getLssns(2023, 3)

lssn = lssns.get_by_lssn_cd("F05108601")
print(lssn.subject)

chk, attd_data = attendlib.checkAttendance(lssn)
print(chk, attd_data)