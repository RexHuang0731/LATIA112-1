// Get data
d3.csv("https://raw.githubusercontent.com/RexHuang0731/LATIA112-1/main/HW4/exchange99-111.csv").then(
    res => {
        console.log(res);
        drawPieChart(res);
        drawBarChart(res);
        drawLinChart(res);
    }
);

function drawPieChart(res){
    
    let trace1 = {};
    trace1.type = "pie";
    trace1.title = {
        text: '111 year exchange student type ratio',
        font : {
            size:27,
        },
    };
    trace1.labels = ['Foreign students formally studying for a degree', 'Overseas Chinese (including Hong Kong and Macao)', 'Formal degree-seeking mainland students', 'foreign exchange students', 'Short-term study abroad and personal selection of readings', 'Students at the Chinese Language Center affiliated with a junior college', 'Mainland trainees', 'Haiqing class'];
    trace1.values = [0,0,0,0,0,0,0,0];
    trace1.hole = 0.72;
    trace1.textfont = {
        size:25,
    };

    trace1.values[0] = parseInt(res[12]['Foreign students formally studying for a degree']);
    trace1.values[1] = parseInt(res[12]['Overseas Chinese (including Hong Kong and Macao)']);
    trace1.values[2] = parseInt(res[12]['Formal degree-seeking mainland students']);
    trace1.values[3] = parseInt(res[12]['foreign exchange students']);
    trace1.values[4] = parseInt(res[12]['Short-term study abroad and personal selection of readings']);
    trace1.values[5] = parseInt(res[12]['Students at the Chinese Language Center affiliated with a junior college']);
    trace1.values[6] = parseInt(res[12]['Mainland trainees']);
    trace1.values[7] = parseInt(res[12]['Haiqing class']);

    let data1 = [];
    data1.push(trace1);
    
    let layout1 = {
        margin:{
            t:50,
            b:50,
        },
        legend:{
            font:{
                size:23.5,
            },
        },
    };
    
    Plotly.newPlot(myGraph1, data1, layout1);
};

function drawBarChart(res){
    
    let trace2 = {};
    trace2.type = "bar";
    
    trace2.x = [];
    trace2.y = [];
    trace2.text = trace2.y;
    trace2.textfont = {
        size:20,
    };
    trace2.marker = {
        color:'#1f77b4',
    };
    trace2.name = "Chinese formal degree students";

    for(let i=0;i<res.length;i++){
        trace2.x[i] = res[i]['year'];
        trace2.y[i] = res[i]['Formal degree-seeking mainland students'];
    };

    let trace22 = {};
    trace22.type = "bar";

    trace22.x = [];
    trace22.y = [];
    trace22.text = trace22.y;
    trace22.textfont = {
        size:20,
    };
    trace22.marker = {
        color:'#7f7f7f',
    };
    trace22.name = "Foreign formal degree students";

    for(let i=0;i<res.length;i++){
        trace22.x[i] = res[i]['year'];
        trace22.y[i] = res[i]['Foreign students formally studying for a degree'];
    };

    let data2 = [];
    data2.push(trace2);
    data2.push(trace22);

    let layout2 = {
        margin:{
            t:100,
        },
        title:{
            text:"99~111 year formal degree foreign and Chinese students",
            font:{
                size:33,
            },
        },
        xaxis:{
            dtick:1,
            tickfont:{
                size:25,
            },
        },
        yaxis:{
            tickfont:{
                size:25,
            },
        },
        legend:{
            x:0,
            y:1,
            orientation:'h',
            font:{
                size:25,
            },
        },
    };

    Plotly.newPlot(myGraph2, data2, layout2);
};

function drawLinChart(res){
    
    let trace3 = {};
    trace3.mode = "markers+lines";
    trace3.type = "scatter";
    trace3.name = "99~111 year the number of foreign students formally studying for a degree";
    trace3.marker = {
        size:15,
        color:'red',
    };

    trace3.x = [];
    trace3.y = [];
    trace3.text = trace3.y;
    trace3.textposition = "bottom center";
    trace3.textfont = {
        family:"Raleway, sans-serif",
        size:20,
        color:"black"
    };
    

    for(let i=0;i<res.length;i++){
        trace3.x[i] = res[i]["year"];
        trace3.y[i] = res[i]["Foreign students formally studying for a degree"]
    };

    let data3 = [];
    data3.push(trace3);

    let layout3 = {
        margin:{
           t:100,
        },
        title:{
            text:"99~111 year the number of foreign students formally studying for a degree",
            font:{
                size:33,
            },
        },
        xaxis:{
            dtick:1,
            tickfont:{
                size:25,
            },
        },
        yaxis:{
            tickfont:{
                size:25,
            },
        },
    };

    Plotly.newPlot(myGraph3, data3, layout3);
};