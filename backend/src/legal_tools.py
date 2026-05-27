from datetime import datetime


def calculate_contract_penalty(contract_value: float, penalty_rate: float, days_late: int) -> dict:
    penalty = contract_value * penalty_rate * days_late
    return {
        "contract_value": contract_value,
        "penalty_rate_per_day": penalty_rate,
        "days_late": days_late,
        "penalty_amount": penalty,
    }



def check_legal_age(birth_year: int, current_year: int | None = None) -> dict:
    current_year = current_year or datetime.now().year
    age = current_year - birth_year
    return {
        "birth_year": birth_year,
        "current_year": current_year,
        "age": age,
        "is_18_plus": age >= 18,
    }



def calculate_inheritance_shares(num_children: int, spouse: bool = True, parents: int = 0) -> dict:
    heirs = num_children + parents + (1 if spouse else 0)
    if heirs <= 0:
        return {"error": "Không có người thừa kế hàng thứ nhất trong mô hình đơn giản này."}
    share = round(1 / heirs, 4)
    return {"total_heirs": heirs, "share_per_heir": share}
