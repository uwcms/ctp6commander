var CTPStatus = (function () {
    var my = {};

    // get the status JSON for the given links, calls callback(data) on success
    var getStatus = function(linkstring, callback) {
        var callbackWithError = function(error, json) {
            if (error) return console.warn(error);
            console.log("WTF");
            callback(json);
        };
        d3.json("/api/status/" + linkstring, callbackWithError);
    };

    var renderStatus = function(statusJsonData) {
        // each link is a div-row.
        // each flag is a span-col
        console.log("render");
        var links = [];
        for (var l in statusJsonData) {
            links.push(l);
        }
        // sort by ascending links.
        links.sort(function(a, b) { return parseInt(a, 10) > parseInt(b, 10); });

        console.log(links);

        var flags = ['Overflow', 'Underflow',
            'LossSync', 'PLLk OK', 'ErrDetect'];

        // Add a header row.  An extra column for the link# and one at the end
        // for the link reset control.
        var headerLabels = ['Link#'].concat(flags).concat(['']);
        console.log(headerLabels);
        d3.select("#linkstatus").selectAll('tr').data([null])
            .enter()
            .append('tr')
            .each(function(dontcare, i) {
                var row = d3.select(this).selectAll("th");
                row.data(headerLabels).enter().append('th')
                    .text(function(d) {return d;});
            });

        // reset button functions
        var resetLinkControl = {};
        resetLinkControl.icon = "icon-repeat";
        resetLinkControl.callback = function(link) {
            d3.json('/api/reset/' + link, function(e, data) {
                console.log("Reset link " + link + ": " + data);
            });
        };

        // function to generate the columns in a <tr>
        var updateRowBadges = function(row, link) {
        };

        d3.select("#linkstatus").selectAll('tr .linkstatusrow').data(links)
            .enter()
            .append('tr')
                .classed("linkstatusrow", true)
                .each(function(link, i) {
                    // select the parent div
                    var row = d3.select(this).selectAll("td .linkrowlabel");
                    row.data([link]).enter().append('td')
                        .classed("linkrowlabel", true)
                        .text(function(idx) {return idx;});

                    row = d3.select(this).selectAll("td .linkstatusbadge");
                    row.data(flags)
                        .enter()
                        .append('td')
                        .attr("class", function(flag) {
                            if (statusJsonData[link][flag]) {
                                return "linkstatusbadge " + "linkstatusok";
                            } else
                                return "linkstatusbadge " + "linkstatusbad";
                        })
                        .text(function(flag) { return flag; });

                    row = d3.select(this).selectAll("td .linkstatuscontrol");
                    row.data([resetLinkControl])
                        .enter()
                        .append('td')
                        .append('span')
                        .attr("class", function (x) { 
                            return "linkstatuscontrol " + x.icon; });

                });
    };

    var doStatus = function(linkstring) {
        console.log("do");
        getStatus(linkstring, renderStatus);
    };

    my.renderStatus = renderStatus;
    my.getStatus = getStatus;
    my.doStatus = doStatus;

    return my;
})();
