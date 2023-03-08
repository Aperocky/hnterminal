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

hnterminal > get_comments 2
PARENT STORY
Hardware microphone disconnect (2021)
2023-03-07 10:28:29
AUTHOR: janniks
FULL URL: https://support.apple.com/guide/security/hardware-microphone-disconnect-secbbd20b00b/web
POINTER/AUTHOR      | COMMENTS
1                   | They have this feature but closing the lid on a MacBook or even putting
lovehashbrowns      | it to sleep allows Bluetooth devices to stay connected. Heck, a MacBook
                    | even while in sleep mode will connect to Bluetooth devices. As far as I
                    | can see, this requires a third-party app to fix. Can an application
                    | still use the microphone on a Bluetooth device that’s connected?

2                         | This has to be the most annoying thing in MacOS. My laptop, soundly
dvirsky                   | sleeping in my backpack, takes over my bluetooth headphones all the
                          | time.

3                               | Similarly, whenever I'm working at my kitchen table I always
cj                              | "lose" my mouse as if there's another monitor connected.
... more ...
