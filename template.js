function createConfig(details, data) {
    return {
        type: details.type,
        data: {
            labels: details.labels,
            datasets: [{
                data: details.data,
                borderColor: details.color,
                fill: true,
            }]
        },
        options: {
            legend: {
                display: false,
                onClick: null
            },
            responsive: true,
            title: {
                display: true,
                text: details.tableName
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = tooltipItem.xLabel;
                        var array = [];
                        var value = {
                            "Followers": details.data[details.labels.indexOf(label)],
                            "Title": details.title[details.labels.indexOf(label)],
                            "Director": details.director[details.labels.indexOf(label)],
                            "Writter": details.writter[details.labels.indexOf(label)],
                            "StoryBoard": details.storyBoard[details.labels.indexOf(label)],
                            "Airdate": details.airdate[details.labels.indexOf(label)]
                        };
                        Object.entries(value).forEach(([k, v]) => {
                            if (v) {
                                array.push(
                                    k + ": " + v
                                );
                            }
                        });
                        return array;
                    }
                }
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: details.Xlabel
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: details.Ylabel
                    }
                }]
            }
        }
    };
}

window.onload = function() {
    var container = document.querySelector('.container');

    var steppedLineSettings = [@1@];

    steppedLineSettings.forEach(function(details) {
        var div = document.createElement('div');
        div.classList.add('chart-container');

        var canvas = document.createElement('canvas');
        div.appendChild(canvas);
        container.appendChild(div);

        eval('temp = ' + details + ';');
        var ctx = canvas.getContext('2d');
        var config = createConfig(temp);
        new Chart(ctx, config);
    });
};