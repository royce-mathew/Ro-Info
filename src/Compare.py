
def compare_val(list: list, index: int):
        # Check Date is different
        try:
            first_tuple = list[-1]
            second_tuple = list[-index]

            if first_tuple[0] == second_tuple[0]:
                return None; # Don't allow comparisons for same date 

            return (first_tuple[1] - second_tuple[1], first_tuple[0], second_tuple[0])
        except Exception as err:
            print(err)
            return None;

def get_comparisons(json_data: dict, index: int=0) -> dict:
    main_dict: dict = {}
    for name, value in json_data.items(): 
        main_dict[name] = calculate_chart_point(value, index)
    return main_dict;

def calculate_chart_point(user_list: dict, index: int) -> None:
    chart_points: float = 0.0;
    point_tuple: tuple = (0, "", "");

    for key, value in user_list.items():
        if (unsafe_tuple := compare_val(value, index)) is None:
            print("Cannot compare on same date")
            continue;

        point_tuple = unsafe_tuple;
        points = point_tuple[0];
        match key:
            case "followers":
                chart_points += points / 2
            case "place_visits":
                chart_points += points / 50
            case "members":
                chart_points += points / 4;
            case _:
                raise Exception(f"Unknown Key found: {key}")      
    return chart_points, *point_tuple[1:];