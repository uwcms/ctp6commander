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

        var flags = ['Overflow', 'Underflow', 'LossSync', 'PLLk OK', 'ErrDetect'];

        d3.select("#linkstatus").selectAll('div').data(links)
            .enter()
            .append('div')
                .each(function(link, i) {
                    console.log(link);
                    // select the parent div
                    var theParentDiv = d3.select(this).selectAll("span");
                    theParentDiv.data([i]).enter().append('span').text(
                        function(idx) {return idx;});
                    theParentDiv.data(flags)
                        .enter()
                        .append('span')
                        // .classed("badge", true)
                        .text(function(flag) { return flag; })
                        .style("background-color",function(flag) {
                            console.log(this);
                            if (statusJsonData[link][flag]) {
                                return "#4DAF4A";
                            } else
                                return "#E41A1C";
                        });
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
