from decimal import Decimal


class SalaryUtilities:
    @staticmethod
    def calculate_pension_or_disability_insurance(
            pension_or_disability_insurance_rate: Decimal,
            social_security_base: Decimal,
            social_security_base_sum: Decimal,
            social_insurance_cap:  Decimal
    ) -> Decimal:
        total_social_security_base_sum = social_security_base_sum + social_security_base
        if total_social_security_base_sum <= social_insurance_cap:
            return social_security_base *pension_or_disability_insurance_rate
        elif total_social_security_base_sum - social_security_base > social_insurance_cap:
            return Decimal('0.0')
        else:
            return (social_security_base - (total_social_security_base_sum - social_insurance_cap))*pension_or_disability_insurance_rate

    @staticmethod
    def calculate_author_rights_cost(
            income_tax_deduction: Decimal,
            cost_fifty_ratio: Decimal,
            base: Decimal,
            cost_fifty_sum: Decimal,
            cost_threshold: Decimal
        )-> Decimal:
        #if cost_fifty_ratio>0:
        cost_fifty = income_tax_deduction * base * cost_fifty_ratio
        total_cost_fifty_sum  = cost_fifty_sum +  cost_fifty
        if total_cost_fifty_sum <= cost_threshold:
            return cost_fifty
        elif total_cost_fifty_sum - cost_fifty <= cost_threshold:
            return cost_threshold - total_cost_fifty_sum -  cost_fifty
        else:
            return Decimal('0.0')
    #else: return Decimal('0.0')
