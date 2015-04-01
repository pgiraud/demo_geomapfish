# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from c2cgeoportal import locale_negotiator, add_interface, INTERFACE_TYPE_SENCHA_TOUCH
from c2cgeoportal.lib.authentication import create_authentication
from demo.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        root_factory=Root, settings=settings,
        locale_negotiator=locale_negotiator,
        authentication_policy=create_authentication(settings)
    )

    config.include('c2cgeoportal')

    config.add_translation_dirs('demo:locale/')

    # scan view decorator for adding routes
    config.scan()

    add_interface(config)
    add_interface(config, 'edit')
    add_interface(config, 'routing')
    add_interface(config, 'mobile', INTERFACE_TYPE_SENCHA_TOUCH)

    config.add_route('file_proxy', '/file_proxy/{layer}/{file}')

    return config.make_wsgi_app()
