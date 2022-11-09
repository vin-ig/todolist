from pytest_factoryboy import register

import tests.factories

register(tests.factories.UserFactory)
register(tests.factories.BoardFactory)
register(tests.factories.GoalCategoryFactory)
register(tests.factories.GoalFactory)

# pytest_plugins = 'tests.fixtures'
