import itertools
import json
import sys

import curio
import gidgethub.httpx
import httpx


with open("pull_requests.graphql", "r", encoding="utf-8") as file:
    PR_QUERY = file.read()


with open("pr_files.graphql", "r", encoding="utf-8") as file:
    FILES_QUERY = file.read()


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks."
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    # From itertools docs.
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


async def changed_files(gh, pr_id, paths):
    """Append file paths for the changed PR to `paths`."""
    has_more_files = True
    cursor = None
    while has_more_files:
        result = await gh.graphql(FILES_QUERY, node=pr_id, cursor=cursor)
        pr_node = result["node"]
        files_node = pr_node["files"]
        has_more_files = files_node["pageInfo"]["hasNextPage"]
        for path_edge in files_node["edges"]:
            cursor = path_edge["cursor"]
            paths.append(path_edge["node"]["path"])


async def main():
    oauth_token = sys.argv[1]
    async with httpx.AsyncClient(timeout=None) as client:
        gh = gidgethub.httpx.GitHubAPI(client, "brettcannon/stdlib-stats",
                                       oauth_token=oauth_token)
        pr_ids = []
        has_more_prs = True
        cursor = None
        print("Getting PR IDs ...", end="", flush=True)
        while has_more_prs:
            result = await gh.graphql(PR_QUERY, cursor=cursor)
            pull_requests = result["repository"]["pullRequests"]
            has_more_prs = pull_requests["pageInfo"]["hasNextPage"]
            for pr in pull_requests["edges"]:
                # Will naturally end on the appropriate cursor for the next query.
                cursor = pr["cursor"]
                pr_node = pr["node"]
                pr_number = pr_node["number"]
                pr_id = pr_node["id"]
                pr_ids.append((pr_number, pr_id))
        print(len(pr_ids), "PRs found")

        pr_to_files = {}
        for pr_chunk in grouper(pr_ids, 10):
            async with curio.TaskGroup() as g:
                for pr_number, pr_id in pr_chunk:
                    files = []
                    pr_to_files[pr_number] = files
                    await g.spawn(changed_files, gh, pr_id, files)
            print(".", end="", flush=True)

        with open("pull_requests.json", "w", encoding="utf-8") as file:
            json.dump(pr_to_files, file)


if  __name__ == "__main__":
    curio.run(main)
