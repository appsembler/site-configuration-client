"""
Mocks for openedx.core.djangoapps.plugins.constants.

Mocks to make the plugin app works during tests
without being concerned to actually test the plugin configs.
"""

from mock import Mock

# Minimal mocks to reduce test maintenance costs.
SettingsType = Mock()
PluginSignals = Mock()
PluginURLs = Mock()
PluginSettings = Mock()
