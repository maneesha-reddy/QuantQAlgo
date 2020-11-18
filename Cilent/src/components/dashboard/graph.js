import React, { Component } from 'react';
import { Line } from "react-chartjs-2";

class Graph extends Component {
    constructor(props) {
        super(props);
        this.state = {  }
        // console.log(this.props)
    }
    render() { 
      // console.log(this.props.grad,"props")
        const data =(canvas) => {
            const ctx = canvas.getContext("2d")
            const gradient = ctx.createLinearGradient(0,0,0,170);
            // gradient.addColorStop(0,"#99e699");
            // gradient.addColorStop(1,"#f2f2f2");
            
            gradient.addColorStop(0,this.props.grad);
            gradient.addColorStop(1,"#f2f2f2");
            return {
                // backgroundColor: gradient,
                labels: this.props.labels,
                 datasets: [
              {
                lineTension: 0,
                label: this.props.title,
                data: this.props.data,
                pointRadius: 0.2,
                // borderColor: " #29a329",
                borderColor:this.props.border,
                backgroundColor: gradient,
                // pointBackgroundColor: "#108ee9",
                // pointBorderColor: "#108ee9",
                // pointHighlightFill: "#108ee9",
                // pointHighlightStroke: "#108ee9",
              },
            ],
            }
            
          };
          const options = {
            legend: {
              display: false,
            },
            scales: {
              xAxes: [
                {
                  // display: true,
                //   scaleLabel: {
                //     display: true,
                //     labelString: "Time",
                //   },
                //   gridLines: {
                //     display: true,
                //     drawBorder: true,
                //     color: "#525252"
                //   },
                //   ticks: {
                //     fontColor: "black",
                //     fontSize: 14,
                //     beginAtZero: true,
                //   },
                },
              ],
              yAxes: [
                {
                  // display: true,
                //   scaleLabel: {
                //     display: true,
                //     // labelString: props.name === "Finished" ? "Finished Tasks" : "Actual Time",
                //     labelString:"LTP",
                //   },
                //   gridLines: {
                //     display: true,
                //     drawBorder: true,
                //     color: "#525252"
                //   },
                //   ticks: {
                //     fontColor: "black",
                //     fontSize: 14,
                //     beginAtZero: true,
                //   },
                },
              ],
            },
          };
        return ( 
            <div style={{width:"230px",height:"150px"}}>
                <Line data={data} options={options}/>
            </div>
          );
    }
}

 
export default Graph;