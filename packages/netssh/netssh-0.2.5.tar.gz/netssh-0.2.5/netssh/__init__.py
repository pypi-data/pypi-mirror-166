from extras.plugins import PluginConfig

class netssh(PluginConfig):
    name = 'netssh'
    verbose_name = 'NetBox WebSSH'
    description = '-'
    version = '0.0.1'
    author = 'Max'
    author_email = 'expample@gmail.com'
    base_url = 'netssh'
    required_settings = []
    default_settings = {}
    caching_config = {
        '*': None
    }

config = netssh