from decimal import Decimal


from polish_salary_calc.contract_settings.mandate_contract_settings import (
    MandateContractSettings,
    MandateContractType,
)
from polish_salary_calc.contract_settings.work_contract_settings import (
    WorkContractSettings,
    WorkContractType,
)
from polish_salary_calc.contract_settings.self_employment_settings import (
    SelfEmploymentSettings,
    SelfEmploymentType,
    TaxType,
    HealthBase,
)
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contracts.base_contract import SalaryType
from polish_salary_calc.contract_settings.employment_contract_settings import (
    EmploymentContractSettings,
)

from polish_salary_calc.summary.contract_summary import YearContractSummary, Months


def main() -> None:
    # --------------1----------
    # create Rates() object with actual polish indicators, default rates are actual the months of feb.2025 and jan.2026
    # to update nesesery rate type rates['rate-name'] = Decimal("rate-value")
    # all values in salary_calculator must be provided in Decimal type

    rates = Rates()

    # --------------2----------
    # the next step is to set up desired contract settings:

    # for employment contract set EmploymentContractSettings - you can do it either with builder or dict,
    # each setting has a predefined default values

    employment_settings = (
        EmploymentContractSettings()
        .SettingsBuilder()
        .is_increased_costs(True)
        .is_active_business(False)
        .is_under_26(False)
        .
        # set_name("NAME CHANGED").
        # set_employee_ppk(Decimal("0.02")).
        # set_employer_ppk(Decimal("0.015")).
        is_fp_fgsp(True)
        .build()
    )

    # for mandated contract set MandateContractSettings

    mandate_settings = (
        MandateContractSettings()
        .SettingsBuilder()
        .set_mandate_contract_type(MandateContractType.COMMON)
        .is_fifty(False)
        .is_fp(True)
        .is_fgsp(True)
        .build()
    )

    # for work contract set WorkContractSettings

    work_settings = (
        WorkContractSettings()
        .SettingsBuilder()
        .is_a_lump_sum(False)
        .set_work_contract_type(WorkContractType.COMMON)
        .build()
    )

    # for self employment set SelfEmploymentSettings

    self_employment_settings = (
        SelfEmploymentSettings()
        .SettingsBuilder()
        .set_self_employment_type(SelfEmploymentType.COMMON)
        .set_sick_pay(True)
        .set_tax_type(TaxType.A_LUMP_SUM)
        .set_tax_lump_rate(Decimal("0.055"))
        .set_health_base(HealthBase.NONE)
        .set_costs(Decimal("0.0"))
        .set_tax_base_sum(Decimal("0.0"))
        .set_name("Samozatrudnienie")
        .build()
    )

    # --------------3----------
    # After setting options make desired contract:
    # and make calculations with .calculate(salary_value, salary_type)
    # salary_value - desired salary amount
    # salary type (SalaryType.GROSS is default) - SalaryType.GROSS or SalaryType.NET - shows which base is delivered salary_value

    # setting up employment contract with rates, and employment settings, salary NET set to 7000, calculations made
    employment_contract = EmploymentContract(rates, employment_settings)
    employment_contract.calculate(Decimal("7000"), SalaryType.NET)

    # setting up mandated contract with rates, and employment settings, salary gross set to 7000, calculations made
    mandate_contract = MandateContract(rates, mandate_settings)
    mandate_contract.calculate(Decimal("7000"), SalaryType.GROSS)

    # setting up work contract with rates, and employment settings, salary gross (default) set to 7000, calculations made
    work_contract = WorkContract(rates, work_settings)
    work_contract.calculate(Decimal("7000"))

    # setting up self-employment with rates, and employment settings, a salary net set to 7000, calculations made
    self_employment = SelfEmployment(rates, self_employment_settings)
    self_employment.calculate(Decimal("7000"), SalaryType.NET)

    # to print output just write print(self_employment)
    print(
        "---------------------------------------- [1 - simple calculations] -------------------------------"
    )
    print(self_employment)  # change this to other contracts to see output

    # you can also set year contract summary with desired options:
    # in this case, use YearContractSummary(default_rates, contract_settings, salary_value, salary_type):

    # for rates, employment_contract, net salary value set to 8000 write bottom code and make calculations:
    year_employment_contract = YearContractSummary(
        rates, employment_settings, Decimal("7000"), SalaryType.NET
    )
    # or you can initiate YearSummary from contract:
    # year_employment_contract = YearContractSummary.from_contract(self_employment)
    year_employment_contract.calculate()

    # to write output just write print:
    print(
        "---------------------------------------- [2 - year calculations] --------------------------------"
    )
    print(year_employment_contract)

    # you can change default data to other with modify_month_contracts method
    year_employment_contract.modify_month_contracts(
        [Months.MAR, Months.DEC], rates=rates, salary_base=Decimal("2100")
    )

    # to disable months type enabled=False
    year_employment_contract.modify_month_contracts(
        [Months.APR, Months.AUG], enabled=False
    )

    # after making modifications always make calculate method
    year_employment_contract.calculate()

    print(
        "---------------------------------------- [3 - modifying particular months] ----------------------"
    )
    print(year_employment_contract)

    # it is possible to compare 2 contracts:
    print(
        "---------------------------------------- [4 - comparing] ----------------------------------------"
    )
    print(year_employment_contract["MAR"].compare_to(year_employment_contract["MAY"]))

    print(
        "---------------------------------------- [5 - comparing] ----------------------------------------"
    )
    print(self_employment.compare_to(year_employment_contract["MAY"]))

    # it is possible to export gathered data to_dict, to_excel file to_csv file and to_json file or get pandas dataframe:
    # employment_data_frame = year_employment_contract.get_data_frame()
    # year_employment_contract.to_excel(Path('Output.xlsx'))
    # year_employment_contract["SUMMARY"].to_csv(Path('Output.xlsx'))
    # year_employment_contract["JAN"].to_json(Path('Output.xlsx'))

    # single contract also can be exported:
    # employment_contract.to_excel(Path('Single.xlsx'))
    # ...
    # if comparison is made, you can export and print compared details
    print(
        "---------------------------------------- [6 - compared data] ----------------------------------------"
    )
    print(self_employment.to_compared_string())


# or export
# self_employment.to_compared_excel()

# rates and settings also can be printed or exported:
# rates.to_csv(Path('rates.csv'))
# employment_contract.get_options().to_json(Path('settings.json') )
# print(rates)
# print(employment_contract.get_options())

if __name__ == "__main__":
    main()
