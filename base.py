import datetime
import requests
import info


class Days():
    today = datetime.date.today()
    day = today.day
    tomorrow = today + datetime.timedelta(days=1)
    next_week_day = today + datetime.timedelta(days=7)
    month = today.month
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
    month_name = months[month - 1]

    if today.year >= 2024 and (today.month == 1 and today.day == 8):  # хардкод для изменения меню 8 января
        today_str = "2024-01-08"
        today_day = "8 января"
        tomorrow_str = "2024-01-08"
        tomorrow_day = "8 января"
        next_week_day_str = "2024-01-08"
        next_week_day_day = "8 января"

    elif today.year >= 2024 and (today.month == 1 and today.day >= 1):  # хардкод для установки 8 января последним днем
        today_str = today.strftime('%Y-%m-%d')
        today_day = f"{day} {month_name}"
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        tomorrow_day = f"{tomorrow.day} {months[tomorrow.month - 1]}"
        next_week_day_str = "2024-01-08"
        next_week_day_day = "8 января"

    else:
        """Сегодня"""
        today_str = today.strftime('%Y-%m-%d')
        today_day = f"{day} {month_name}"

        """Завтра"""
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        tomorrow_day = f"{tomorrow.day} {months[tomorrow.month - 1]}"

        """На неделе"""
        next_week_day_str = next_week_day.strftime('%Y-%m-%d')
        next_week_day_day = f"{next_week_day.day} {months[next_week_day.month - 1]}"


class DataFetcherCategory:
    def __init__(self, api_parameter):
        self.api = 'https://first-api-link.com?code='
        self.api_parameter = api_parameter

    def fetch_data(self):
        try:
            r = requests.get(self.api + self.api_parameter)
            data = r.json()
            results = []
            count = 0
            for item in data:
                if item["activity"]:
                    result = {
                        "Название": item["title"],
                        "Ссылка": item["link"]
                    }
                    results.append(result)
                    count += 1
            return results, None
        except requests.exceptions.RequestException as e:
            error_message = info.category_empty_message
            return None, error_message


class DataFetcherAfisha:
    def __init__(self, date_end, date_start, day_start, day_end):
        self.day_start = day_start
        self.day_end = day_end
        self.date_start = date_start
        self.date_end = date_end
        self.api = f'https://second-api-link.com/?start_date={date_start}&end_date={date_end}'

    def fetch_data(self):
        try:
            r = requests.get(self.api)
            data = r.json()
            results = []
            count = 0
            for card in data["cards"]:
                for event in card["value"]:
                    if not event["value"]["daily"]:
                        result = {
                            "Категория": event["value"]["category"][0],
                            "Название": event["value"]["title"],
                            "Ссылка": event["value"]["detail_url"] + "&?utm_source=tg-bot",
                            "Дата_начала": event["value"]["date"]["date"]["start_date"],
                            "Дата_окончания": event["value"]["date"]["date"]["end_date"]
                        }
                        results.append(result)
                        count += 1
                        if count >= 10:
                            break
                if count >= 10:
                    break
            if self.day_start == self.day_end:
                date_range = self.day_start
            else:
                date_range = f"{self.day_start} - {self.day_end}"
            return date_range, results, None
        except requests.exceptions.HTTPError as e:
            error_message = info.afisha_empty_message
            return None, None, error_message
        except requests.exceptions.RequestException as e:
            error_message = info.afisha_empty_message
            return None, None, error_message
