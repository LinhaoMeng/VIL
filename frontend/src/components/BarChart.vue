<template>
  <div>
    <apexchart
      :width="width"
      :height="height"
      type="bar"
      :options="chartOptions"
      :series="seriesdata"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: 'BarChart',
  props:{
      seriesdata: Array,
      width: Number,
      height: Number,
      categories: Array,
  },
  components: {
    apexchart: VueApexCharts,
  },
  computed:{
    chartOptions(){
        return {
            xaxis:{
                categories: this.categories
            },
            title: {
                text:"No. of Labeled"
            },
            plotOptions: {
                bar: {
                    distributed: true,
                }
            },
            chart:{
                stacked: true,
            },
            legend: {
                show: false
            },
            tooltip: {
                shared: true,
                intersect:false
            }
        }
    }
  }
};

</script>