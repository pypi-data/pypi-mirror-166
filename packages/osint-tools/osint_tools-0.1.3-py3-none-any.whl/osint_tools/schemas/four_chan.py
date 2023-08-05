from .base import *


# string Enum with 4chan board name (e.g. 'wg', 'v', 'b', 'pol', 's', 'h', 'c', 'e', 'int', 'g', 'k', 'o', 'u', 'vg', 'r9k', 's4s', 'cm', 'hm', 'lgbt', 'sci', 'wsg', 'adv', 'an', 'out', 'trv', 'sp', 'soc', 'fit', 'biz', 'fa', 'int', 'pol', 's4s', 'tg', 'w', 'wg', 'wsg', 'x')
class Board(str, Enum):
    wg = 'wg'
    v = 'v'
    b = 'b'
    pol = 'pol'
    s = 's'
    h = 'h'
    c = 'c'
    e = 'e'
    int = 'int'
    g = 'g'
    k = 'k'
    o = 'o'
    u = 'u'
    vg = 'vg'
    r9k = 'r9k'
    s4s = 's4s'
    cm = 'cm'
    hm = 'hm'
    lgbt = 'lgbt'
    sci = 'sci'
    wsg = 'wsg'
    adv = 'adv'
    an = 'an'
    out = 'out'
    trv = 'trv'
    sp = 'sp'
    soc = 'soc'
    fit = 'fit'
    biz = 'biz'
    fa = 'fa'
    tg = 'tg'
    w = 'w'
    x = 'x'



class CatalogBase(BaseModel):
    no: int = Field(None, description="always | The numeric post ID | any positive integer")
    resto: int = Field(None, description="always | For replies: this is the ID of the thread being replied to. For OP: this value is zero |`0` or `Any positive integer")
    sticky: int = Field(None, description="OP only, if thread is currently stickied | If the thread is being pinned to the top of the page| `1` or not set")
    closed: int = Field(None, description="OP only, if thread is currently closed | If the thread is closed to replies | `1` or not set")
    now: str = Field(None, description="always | MM/DD/YY(Day)HH:MM (:SS on some boards), EST/EDT timezone | `string")
    time: int = Field(None, description="always | UNIX timestamp the post was created | UNIX timestamp")
    name: str = Field(None, description="always | Name user posted with. Defaults to Anonymous | any string")
    trip: str = Field(None, description="if post has tripcode | The users tripcode, in format: !tripcode or !!securetripcode| any string")
    id: str = Field(None, description="if post has ID | posters ID | any 8 chars")

    capcode: str = Field(None, description="if post has capcode | The capcode identifier for a post | Not set, mod, admin, admin_highlight, manager, developer, founder")

    country: str = Field(None, description="if country flags are enabled | Posters [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 | 2 character string or XX if unknown")
    country_name: str = Field(None, description="if country flags are enabled | Posters country name | Name of any country")

    sub: str = Field(None, description="OP only, if subject was included| OP Subject text | any string")

    com: str = Field(None, description="if comment was included | Comment (HTML escaped) | any HTML escaped string")

    tim: int = Field(None, description="always if post has attachment | Unix timestamp + microtime that an image was uploaded | integer")
    filename: str = Field(None, description="always if post has attachment | Filename as it appeared on the poster's device | any string")
    ext: str = Field(None, description="always if post has attachment | Filetype | jpg, png, gif, pdf, swf, webm")
    fsize: int = Field(None, description="always if post has attachment | Size of uploaded file in bytes | any integer")
    md5: str = Field(None, description="always if post has attachment | 24 character, packed base64 MD5 hash of file")
    w: int = Field(None, description="always if post has attachment | Image width dimension | `any integer")
    h: int = Field(None, description="always if post has attachment | Image height dimension | `any integer")
    tn_w: int = Field(None, description="always if post has attachment | Thumbnail image width dimension | any integer")
    tn_h: int = Field(None, description="always if post has attachment | Thumbnail image height dimension | any integer")
    filedeleted: int = Field(None, description="if post had attachment and attachment is deleted | If the file was deleted from the post | `1` or not set")
    spoiler: int = Field(None, description="if post has attachment and attachment is spoilered | If the image was spoilered or not | `1` or not set")
    custom_spoiler: int = Field(None, description="if post has attachment and attachment is spoilered | The custom spoiler ID for a spoilered image | `1-10` or not set |")
    omitted_posts: int = Field(None, description="OP only| Number of replies minus the number of previewed replies | `any integer` |")
    omitted_images: int = Field(None, description="OP only| Number of image replies minus the number of previewed image replies | `any integer` |")
    replies: int = Field(None, description="OP only | Total number of replies to a thread | any integer")
    images: int = Field(None, description="OP only | Total number of image replies to a thread | any integer")
    bumplimit: int = Field(None, description="OP only, only if bump limit has been reached | If a thread has reached bumplimit, it will no longer bump | `1` or not set |")
    imagelimit: int = Field(None, description="OP only, only if image limit has been reached | If an image has reached image limit, no more image replies can be made  | `1` or not set |")
    last_modified: int = Field(None, description="OP only | UNIX timestamp marking last time thread was modified post | added/modified/deleted, thread closed/sticky settings modified | `UNIX Timestamp")
    tag: str = Field(None, description="OP only, /f/ only | The category of `.swf` upload |`Game`, `Loop`, etc")
    semantic_url: str = Field(None, description="OP only | SEO URL slug for thread | `string` |")
    since4pass: int = Field(None, description="if poster put 'since4pass' in the options field` | Year 4chan pass bought | `any 4 digit year`")
    unique_ips: int = Field(None, description="OP only | Number of unique posters in a thread | any integer")
    m_img: int = Field(None, description="any post that has a mobile-optimized image` | Mobile optimized image exists for post | 1 or not set")

class CatalogThread(CatalogBase):
    '''
    Helps us keep code DRY
    - Do not
    - Repeat
    - Yourself
    '''
    last_replies: List[CatalogBase] = []# catalog OP only | JSON representation of the most recent replies to a thread | array of JSON post objects")
