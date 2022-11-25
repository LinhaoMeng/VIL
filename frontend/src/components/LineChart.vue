<template>
  <div>
    <apexchart
      :width="width"
      :height="height"
      type="line"
      :options="chartOptions"
      :series="seriesdata"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: 'LineChart',
  props:{
      seriesdata: Array,
      width: Number,
      height: Number,
  },
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      chartOptions: {
        chart: {
          id: "vuechart-line",
        },
        xaxis: {
          type: 'numeric',
          decimalsInFloat: 0,
          tickAmount: 'dataPoints'
        },
        title: {
            text:"Test Accuray"
        }
      }
    };
  },
};

</script>
