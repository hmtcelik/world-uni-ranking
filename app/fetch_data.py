import pathlib
import requests
import pandas as pd
import logging

ENDPOINT = (
    "https://www.topuniversities.com/rankings/endpoint?nid=3990755&items_per_page=15"
)
LIMIT = 500


def fetch_page(page):
    url = f"{ENDPOINT}&page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def process_data(data=None, page=0):
    if data is None:
        data = []

    for node in fetch_page(page)["score_nodes"]:
        desired_cols = [
            "rank_display",
            "rank",
            "title",
            "region",
            "country",
            "city",
            "overall_score",
        ]
        base_data = {key: node[key] for key in desired_cols}
        data.append(base_data)

    if len(data) < LIMIT:
        return process_data(data, page + 1)
    return data


def save_data(file_name: str, data: list):
    df = pd.DataFrame(data)
    current_dir = pathlib.Path(__file__).parent
    df.to_csv(current_dir / "data" / file_name, index=False)


if __name__ == "__main__":
    data = process_data()
    save_data("university_rankings.csv", data)
    logging.info("Data fetched and saved successfully")
