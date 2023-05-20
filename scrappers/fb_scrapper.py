import argparse
import logging
import pandas as pd
from facebook_scraper import get_posts

logging.basicConfig(filename='fb_scrapper.log', encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook scrapper')
    parser.add_argument('--groups_csv', type=str, help='Path to csv file with Facebook group names')
    parser.add_argument('--output', type=str, help='Path to output file')
    args = parser.parse_args()

    # groups_path = args.groups_csv
    groups_path = '../data/facebook_job_groups.csv'
    # output_path = args.output
    output_path = '../data/facebook_job_posts.json'

    logging.info(f'Config: groups_csv={groups_path}, output={output_path}')

    df_fb_groups = pd.read_csv(groups_path)
    logging.info(f'Loaded {len(df_fb_groups)} groups')

    posts = []
    for group in df_fb_groups['group_name']:
        try:
            for post in get_posts(group):
                posts.append(post)
                logging.info(f'Added post from group {group}')
        except:
            logging.error(f'Error while scrapping group {group}')
    logging.info(f'Scrapped {len(posts)} posts')

    df_posts = pd.DataFrame(posts)
    if output_path.endswith('.csv'):
        df_posts.to_csv('../data/facebook_job_posts.csv', index=False)
    elif output_path.endswith('.json'):
        with open('../data/facebook_job_posts.json', 'w', encoding='utf-8') as f:
            df_posts.to_json(f, force_ascii=False, orient='records')
    else:
        logging.error(f'Unknown output format {output_path}')

    logging.info('Done')
