def convert_timestr_to_sec(time_str: str) -> int:
    match time_str:
        case time_str if time_str.endswith('s'):
            return int(time_str[:-1])
        case time_str if time_str.endswith('m'):
            return int(time_str[:-1]) * 60
        case time_str if time_str.endswith('h'):
            return int(time_str[:-1]) * 60 * 60
        case time_str if time_str.endswith('d'):
            return int(time_str[:-1]) * 60 * 60 * 24
        case time_str if time_str.endswith('w'):
            return int(time_str[:-1]) * 60 * 60 * 24 * 7
        case time_str if time_str.endswith('y'):
            return int(time_str[:-1]) * 60 * 60 * 24 * 7 * 365
        case _:
            raise ValueError(f'Invalid time string {time_str}')
