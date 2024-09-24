import requests
import pandas as pd

ENDPOINT = (
    "https://www.topuniversities.com/rankings/endpoint?nid=3990755&items_per_page=15"
)
LIMIT = 500


def fetch_data(page):
    url = f"{ENDPOINT}&page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def process_data(data=None, page=0):
    if data is None:
        data = []

    for node in fetch_data(page)["score_nodes"]:
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


if __name__ == "__main__":
    data = process_data()
    df = pd.DataFrame(data)
    df.to_csv("./data/university_rankings.csv", index=False)
