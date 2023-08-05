from decimal import Decimal

from kih_api.global_common import Currency
from kih_api.wise.models import IntraAccountTransfer, ReserveAccount, ProfileTypes, CashAccount

monthly_expenses_reserve_account: ReserveAccount = ReserveAccount.get_reserve_account_by_profile_type_currency_and_name(ProfileTypes.PERSONAL, Currency.NZD, "Monthly Expenses", False)
nzd_account: CashAccount = CashAccount.get_by_profile_type_and_currency(ProfileTypes.PERSONAL, Currency.NZD)
test = IntraAccountTransfer.execute(Decimal("50"), monthly_expenses_reserve_account, nzd_account, ProfileTypes.PERSONAL)
pass