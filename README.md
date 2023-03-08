## hnterminal

`pip install hnterminal`

HN browser in terminal.

Built on top of [HN API](https://github.com/HackerNews/API) and [replbuilder](https://github.com/Aperocky/replbuilder)

TODO: Add login, commenting ability

## Usage

Texts are highlighted, terminal behavior is *responsive* and adjust to your terminal width.

```
$ hnterminal

hnterminal > ls
List of available commands:
Read
    get_front_page    Get the front page of Hacker News
    get_story         Get story by pointer shown
    get_comments      Get comments by pointer, works with both stories and comments
Cache
    get_cache         See stored item count and call count
    clear_cache       Remove all cache

hnterminal > get_front_page -n 5
POINTER| AUTHOR                   | SCORE | COMMENT | AGE        | BASE URL
1      | ChatGPT Explained: A normie's guide to how it works
       | hui-zheng                | 130   | 43      | 3 hours    | www.jonstokes.com
2      | Hardware microphone disconnect (2021)
       | janniks                  | 594   | 328     | 10 hours   | support.apple.com
3      | Zero energy ready homes are coming
       | ricardou                 | 145   | 253     | 5 hours    | www.energy.gov
4      | The Grind a Day: thousands of Apple II floppy disks archived
       | pabs3                    | 50    | 8       | 2 days     | ascii.textfiles.com
5      | The decline of net neutrality activism
       | neelc                    | 27    | 9       | 2 hours    | neelc.org

hnterminal > get_comments 5
PARENT STORY
The decline of net neutrality activism
2023-03-07 18:26:57
AUTHOR: neelc
FULL URL: https://neelc.org/posts/net-neutrality-activism/
POINTER/AUTHOR      | COMMENTS
1                   | I feel like the USA is focusing on the wrong thing with net neutrality.
p1necone            | The core problem is that individual ISPs have total monopolies on
                    | infrastructure (or at least on the better infrastructure) in a lot of
                    | areas, and so can do all the anti consumer bullshit they want without
                    | repercussions.
                    | Enforcing net neutrality is just treating a symptom of the monopoly.
                    | Other countries fix this by having the shared physical infrastructure
                    | controlled by a government entity that rents access to any company that
                    | wants to sell service as an ISP.

2                         | I’d advise not saying “the USA” in conversations like this, but
Uehreka                   | being more specific and saying “US activists” or “US policymakers”.
                          | The former are probably who you are referring to, the latter are
                          | who people are generally referring to when they say “the USA” in
                          | international policy discussions, but US policymakers are deeply
                          | divided on this issue and most either don’t have a strong opinion
                          | or are actually against net neutrality.
... more ...
