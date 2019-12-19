import random
from django import template

register = template.Library()

@register.simple_tag
def random_image():
    random_num = random.randint(1, 4)
    if random_num == 1:
        return "{% static 'flare/images/character-one-archive.jpg' %}"
    elif random_num == 2:
        return "{% static 'flare/images/character-two-archive.jpg' %}"
    elif random_num == 3:
        return "{% static 'flare/images/character-three-archive.jpg' %}"
    else:
        return "{% static 'flare/images/character-four-archive.jpg' %}"
