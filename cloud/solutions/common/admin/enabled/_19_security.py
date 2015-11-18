# The name of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'security'

# If set to True, this dashboard will not be added to the settings.
DISABLED = True

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.security',
]