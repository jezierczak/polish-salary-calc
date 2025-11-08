from decimal import Decimal
from pathlib import Path

import pandas as pd

# SalaryDict = dict[str, str | Decimal | bool]
SummaryDict = dict[str, dict[str, str | Decimal | bool]]

class SalaryExporter:

    @staticmethod
    def to_string( input_data:  SummaryDict) -> str:
        # print(len(input_data))
        # print(len(input_data.keys()))
        # print(input_data)
        # if len(input_data) != 13 or not [str(k).isupper() for k in input_data.keys()][0]:
        if len(input_data.keys()) <= 1:
            return SalaryExporter.print_dict(input_data)
        else:
            return str(SalaryExporter.get_data_frame(input_data, columns = [
            "salary_gross", "social_insurance_sum", "cost", "health_insurance", "tax_advance_payment",
            "net_salary", "employer_pension_contribution", "employer_disability_contribution",
            "accident_insurance", "fp", "fgsp", "total_employer_cost"]))

    @staticmethod
    def get_data_frame(input_data: SummaryDict,rows: list[str] | None = None,columns: list[str] | None = None) -> pd.DataFrame:
        # output:dict[str,Salary] ={}
        # if isinstance(self,Salary):

        # else: output[self.get_contract_type()] =self
        if rows is not None:
            input_data = {k:v for k,v in input_data.items() if k in rows}
        # if len(input_data) != 13 or not [str(k).isupper() for k in input_data.keys()][0]:
        #     return SalaryExporter._generate_data_frame_from_salary_dict(input_data, columns)
        # else:
        return SalaryExporter._generate_data_frame_from_contract_summary(input_data, columns)

    @staticmethod
    def to_excel(input_data: SummaryDict, path: Path):
        first_items = list(input_data.items())[0][0] #or {'contract_type':"None"}
        # print('-------------------------')
        # print(first_items)
        return SalaryExporter.get_data_frame(input_data).to_excel(path,sheet_name=first_items)

    @staticmethod
    def to_json(input_data: SummaryDict, path: Path):
        return SalaryExporter.get_data_frame(input_data).to_json(path, indent=4, index=True,orient="index")

    @staticmethod
    def to_csv(input_data: SummaryDict, path: Path):
        return SalaryExporter.get_data_frame(input_data).to_csv(path,sep=";", index=True)


    @staticmethod
    def _generate_data_frame_from_contract_summary(contract_summary_dict: dict[str, dict[str, str | Decimal | bool]], columns: list | None = None
                                              ) -> pd.DataFrame:

        first_key = list(contract_summary_dict.keys())[0]
        # print(list(contract_summary_dict.values()))
        if columns is None:
            columns = list(contract_summary_dict.get(first_key).keys())
        data = list(contract_summary_dict.values())
        index = list(contract_summary_dict.keys())

        df = pd.DataFrame(data,
                        index=index,
                        columns=columns
                        )
        return df

    @staticmethod
    def print_dict(input_dict: dict) -> str:
        first_key = list(input_dict.keys())[0]
        out = [first_key]
        max_len = 0
        for key, value in input_dict.get(first_key).items():
            if isinstance(value,tuple):
                value = "  ".join(str(v) for v in value)
            max_len = max(max_len, len(key)+len(str(value)))

        for key, value in input_dict.get(first_key).items():
            if isinstance(value,tuple):
                value =" ".join(str(v) for v in value)
                value = "("+value+")"
            key = key.upper().replace("_", " ")

            # print(key,max_len)
            out.append(f"{key}{"":.>{max_len-len(key)-len(str(value))+2}}{str(value)}")
        return "\n".join(out)