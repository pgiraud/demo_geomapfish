Ext.onReady(function() {
    // Ext global settings
    Ext.BLANK_IMAGE_URL = "${request.static_url('demo:static/lib/cgxp/ext/Ext/resources/images/default/s.gif')}";
    Ext.QuickTips.init();

    // OpenLayers global settings
    OpenLayers.Number.thousandsSeparator = ' ';
    OpenLayers.IMAGE_RELOAD_ATTEMPTS = 5;
    OpenLayers.DOTS_PER_INCH = 72;
    OpenLayers.ImgPath = "${request.static_url('demo:static/lib/cgxp/core/src/theme/img/ol/')}";
    OpenLayers.Lang.setCode("${lang}");

    // GeoExt global settings
    GeoExt.Lang.set("${lang}");

    % if user:
    var initialExtent = ${user.role.json_extent};
    % else:
    var initialExtent = [420000, 30000, 900000, 350000];
    % endif

    var themes = {
        "local": ${themes | n}
    % if external_themes:
        , "external": ${external_themes | n}
    % endif
    };

    app = new gxp.Viewer({

        // viewer config
        portalConfig: {
            layout: 'border',
            items: [
                'app-map',
            {
                id: 'left-panel',
                region: 'west',
                width: 300
            }]
        },

        // tools
        tools: [{
            ptype: 'cgxp_editing',
            layerTreeId: 'layertree',
            layersURL: "${request.route_url('layers_root')}"
        }, {
            ptype: 'cgxp_themeselector',
            outputTarget: 'left-panel',
            outputConfig: {
                layout: 'fit',
                style: 'padding: 3px;'
            },
            layerTreeId: 'layertree',
            themes: themes
        }, {
            ptype: "cgxp_layertree",
            id: "layertree",
            outputConfig: {
                header: false,
                flex: 1,
                layout: 'fit',
                autoScroll: true,
                themes: themes,
                wmsURL: '${request.route_url('mapserverproxy')}'
            },
            outputTarget: 'left-panel'
        }, {
            ptype: "cgxp_menushortcut",
            type: '->'
        }, {
            ptype: "cgxp_login",
            actionTarget: "map.tbar",
    % if user:
            username: "${user.username}",
    % endif
            loginURL: "${request.route_url('login', path='')}",
            logoutURL: "${request.route_url('logout', path='')}"
        }],

        // map and layers
        map: {
            id: "app-map", // id needed to reference map in portalConfig above
            stateId: "map",
            xtype: 'cgxp_mappanel',
            projection: "EPSG:21781",
            extent: initialExtent,
            maxExtent: [420000, 30000, 900000, 350000],
            restrictedExtent: [420000, 30000, 900000, 350000],
            units: "m",
            resolutions: [4000,2000,1000,500,250,100,50,20,10,5,2.5,1,0.5,0.25,0.1,0.05],
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.KeyboardDefaults(),
                new OpenLayers.Control.PanZoomBar({panIcons: false}),
                new OpenLayers.Control.ArgParser(),
                new OpenLayers.Control.Attribution(),
                new OpenLayers.Control.ScaleLine({
                    bottomInUnits: false,
                    bottomOutUnits: false
                }),
                new OpenLayers.Control.MousePosition({numDigits: 0})
            ],
            layers: [{
                // base layers go here
            }],
            items: []
        }
    });

    app.on('ready', function() {
        // remove loading message
        Ext.get('loading').remove();
        Ext.fly('loading-mask').fadeOut({
            remove: true
        });
    }, app);
});
