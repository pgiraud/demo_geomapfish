# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from c2cgeoportal import locale_negotiator
from c2cgeoportal.resources import FAModels, defaultgroupsfinder
from c2cgeoportal.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authentication_policy = AuthTktAuthenticationPolicy(
            settings.get('authtkt_secret'),
            callback=defaultgroupsfinder,
            cookie_name=settings.get('authtkt_cookie_name'))
    config = Configurator(root_factory=Root, settings=settings,
            locale_negotiator=locale_negotiator, 
            authentication_policy=authentication_policy)

    config.add_settings({'srid': 900913})

    config.include('c2cgeoportal')

    config.add_translation_dirs('c2cgeoportal:locale/')

    config.formalchemy_admin('admin', package='c2cgeoportal',
            view='fa.jquery.pyramid.ModelView', factory=FAModels)

    config.add_route('checker_all', '/checker_all')

    # scan view decorator for adding routes
    config.scan()

    # add the main static view
    config.add_static_view('proj', 'c2cgeoportal:static')

    # mobile views and routes
    config.add_route('mobile_index_dev', '/mobile_dev/')
    config.add_view('c2cgeoportal.views.mobile.index',
                    renderer='c2cgeoportal:static/mobile/index.html',
                    route_name='mobile_index_dev')
    config.add_route('mobile_config_dev', '/mobile_dev/config.js')
    config.add_view('c2cgeoportal.views.mobile.config',
                    renderer='c2cgeoportal:static/mobile/config.js',
                    route_name='mobile_config_dev')
    config.add_static_view('mobile_dev', 'c2cgeoportal:static/mobile')

    config.add_route('mobile_index_prod', '/mobile/')
    config.add_view('c2cgeoportal.views.mobile.index',
                    renderer='c2cgeoportal:static/mobile/build/production/index.html',
                    route_name='mobile_index_prod')
    config.add_route('mobile_config_prod', '/mobile/config.js')
    config.add_view('c2cgeoportal.views.mobile.config',
                    renderer='c2cgeoportal:static/mobile/build/production/config.js',
                    route_name='mobile_config_prod')
    config.add_static_view('mobile', 'c2cgeoportal:static/mobile/build/production')

    return config.make_wsgi_app()
