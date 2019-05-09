from urllib.parse import quote

import requests

# For better integration scenarios, cosider using the full library
# https://github.com/halcy/Mastodon.py

"""
Simple tryout program for connecting to mastodon (norden.social) via the public HTTP API.
"""


class Toot:
    def __init__(self, json_data):
        self.id = json_data['id']
        self.content = json_data['content']
        self.tags = []
        for tag in json_data['tags']:
            self.tags.append('#' + tag['name'])

    def get_id(self):
        return self.id

    def get_content(self):
        return self.content

    def get_tags(self):
        return self.tags


# Based on
# https://stackoverflow.com/a/6386366/1143126
def main():
    tag = "potsdam"
    json_data = retrieve_latest_json_data_for_tag(tag)
    toots = json_data_to_toots_list(json_data)
    for toot in toots:
        render_toot(toot)


def retrieve_latest_json_data_for_tag(tag):
    base_url = "https://norden.social/api/v1/timelines/tag/"
    request_url = base_url + encode_for_url(tag)
    request_params = dict(
    )
    resp = requests.get(url=request_url, params=request_params)
    data = resp.json()
    return data


def encode_for_url(tag):
    return quote(tag)


def json_data_to_toots_list(json_data):
    result = []
    for toot_json in json_data:
        result.append(Toot(toot_json))
    return result


def render_toot(toot):
    print("{}: \n"
          "\t{}\n"
          "\t\t{}\n".format(toot.get_id(), toot.get_content(), ' '.join(toot.get_tags())))


if __name__ == "__main__":
    main()
