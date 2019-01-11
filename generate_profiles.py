#!/usr/bin/env python3

import json
from pathlib import Path

from jinja2 import Template
from slugify import slugify

# some awful hackery that needs to be done:
# in statistics/background.json, south and north korea are
# "korea-north" and "korea-south". So we manually rename them
# with sed. This is terrible

COMMITTEES_DIR=Path('committees')
PROFILES_FILE=Path('profiles.json')
PROFILE_TEMPLATE=Template(open('profile.html.tmpl', 'r').read())
STATS_SRC_DIR=Path('by-statistic')
OUTPUT_DIR="_generated"


def load_selected_statistics(statistics):
    """Load from disk factstrape statistics specified in the argument."""

    stats = {}
    for stat in statistics:
        with (STATS_SRC_DIR / (stat + '.json')).open('r') as f:
            stats[stat] = json.loads(f.read())

    return stats
        
def load_committee_statistics():
    # { name: [ chosen_statistics ] }
    committees = {}
    for c in COMMITTEES_DIR.iterdir():
        committees[c.name] = c.open().read().strip().split('\n')

    return committees


def load_profiles():
    # structure is { committee: { country: { issues, quotes, policies } } }
    with PROFILES_FILE.open('r') as f:
        return json.loads(f.read())
    

def render_template(context):
    committee = context['committee']
    country = context['country']

    result_path = Path(OUTPUT_DIR) / committee 
    result_path.mkdir(parents=True, exist_ok=True)

    with (result_path / (country + ".html")).open('w') as f:
        f.write(PROFILE_TEMPLATE.render(**context))
    
def main():

    # each committee has list of associated statistics
    committee_statistics = load_committee_statistics()
    all_statistics = load_selected_statistics(
        set(
            stat for c_stat in committee_statistics.values()
            for stat in c_stat
        ) | { 'background' }
    )
    
    profiles_data = load_profiles()

    for committee, countries in profiles_data.items():
        for country in countries:
            issues = countries[country]['issues']
            policies = countries[country]['policies']
            quotes = countries[country]['quotes']

            country_statistics = []

            if committee in committee_statistics:
                for stat in committee_statistics[committee]:
                    if stat in all_statistics and \
                       country in all_statistics[stat]:
                        country_statistics.append(
                            (stat, all_statistics[stat][country])
                        )

            context = {
                'committee': committee,
                'country': country,
                'background_text': all_statistics['background'][country],
                'issues_text': issues,
                'policies_text': policies,
                'quotes': quotes,
                'country_statistics': country_statistics,
            }
            print("rendering template for {} - {}".format(committee, country))
            render_template(context)

            
        

    
    

    
    

if __name__=='__main__':
    main()
