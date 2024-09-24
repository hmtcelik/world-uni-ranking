import requests
import pandas as pd

ENDPOINT = (
    "https://www.topuniversities.com/rankings/endpoint?nid=3990755&items_per_page=15"
)
LIMIT = 500
data = []
page = 0


def fetch_data(page):
    url = f"{ENDPOINT}&page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def process_data(page=0):
    global data

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
        process_data(page + 1)


if __name__ == "__main__":
    process_data()
    df = pd.DataFrame(data)
    df.to_csv("./data/university_rankings.csv", index=False)
