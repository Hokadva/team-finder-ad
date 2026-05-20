COLORSCHEME = (
    ('#4A90E2', '#FFFFFF'),
    ('#50E3C2', '#2C3E50'),
    ('#B8E986', '#2C3E50'),
    ('#F5A623', '#FFFFFF'),
    ('#D0021B', '#FFFFFF'),
    ('#F8E71C', '#2C3E50'),
    ('#FFC107', '#2C3E50')
)

IMAGESIZE = (200, 200)

FONTSIZE = 100

STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
)

UPOFFSET = 10

FONTPATH = [
        'C:\\Windows\\Fonts\\Arial.ttf',
        'C:\\Windows\\Fonts\\arial.ttf',
        'C:\\Windows\\Fonts\\segoeui.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/Library/Fonts/Arial.ttf',
]

FILTER_CHOICES = (
        ('owners-of-favorite-projects', 'Авторы избранных проектов'),
        ('owners-of-participating-projects',
         'Авторы проектов, в которых я участвую'),
        ('interested-in-my-projects',
         'Пользователи, которым нравятся мои проекты'),
        ('participants-of-my-projects', 'Участники моих проектов')
    )
