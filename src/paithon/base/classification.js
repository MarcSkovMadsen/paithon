render=()=>{
  state.oMap = function(x){return {"x": x["label"], "y": Math.round(x["score"]*100)}}
  state.theme = function(){return {default: "light", dark: "dark"}[data.theme]}
  state.options=()=>{return {...data._base_options, series: [{name: "Score", "data": Array.from(data.output_json, state.oMap)}], colors: [data.color], theme: {mode: state.theme()}}};
  state.chart = new ApexCharts(plot, state.options());
  state.chart.render();
}
output_json=()=>{
  state.chart.updateOptions(state.options())
}
color=()=>{
  state.chart.updateOptions({colors: [data.color]})
}
theme=()=>{
  state.chart.updateOptions({theme: {mode: state.theme()}})
}
after_layout=()=>{
  // window.dispatchEvent(new Event('resize'))
}