import os

from shared import COMMIT_MESSAGES
from steal import StealModule
from git_commands import Git

MANIFESTS = [
    StealModule("fagram", "https://raw.githubusercontent.com/fagramdesktop/fagram-scoop/refs/heads/main/fagram.json")
]


def main():
    # TODO: async
    git = Git()
    for manifest in MANIFESTS:
        # TODO: actual logging needed LOL
        print(f"Checking {manifest} for updates")
        if manifest.check_update():
            print(f"Found update for {manifest} ({manifest.state})")
            manifest.update()
            assert manifest.state is not None
            commit_msg = COMMIT_MESSAGES[manifest.state].format(name=manifest.name, curver=manifest.curver, newver=manifest.newver)
            git.add_n_commit(manifest.manifest_path, commit_msg=commit_msg)
        else:
            print(f"No updates for {manifest} found")


if __name__ == "__main__":
    main()
