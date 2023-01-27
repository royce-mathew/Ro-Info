
def compare_val(list):
        try:
            return list[-1][1] - list[-2][1]
        except Exception as err:
            return None;

def get_comparisons(json_data: dict) -> dict:
    main_dict: dict = {}
    for name, value in json_data.items(): 
        main_dict[name] = calculate_chart_point(value)
    return main_dict;

def calculate_chart_point(user_list: dict) -> None:
    chart_points: float = 0.0;
    for key, value in user_list.items():
        if (points := compare_val(value)) is None:
            print(f"Cannot compare: [key: {key}]; len(list) < required")
            continue;
        
        match key:
            case "followers":
                chart_points += points / 2
            case "place_visits":
                chart_points += points / 50
            case "members":
                chart_points += points / 4;
            case _:
                raise Exception(f"Unknown Key found: {key}")          
    return chart_points;