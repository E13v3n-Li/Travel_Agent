from .weather import get_weather
from .poi import search_attraction
from .plan import go_plan

def get_all_tools():
    return [get_weather, search_attraction, go_plan]