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
        var linkStatuses = [];
        for (var l in statusJsonData) {
            linkStatuses.push({
                'link': l,
                'theStatus': statusJsonData[l]
            });
        }
        // sort by ascending links.
        linkStatuses.sort(function(a, b) { 
            return parseInt(a.link, 10) > parseInt(b.link, 10); });

        // reset button functions
        var resetLinkControl = {};
        resetLinkControl.icon = "icon-repeat";
        resetLinkControl.callback = function(link) {
            d3.json('/api/reset/' + link, function(e, data) {
                console.log("Reset link " + link + ": " + data);
            });
        };

        // Our table.
        var statusTable = d3.select("#linkstatus");
        // Get the status flag types
        var flags = [];
        for (var i = 0; i < linkStatuses[0].theStatus.length; ++i) {
            flags.push(linkStatuses[0].theStatus[i][0]);
        }

        // Add a header row.  An extra column for the link# and one at the end
        // for the link reset control.
        var headerLabels = ['Link#'].concat(flags).concat(['Reset']);
        var headerRow = statusTable.selectAll('tr .linkstatusheader')
            .data([null]).enter()
                .append('tr').classed('linkstatusheader', true);
        headerRow.selectAll('th').data(headerLabels).enter()
            .append('th').text(function(d) { return d; });

        // create a row for each link and embed the status data
        var rows = statusTable.selectAll('tr .linkstatusrow')
            .data(linkStatuses)
            .enter()
                .append('tr')
                .classed("linkstatusrow", true);

        // give each row a link row label
        rows.selectAll("td .linkrowlabel").data(
                function(d) { return [d.link]; })
            .enter()
                .append('td')
                .classed('linkrowlabel', true)
                .text(function(link) { return link; });


        // populate the data
        rows.selectAll('td .linkstatusbadge').data(
                function(d) { return d.theStatus; })
            .enter()
                .append('td')
                .attr("class", function(x) {
                    if (x[1]) {
                        return "linkstatusbadge " + "linkstatusok";
                    } else
                    return "linkstatusbadge " + "linkstatusbad";
                })
                .text(function(x) { return x[0]; });

        // add a control for each row
        rows.selectAll('td .linkresetcontrol')
            .data(function(d) { return [[this, d]]; })
            .enter()
                .append('td')
                .classed('linkresetcontrol', true)
                    .append('span')
                    .on("click", function(d) { console.log(d); })
                    .style("cursor", "pointer")
                    .classed('icon-repeat', true);
    };

    var doStatus = function(linkstring) {
        getStatus(linkstring, renderStatus);
    };

    my.renderStatus = renderStatus;
    my.getStatus = getStatus;
    my.doStatus = doStatus;

    return my;
})();
