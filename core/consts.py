from enum import StrEnum


class Colors(StrEnum):
    BLUE = '#4A90E2'
    WHITE = '#FFFFFF'
    ALMOSTBLACK = '#2C3E50'
    BLUEGREEN = '#50E3C2'
    SALAD = '#B8E986'
    ORANGE = '#F5A623'
    RED = '#D0021B'
    YELLOW = '#F8E71C'
    BLACKYELLOW = '#FFC107'


class ProjectStatus:
    OPEN = 'open'
    CLOSED = 'closed'

    CHOICES = (
        (OPEN, 'Открыт'),
        (CLOSED, 'Закрыт'),
    )


COLORSCHEME = (
    (Colors.BLUE, Colors.WHITE),
    (Colors.BLUEGREEN, Colors.ALMOSTBLACK),
    (Colors.SALAD, Colors.ALMOSTBLACK),
    (Colors.ORANGE, Colors.WHITE),
    (Colors.RED, Colors.WHITE),
    (Colors.YELLOW, Colors.ALMOSTBLACK),
    (Colors.BLACKYELLOW, Colors.ALMOSTBLACK)
)

IMAGESIZE = (200, 200)

FONTSIZE = 100

UPOFFSET = 10

WINDOWSFONTPATH = 'C:\\Windows\\Fonts\\'

OTHERFONTSPATH = '/usr/share/fonts/truetype/'

FONTPATH = [
    f'{WINDOWSFONTPATH}Arial.ttf',
    f'{WINDOWSFONTPATH}arial.ttf',
    f'{WINDOWSFONTPATH}segoeui.ttf',
    f'{OTHERFONTSPATH}dejavu/DejaVuSans.ttf',
    f'{OTHERFONTSPATH}truetype/liberation/LiberationSans-Regular.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
    '/Library/Fonts/Arial.ttf',
]

USERLISTPAGINATENUM = 12

PASSWORDMINIMUMLENGTH = 8

PHONEMAXLENGTH = 12

ABOUTMAXLENGTH = 256

NAMEMAXLENGTH = 124

SURNAMEMAXLENGTH = 124

MAXPROJECTNAMELENGTH = 200

MAXPROJECTSTATUSLENGTH = 6

PROJECTLISTPAGINATENUM = 12

FILTER_CHOICES = (
    ('owners-of-favorite-projects', 'Авторы избранных проектов'),
    ('owners-of-participating-projects',
     'Авторы проектов, в которых я участвую'),
    ('interested-in-my-projects',
     'Пользователи, которым нравятся мои проекты'),
    ('participants-of-my-projects', 'Участники моих проектов')
)
