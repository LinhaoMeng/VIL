<template>
  <div id="projectioncanvas" ref="divRef" v-resize="onResize">
    <canvas ref="canvasRef" />
    <canvas ref="upperCanvasRef" />
    <svg ref="svgRef">
      <g class="brush" />
    </svg>
    <div style="position: absolute">
      <q-btn
        color="white"
        text-color="black"
        label="prediction"
        no-caps
        @click="setencoding('prediction')"
      />
      <q-btn
        color="white"
        text-color="black"
        label="label"
        no-caps
        @click="setencoding('label')"
      />
    </div>
    <div style="position: absolute; right: 5px">
      <q-btn-toggle
        v-model="selecttool"
        size="md"
        dense
        toggle-color="yellow"
        :options="[
          { value: 'brush', slot: 'one' },
          { value: 'lasso', slot: 'two' },
        ]"
      >
        <template v-slot:one>
          <div class="row items-center no-wrap">
            <q-icon name="img:brush.svg" />
          </div>
        </template>

        <template v-slot:two>
          <div class="row items-center no-wrap">
            <q-icon name="img:lasso.svg" />
          </div>
        </template>
      </q-btn-toggle>
    </div>
  </div>
</template>

<script>
import { useStore } from "@/stores/globalstore";
import { select, extent, scaleLinear, brush, polygonContains } from "d3";
import { renderQueue } from "@/components/utils/util";
import lasso from "@/components/utils/lasso";

import { computed } from "vue";

export default {
  data() {
    return {
      width: 500,
      height: 500,
      margin: 5,
      ctx: null,
      upperctx: null,
      r: 3,
      selectedindexes: [],
      encoding: "label",
      trianglelength: 10,
      selecttool: "lasso",
    };
  },
  computed: {
    xScale() {
      console.log(this.embeddeddata);
      let range0 = extent(this.embeddeddata.map((d) => d[0]));
      return scaleLinear()
        .domain(range0)
        .range([this.margin, this.width - this.margin]);
    },
    yScale() {
      let range0 = extent(this.embeddeddata.map((d) => d[1]));
      return scaleLinear()
        .domain(range0)
        .range([this.height - this.margin, this.margin]);
    },
    canvasbrush() {
      return brush()
        .extent([
          [0, 0],
          [this.width, this.height],
        ])
        .on("end", this.brushed);
    },
    triangleheight() {
      return (this.trianglelength * Math.sqrt(3)) / 2;
    },
  },
  setup() {
    const store = useStore();
    return {
      embeddeddata: computed(() => store.embedding),
      getImages: store.getImages,
      predictions: computed(() => store.predictions),
      allprobs: computed(() => store.allprobs),
      prediction_probs: computed(() => store.prediction_probs),
      labeleddata: computed(() => store.labeleddata),
      newlabelledlabels: computed(() => store.newlabelledlabels),
      labeltime: computed(() => store.labeltime),
      ylabel: computed(() => store.ylabel),
      classcolorscale: computed(() => store.classcolorscale),
      suggestedindices: computed(() => store.suggestedindices),
      updateselectedindices: store.updateselectedindices,
      globalselectedindixes: computed(() => store.selectedindices),
    };
  },
  mounted() {
    this.width = this.$refs.divRef.clientWidth;
    this.height = this.$refs.divRef.clientHeight;
    this.lasso = lasso().on("end", this.handleLassoEnd);
    this.initView();
  },
  watch: {
    embeddeddata() {
      this.renderPoints(this.width, this.height);
    },
    encoding() {
      this.renderPoints(this.width, this.height);
    },
    labeltime() {
      this.renderPoints(this.width, this.height);
    },
    selecttool(newtool, oldtool) {
      if (newtool === oldtool) return;
      if (newtool === "lasso") this.lasso.show();
      else this.lasso.hide();
    },
    suggestedindices: {
      deep: true,
      handler() {
        this.renderCandidates(this.width, this.height);
      },
    },
    globalselectedindixes: {
      deep: true,
      handler() {
        this.renderCandidates(this.width, this.height);
      },
    },
  },
  methods: {
    onResize({ width, height }) {
      this.width = width;
      this.height = height;
      // resize canvas and svg
      const svg = select(this.$refs.svgRef);
      const canvas = select(this.$refs.canvasRef);
      const uppercanvas = select(this.$refs.upperCanvasRef);
      canvas.attr("width", width).attr("height", height);
      uppercanvas.attr("width", width).attr("height", height);
      // brush g needs to rebind after svg size change
      this.drawSVG(svg, width, height);
      // rerender the points based on the new size
      this.renderPoints(width, this.height);
      this.renderCandidates(this.width, this.height);
    },

    initView() {
      const svg = select(this.$refs.svgRef);
      const canvas = select(this.$refs.canvasRef);
      const uppercanvas = select(this.$refs.upperCanvasRef);
      this.drawCanvas(canvas, uppercanvas, this.width, this.height);
      this.drawSVG(svg, this.width, this.height);
      this.renderPoints(this.width, this.height);
      this.renderCandidates(this.width, this.height);
    },

    //===================for canvas==========================//
    drawCanvas(canvas, uppercanvas, width, height) {
      canvas.attr("width", width).attr("height", height);
      this.ctx = canvas.node().getContext("2d");
      this.ctx.globalCompositeOperation = "color";
      this.ctx.globalAlpha = 0.8;
      this.ctx.lineWidth = 2;
      uppercanvas.attr("width", width).attr("height", height);
      this.upperctx = uppercanvas.node().getContext("2d");
      // ctx.globalCompositeOperation = 'color';
      this.upperctx.globalAlpha = 0.6;
      this.upperctx.lineWidth = 5;
    },

    triangledraw(x, y, ctx) {
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + this.trianglelength, y);
      ctx.lineTo(x + this.trianglelength / 2, y - this.triangleheight);
      ctx.closePath();
    },
    circledraw(x, y, r, ctx) {
      ctx.beginPath();
      ctx.arc(x, y, r, 0, 2 * Math.PI);
      ctx.closePath();
    },
    stardraw(cx, cy, spikes, outerRadius, innerRadius) {
      var rot = (Math.PI / 2) * 3;
      var x = cx;
      var y = cy;
      var step = Math.PI / spikes;

      this.upperctx.beginPath();
      this.upperctx.moveTo(cx, cy - outerRadius);
      for (let i = 0; i < spikes; i++) {
        x = cx + Math.cos(rot) * outerRadius;
        y = cy + Math.sin(rot) * outerRadius;
        this.upperctx.lineTo(x, y);
        rot += step;

        x = cx + Math.cos(rot) * innerRadius;
        y = cy + Math.sin(rot) * innerRadius;
        this.upperctx.lineTo(x, y);
        rot += step;
      }
      this.upperctx.lineTo(cx, cy - outerRadius);
      this.upperctx.closePath();
    },

    drawpoints_predmodel(d, i) {
      let islabel = 0;
      let labelcolor;

      //use prediction color to fill shape
      let predcolor = this.classcolorscale(this.predictions[i]);
      this.ctx.fillStyle = predcolor;

      // if it is newly labelled
      // no
      if (this.newlabelledlabels[i] !== -1) {
        labelcolor = this.classcolorscale(this.newlabelledlabels[i]);
        islabel = 1;
      }
      //yes
      else {
        if (this.labeleddata[i] !== -1) {
          labelcolor = this.classcolorscale(this.ylabel[i]);
          islabel = 1;
        }
      }

      if (islabel) {
        this.triangledraw(
          this.xScale(d[0]) - this.trianglelength / 2,
          this.yScale(d[1]) + this.triangleheight / 2,
          this.ctx
        );
        if (labelcolor !== predcolor) {
          this.ctx.strokeStyle = labelcolor;
          this.ctx.stroke();
        }
        this.ctx.fill();
      } else {
        this.circledraw(this.xScale(d[0]), this.yScale(d[1]), this.r, this.ctx);
        this.ctx.fill();
      }
    },

    drawpoints_labelmode(d, i) {
      let islabel = 1;
      // if it is newly labelled
      // no
      if (this.newlabelledlabels[i] === -1) {
        // if it is labelled before
        if (this.labeleddata[i] !== -1) {
          this.ctx.fillStyle = this.classcolorscale(this.ylabel[i]);
        } else {
          this.ctx.fillStyle = "#444444";
          islabel = 0;
        }
      }
      //yes
      else {
        this.ctx.fillStyle = this.classcolorscale(this.newlabelledlabels[i]);
      }

      // if it is labelled draw triangle
      if (islabel) {
        this.triangledraw(
          this.xScale(d[0]) - this.trianglelength / 2,
          this.yScale(d[1]) + this.triangleheight / 2,
          this.ctx
        );
        this.ctx.fill();
      }
      // or else draw point
      else {
        this.circledraw(this.xScale(d[0]), this.yScale(d[1]), this.r, this.ctx);
        this.ctx.fill();
      }
    },

    renderPoints(width, height) {
      this.ctx.clearRect(0, 0, width, height);
      let render;
      if (this.encoding === "label") {
        render = renderQueue(this.drawpoints_labelmode);
      } else {
        render = renderQueue(this.drawpoints_predmodel);
      }
      render(this.embeddeddata);
    },

    drawupperpoints(d) {
      // this.drawStar(this.xScale(d[0]), this.yScale(d[1]), 5, 30, 15, this.upperctx)
      this.circledraw(this.xScale(d[0]), this.yScale(d[1]), 5, this.upperctx);
      this.upperctx.lineWidth = 5;
      this.upperctx.strokeStyle = "blue";
      this.upperctx.stroke();
      this.upperctx.fillStyle = "skyblue";
      this.upperctx.fill();
    },

    renderCandidates(width, height) {
      this.upperctx.clearRect(0, 0, width, height);
      let data = this.suggestedindices.map((d) => this.embeddeddata[d]);
      for (let d of data) {
        this.stardraw(
          this.xScale(d[0]),
          this.yScale(d[1]),
          5,
          30,
          15,
          this.upperctx
        );
        this.upperctx.lineWidth = 5;
        this.upperctx.strokeStyle = "blue";
        this.upperctx.stroke();
        this.upperctx.fillStyle = "skyblue";
        this.upperctx.fill();
      }
      let render = renderQueue(this.drawupperpoints);
      render(this.globalselectedindixes.map((d) => this.embeddeddata[d]));
    },

    //===================for SVG==========================//
    drawSVG(svg, width, height) {
      svg.attr("width", width).attr("height", height);
      //    .attr("viewBox", [0, 0, width, height])
      svg.select(".brush").remove();
      svg.attr("class", "brush").call(this.canvasbrush);
      svg.call(this.lasso);
    },

    // when a lasso is completed, filter to the points within the lasso polygon
    handleLassoEnd(lassoPolygon) {
      this.selectedindexes = this.embeddeddata.reduce(
        (a, d, i /*Current index*/) => {
          if (
            polygonContains(lassoPolygon, [
              this.xScale(d[0]),
              this.yScale(d[1]),
            ])
          ) {
            a.push(i); //Add the found index.
          }
          return a;
        },
        []
      );

      this.updateselectedindices(this.selectedindexes);
      this.lasso.reset();
    },

    brushed({ sourceEvent, selection }) {
      if (!sourceEvent) return;
      if (selection) {
        const [[x0, y0], [x1, y1]] = selection;
        this.selectedindexes = this.embeddeddata.reduce(
          (a, d, i /*Current index*/) => {
            if (
              this.xScale(d[0]) > x0 &&
              this.xScale(d[0]) < x1 &&
              this.yScale(d[1]) > y0 &&
              this.yScale(d[1]) < y1
            )
              a.push(i); //Add the found index.
            return a;
          },
          []
        );
      }
      this.updateselectedindices(this.selectedindexes);
      select("g.brush").call(this.canvasbrush.move, null);
    },

    setencoding(method) {
      if (method === "prediction") {
        this.encoding = "prediction";
      } else {
        this.encoding = "label";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#projectioncanvas {
  padding: 0;
  height: 100%;
  position: relative;
  width: 100%;
}
canvas {
  position: absolute;
}

svg {
  position: absolute;
  fill: none;
  stroke: none;
  overflow: visible;
}

text {
  font: bold 16px sans-serif;
}
</style>
