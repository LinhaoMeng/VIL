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
  name: 'HorizontalBar',
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
            plotOptions: {
                bar: {
                    horizontal: true,
                }
            },
            chart:{
                stacked: true,
                stackType: '100%'
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