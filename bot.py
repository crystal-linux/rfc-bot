from github import Github

g = Github(open(".access_token").read().strip())

repo = g.get_repo('crystal-linux/.github')

core_team = g.get_organization('crystal-linux').get_team_by_slug('core-team')
core_team_members = core_team.get_members()
core_team_logins = []

for member in core_team_members:
    core_team_logins.append(member.login)

for issue in repo.get_issues():
    if 'RFC' in issue.title:
        print(f"Working on: {issue.title}")
        all_reactions = issue.get_reactions()
        if all_reactions.totalCount != 0:
            total_votes_for = 0
            total_votes_against = 0
            for reaction in all_reactions:
                if reaction.user.login in core_team_logins:
                    #print(f"- {reaction.content}: by {reaction.user.login}")
                    if reaction.content == "+1":
                        total_votes_for += 1
                    elif reaction.content == "-1":
                        total_votes_against += 1
            print(f"Total votes for resolution: {str(total_votes_for)}")
            print(f"Total votes against resolution: {str(total_votes_against)}")
            if (total_votes_for/len(core_team_logins)) > 0.5:
                print("This RFC should be passed. Adding comment.")
                issue.create_comment("This resolution has enough votes from Core Team mebers to be considered passed. Please close the issue once appropriate actions have been taken. - Beep Boop (I'm a bot, and this action was performed automatically)")
                issue.lock("resolved")
            else:
                print("Not enough votes to pass")