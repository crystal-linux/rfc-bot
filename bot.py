from github import Github
from datetime import datetime

g = Github(open(".access_token").read().strip())


def post_update(text):
    repo = g.get_repo("crystalrfc-bot/status")
    thread = repo.get_issue(1)
    thread.create_comment(f"{text}\nBeep Boop! (I'm a bot, and this action was performed automagically.)\nScan timestamp: `{datetime.now().isoformat()}`")


targets = ["crystal-linux/.github", "crystal-linux-packages/.github"]

status_text = ""

for tgt in targets:
    repo = g.get_repo(tgt)
    status_text += f"# Examining {repo.full_name}\n"

    core_team = g.get_organization("crystal-linux").get_team_by_slug("core-team")
    trusted_contrib = g.get_organization("crystal-linux").get_team_by_slug(
        "trusted-contribututors"
    )
    core_team_members = core_team.get_members()
    trusted_contrib_members = trusted_contrib.get_members()

    crystal_logins = []

    for member in core_team_members:
        crystal_logins.append(member.login)

    for member in trusted_contrib_members:
        crystal_logins.append(member.login)

    rfcs_passed = 0
    for issue in repo.get_issues():
        if "RFC" in issue.title:
            print(f"Working on: {issue.title}")
            all_reactions = issue.get_reactions()
            if all_reactions.totalCount != 0:
                total_votes_for = 0
                total_votes_against = 0
                for reaction in all_reactions:
                    if reaction.user.login in crystal_logins:
                        # print(f"- {reaction.content}: by {reaction.user.login}")
                        if reaction.content == "+1":
                            total_votes_for += 1
                        elif reaction.content == "-1":
                            total_votes_against += 1
                print(f"Total votes for resolution: {str(total_votes_for)}")
                print(f"Total votes against resolution: {str(total_votes_against)}")
                if (total_votes_for / len(crystal_logins)) > 0.5:
                    print("This RFC should be passed. Adding comment.")
                    if not issue.locked:
                        issue.create_comment(
                            "This resolution has enough votes to be considered passed. "
                            "Please close the issue once appropriate actions have been taken. "
                            "- Beep Boop (I'm a bot, and this action was performed automagically)"
                        )
                        issue.lock("resolved")
                    rfcs_passed += 1
                    status_text += f"* Suggested that {issue.title} be acted upon, as it has passed.\n"
                else:
                    print("Not enough votes to pass")

    if rfcs_passed == 0:
        status_text += "No action taken in this repo.\n"

if status_text == "":
    status_text = "Something has gone wrong! No actions were taken at *all*!"

post_update(status_text)
