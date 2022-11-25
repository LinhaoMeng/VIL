<template>
  <div id="imagepanel" class="column">
    <div id="imageboard" class="col">
      <div class="row justify-start">
        <div
          v-for="path in imagepaths"
          :key="path.index"
          :data-index="path.index"
          class="img-wrap"
          :style="'border-color:' + gettruecolorfn(path.index)"
        >
          <ImageBox
            :path="path"
            :removeImg="removeImg"
            :getImgUrl="getImgUrl"
          />
        </div>
      </div>
    </div>
    <LabelOperation :labeldatafn="labeldatafn" />
  </div>
</template>size

<script>
import { computed } from "vue";
import { useStore } from "@/stores/globalstore";
import { select, selectAll } from "d3";

import LabelOperation from "./LabelOperation.vue";
import ImageBox from "./ImageBox.vue";

export default {
  components: { LabelOperation, ImageBox },
  setup() {
    const store = useStore();
    const labeleddata = computed(() => store.labeleddata);
    const newlabelledlabels = computed(() => store.newlabelledlabels);
    const classcolorscale = computed(() => store.classcolorscale);
    // const predictions = computed(()=>store.predictions);

    const baseURL = process.env.VUE_APP_ROOT_API;

    const getImgUrl = (path) => {
      return baseURL + "/images" + path + "?" + Date.now();
    };

    const imagepaths = computed(() => store.imagepaths);

    const removeImg = (index) => {
      console.log(
        index,
        imagepaths.value.findIndex((d) => d.index === index)
      );
      imagepaths.value.splice(
        imagepaths.value.findIndex((d) => d.index === index),
        1
      );

      // select(e.target).node().closest('.img-wrap').remove()
    };

    const labeldatafn = (label) => {
      let indexarr = [];
      selectAll(".img-wrap").each(function (d, i) {
        indexarr[i] = select(this).node().dataset.index;
      });
      console.log(indexarr);
      store.labeldata(indexarr, label);
    };

    const gettruecolorfn = (index) => {
      let label = newlabelledlabels.value[index];
      if (label === -1) {
        label = labeleddata.value[index];
      }
      if (label !== -1) {
        return classcolorscale.value(label);
      } else {
        return "None";
      }
    };

    return {
      getImgUrl,
      removeImg,
      labeldatafn,
      imagepaths,
      gettruecolorfn,
    };
  },
};
</script>

<style lang="scss" scoped>
#imagepanel {
  width: 100%;
  height: 100%;
}
#imageboard {
  overflow-y: scroll;
  height: auto;
  border-bottom: 1px solid grey;
  //max-height: 00px;
}
#labelbuttons {
  height: 40px;
  display: table-cell;
  vertical-align: middle;
}
.img-wrap {
  width: 52px;
  border-width: 1px;
  border-style: solid;
  font-size: 0;
  position: relative;
}
</style>