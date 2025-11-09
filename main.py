from pathlib import Path

from polish_salary_calc.contract_settings.mandate_contract_settings import MandateContractSettings, MandateContractType
from polish_salary_calc.contract_settings.work_contract_settings import WorkContractSettings, WorkContractType

from polish_salary_calc.contract_settings.self_employment_settings import SelfEmploymentSettings, SelfEmploymentType, TaxType, \
    HealthBase
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contracts.base_contract import SalaryType

from polish_salary_calc.contract_settings.employment_contract_settings import EmploymentContractSettings

from decimal import Decimal

from polish_salary_calc.summary.contract_summary import YearContractService, Months


def main() -> None:
    rates = Rates()
    path2 = Path("./data")
    path2.mkdir(parents=True, exist_ok=True)
    # print(rates.to_json(path2 / "rates.json"))

    employment_options = (EmploymentContractSettings().builder().
                          is_increased_costs(True).
                          is_active_business(False).
                          is_under_26(False).
                          # set_name("NAME CHANGED").
                          # set_employee_ppk(Decimal("0.02")).
                          # set_employer_ppk(Decimal("0.015")).
                          is_fp_fgsp(True).
                          build())
    # print(employment_options)
    # salary = EmploymentContract(rates,employment_options)
    # salary.calculate(Decimal('10000'), SalaryType.GROSS)

    # print(rates)
    # print(employment_options)
    # print(salary)

    # printer = ConsolePrinter(salary)
    # print(printer.print_rates())
    # print(printer.print_options())
    # print(printer.print_contract())

    # print(salary.get_rates())
    # print(salary.get_options())
    # for k,i in salary.to_dict().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary.net_ratio}')
    # print(f'Total markups: {salary.total_markups}')
    # print(f'Total markups ratio: {salary.total_markups_ratio}')

    # print('--------------------Zlecenie----------------------------')

    mandate_options = (MandateContractSettings().builder().
                       set_mandate_contract_type(MandateContractType.COMMON).
                       is_fifty(False).
                       is_fp(True).
                       is_fgsp(True).
                       build())
    #
    # salary2 = MandateContract(rates, mandate_options)
    # # salary.update_options(employment_options)
    # salary2.calculate(Decimal('2000'), SalaryType.GROSS)
    #
    # print(salary2.get_rates())
    # print(salary2.get_options())
    # for k, i in salary2.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary2.net_ratio}')
    # print(f'Total markups: {salary2.total_markups}')
    # print(f'Total markups ratio: {salary2.total_markups_ratio}')
    #
    # print('--------------------O dzieło----------------------------')
    #
    work_options = (WorkContractSettings().builder().
                    is_a_lump_sum(False).
                    set_work_contract_type(WorkContractType.COMMON).
                    build())
    salary3 = WorkContract(rates, work_options)
    salary3.calculate(Decimal('8000'), SalaryType.NET)

    # print(salary3.get_rates())
    # print(salary3.get_options())
    # for k, i in salary3.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary3.net_ratio}')
    # print(f'Total markups: {salary3.total_markups}')
    # print(f'Total markups ratio: {salary34.total_markups_ratio}')
    # #
    # print('--------------------Działalność----------------------------')
    #
    self_employment_options = (SelfEmploymentSettings().
                                builder().
                                set_self_employment_type(SelfEmploymentType.COMMON).
                                set_sick_pay(True).
                                set_tax_type(TaxType.A_LUMP_SUM).
                                set_tax_lump_rate(Decimal('0.055')).
                                set_health_base(HealthBase.NONE).
                                set_costs(Decimal('0.0')).
                                set_tax_base_sum(Decimal('0.0')).
                                set_name("Umowa nr 193").
                                build())
    # salary4 = SelfEmployment(rates, self_employment_options)
    # salary4.calculate(Decimal('10000'), SalaryType.GROSS)
    # # print(salary4)
    # print(salary4)
    # print(salary4)
    #
    # # print(salary4.get_rates())
    # # print(salary4.get_options())
    # for k, i in salary4.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary4.net_ratio}')
    # print(f'Total markups: {salary4.total_markups}')
    # print(f'Total markups ratio: {salary4.total_markups_ratio}')

    # contract_service = ContractServic(rates)
    # contract_service.add_contract(All,salary4)
    # contract_service.show()
    # contract_service.export(EXCCEL,"mojasymulacja.xcl", clean=True)
    print("---------Porównanie umów----------")
    # yc = YearContractService(rates,employment_options,Decimal("12000"),SalaryType.NET)
    # yc.calculate()
    # print(yc.get_data_frame(rows=["summary"]))
    # yc2 = YearContractService(rates,mandate_options,Decimal("12000"),SalaryType.NET)
    # yc2.calculate()
    # print(yc2.get_data_frame(rows=["summary"]))
    # yc3 = YearContractService(rates, work_options, Decimal("12000"),SalaryType.NET)
    # yc3.calculate()
    # print(yc3.get_data_frame(rows=["summary"]))
    yc4 = YearContractService(rates, employment_options, Decimal("8000"),SalaryType.NET)
    # yc4.modify_month_contracts([Months.APR,Months.MAY],salary_base= Decimal("12000"))
    # yc4.modify_month_contracts([Months.JAN,], salary_base=Decimal("0"), enabled=False)



    path = Path("./data")
    path.mkdir(parents=True, exist_ok=True)
    yc4.calculate()

    print(salary3.compare_to(yc4["JUL"]))

    # print(yc4.compare_to(yc4))


    # print(yc4.to_excel(path / 'salary8000.xlsx'))
    # yc4.all_to_json(path / "salary4.json")
    # print(yc4.to_csv(path / "plik1.csv"))
    # print(yc4['JUL'].to_csv(path / "plik2.csv"))
    # print(yc4.all_to_csv(path / "plik3.csv"))
    # yc4["JUN"].to_excel(path / "Plik462.xlsx")
    # yc4.to_excel(path / "Plik42.xlsx")
    # yc4.all_to_excel(path / "Plik442.xlsx")

    # print(yc4)


    # print(yc4["JAN"])
    # yc4["APR"].to_csv(path / "APR.csv")
    # yc4["APR"].to_excel(path / "EXcel.xls")
    # yc4["APR"].to_json(path / "Json.json")

    # yc4["APR"].get_data_frame().to_excel(path / "output.xlsx",sheet_name=yc4.name)
    # yc4.get_data_frame().to_json(path / "output.json",indent=4, index=True,orient="index")
    # yc4.get_data_frame().to_csv(path / "output.csv", sep=";", index=True)
    #
    # print(yc4.monthly_contract_calculated_data.get(Months.JAN))

    # df =pandas.DataFrame([salary.to_dict() for salary in yc.monthly_contract_calculated_data.values()],
    #                      index=[k.value for k in yc.monthly_contract_calculated_data.keys()],
    #                      columns=list(yc.monthly_contract_calculated_data[Months.JAN].to_dict().keys()))
    # print(list(yc.monthly_contract_calculated_data[Months.JAN].to_dict().keys()))

    # print({month:salary.to_dict() for month,salary in yc.monthly_contract_calculated_data.items()})

    # print(yc.monthly_contract_calculated_data[Months.DEC].tax_base_total)
    # suma = Decimal("0")
    # for month in Months:
    #     print(yc.monthly_contract_calculated_data[month].social_security_base)
    #     print(yc.monthly_contract_calculated_data[month].social_security_base_total)
    #
    #     suma+=yc.monthly_contract_calculated_data[month].social_security_base
    # print(suma == yc.summary.social_security_base)
    # print("------------------------")
    # print(yc.summary)
    # print(yc.summary.social_security_base_total)
if __name__ == '__main__':
    main()