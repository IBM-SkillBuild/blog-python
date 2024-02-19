var playerEmbed = {
    prontus_id: '',
    hostUrl: '',
    // Config predeterminada

    init: function () {
        var url = window.location.href;
        var src = "";
        var img = "";
        var splitted = url.split('?');
        if (typeof splitted[1] === 'undefined') {
            return;
        }
        var args = splitted[1].split(/&/);
        for (var i = 0; i < args.length; i++) {
            var temp = args[i].split(/=/);
            if (temp[0] == "src") {
                src = temp[1];
            }
        }
        if (src == "") {
            console.error('No se puede determinar src');
            return;
        }
        var temp = src.split('/');
        if (temp.length > 1) {
            playerEmbed.prontus_id = temp[1];
        }
        temp = window.location.href.split('/');
        if (temp.length > 2) {
            playerEmbed.hostUrl = temp[0] + '//' + temp[2];
        }
        var json_data = src.replace('.mp4', '.json');

        Utils.ajaxRequest({
            url: playerEmbed.hostUrl + json_data,
            success: function (data) {
                if (typeof data != 'undefined' && typeof data['qualities'] != 'undefined' && typeof data['qualities']['1']['file'] !== 'undefined') {
                    playerEmbed.install(data, src);
                } else {
                    // console.log('install 2');
                    playerEmbed.install({}, src);
                }
            },
            error: function () {
                console.error('Ocurrió un error al cargar.');
            }
        });
    },

    install: function (metadata, src) {
        var config = new Object();
        config.player = new Object();
        if (typeof metadata.poster !== 'undefined' && metadata.poster !== '' ) {
            config.player.image = playerEmbed.hostUrl + metadata.poster;
        }

        if (typeof metadata.thumbnails != 'undefined') {
            config.player.thumbnails = metadata.thumbnails;
        }

        var quality_counter = 0;

        if (typeof metadata.qualities != 'undefined') {
            quality_counter = Object.keys(metadata.qualities).length;
        }

        config.mediaSrc = new Object();

        if (typeof metadata.hls !== 'undefined' && metadata.hls !== '' ) {
            config.mediaSrc.defaultSrc = playerEmbed.hostUrl + metadata.hls;
        } else if (quality_counter > 1) {
            config.qualities = new Object();
            var labels = ["HD", "SD", "LQ"];
            var list = new Array();
            var i = 1;
            for (i = quality_counter; i >= 1; i--) {
                list.push({"label":labels[i-1],
                           "src": playerEmbed.hostUrl + metadata['qualities'][i]['file']
                        });
            }
            config.qualities.list = list;
            config.qualities.defaultQ = labels[0];
        } else {
            if (typeof metadata['qualities'] != 'undefined') {
                config.mediaSrc.defaultSrc = playerEmbed.hostUrl + metadata['qualities']['1']['file'];
            }
        }

        // TODO: verificar mismo origen.
        config.mediaSrc.defaultSrc = playerEmbed.hostUrl + src;
        // console.log('install player', config);

        prontusPlayer.installNow(config);
    }
};
