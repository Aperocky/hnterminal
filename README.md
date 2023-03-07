## hnterminal

`pip install hnterminal`

HN in terminal.

## Usage

```
$ hnterminal

hnterminal > help
List of available commands:
Read
    get_front_page    Get the front page of Hacker News
    get_story         Get story by pointer shown
    get_comments      Get comments by pointer, works with both stories and comments

hnterminal > get_front_page
POINTER| TITLE                                                                            | SCORE | COMMENT | AGE        | BASE URL
1      | Retail, search and Amazon’s $40B ‘advertising’ business                          | 103   | 42      | 2 hours    | www.ben-evans.com
2      | Reliability: It’s not great                                                      | 908   | 325     | 13 hours   | community.fly.io
3      | Discord, or the Death of Lore                                                    | 223   | 137     | 4 hours    | ascii.textfiles.com
4      | Qualcomm wants to replace eSIMs with iSIMs, has the first certified SoC          | 13    | 4       | 2 days     | arstechnica.com
.. more records ..

hnterminal > get_comments -p 2
POINTER/AUTHOR      | COMMENTS
1                   | Fundamentally I think some of the problems come down to the difference between what Fly set out to build and what the market currently want.
samwillis           | Fly (to my understanding) at its core is about <i>edge</i> compute. That is where they started and what the team are most excited about developing. It's a brilliant
                    | idea, they have the skills and expertise. They are going to be successful at it.
                    | However, at the same time the market is looking for a successor to Heroku. A zero dev ops PAAS with instant deployment, dirt simple managed Postgres, generous free
                    | level of service, lower cost as you scale, and a few regions around the world. That isn't what Fly set out to do... exactly, but is sort of the market they find
                    | themselves in when Heroku then basically told its low value customers to go away.
                    | It's that slight miss alignment of strategy and market fit that results in maybe decisions being made that benefit the original vision, but not necessarily the
                    | immediate influx of customers.
                    | I don't envy the stress the Fly team are under, but what an exciting set of problems they are trying to solve, I do envy that!

2                         | There's a wonderfully blunt saying that applies here (too): you are not in the business you think you are, you are in the business your customers think you are.
bostik                    | If you offer data volumes, the <i>low water mark</i> is how EBS behaves. If you offer a really simple way to spin up Postgres databases, you are implicitly
                          | promising a fully managed experience.
                          | And $deity forbid, if you want global CRUD with read-your-own-writes semantics, the yardstick people measure you against is Google's Spanner.

3                               | Where does the misalignment between what the customer thinks they want, and what they actually want fit in to your philosophy? Google Spanner is a great
zamnos                          | example of this because who <i>doesn't</i> want instantaneous global  writes? It's just that, y'know, there's a ton of businesses, especially smaller ones,
                                | that don't actually need that. The smarter customers realize this themselves, and can judge the premium they'd pay for Spanner over something far less
                                | complex. What I'm getting to is that sales is a critical company function to bridge the gap between what customers want, and what customers actually need,
                                | and for you to make money.
                                | The first releases of EBS weren't very good and took a while to get to where we are. Some places still avoid using EBS due to bad experience back in 2011
                                | when it was first released.
.. more records ..
