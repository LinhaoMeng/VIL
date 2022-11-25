<template>
  <div>
    <q-list>
      <q-item-label header>Labeling Setting</q-item-label>
      <q-item>
        <q-item-section avatar>
          <q-icon name="source" />
        </q-item-section>
        <q-item-section>
          <q-select
            v-model="dataset"
            :options="datasetoptions"
            label="Dataset"
          />
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section avatar>
          <q-icon name="numbers" />
        </q-item-section>
        <q-item-section>
          <q-item-section>
            <span>
              Percentage of labelled: {{ `${parseInt(10 * initialN)}%` }}
            </span>
            <q-slider
              v-model="initialN"
              color="deep-orange"
              markers
              :marker-labels="fnMarkerLabel"
              :min="0"
              :step="0"
              :max="5"
            />
          </q-item-section>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section avatar>
          <q-icon name="model_training" />
        </q-item-section>
        <q-item-section>
          <q-select v-model="model" :options="modeloptions" label="Model" />
        </q-item-section>
      </q-item>
    </q-list>
    <div class="row justify-center">
      <q-btn color="primary" label="Load Data" @click="loaddata" />
    </div>
    <hr class="dashed" />
    <q-list dense>
      <q-item>
        <q-item-section>
          <q-item-label>selection mode:</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-btn-toggle
            v-model="selectionmode"
            push
            glossy
            toggle-color="primary"
            :options="[
              { value: 'new', slot: 'one' },
              { value: 'union', slot: 'two' },
              { value: 'intersection', slot: 'three' },
            ]"
          >
            <template v-slot:one>
              <div class="row items-center no-wrap">
                <span
                  class="icon-new"
                  style="
                    font-size: 16px;
                    line-height: 0;
                    vertical-align: bottom;
                    display: inline-block;
                  "
                ></span>
              </div>
            </template>

            <template v-slot:two>
              <div class="row items-center no-wrap">
                <span
                  class="icon-union"
                  style="
                    font-size: 22px;
                    line-height: 0;
                    vertical-align: bottom;
                    display: inline-block;
                  "
                ></span>
              </div>
            </template>

            <template v-slot:three>
              <div class="row items-center no-wrap">
                <span
                  class="icon-intersect"
                  style="
                    font-size: 22px;
                    line-height: 0;
                    vertical-align: bottom;
                    display: inline-block;
                  "
                ></span>
              </div>
            </template>
          </q-btn-toggle>
        </q-item-section>
      </q-item>
      <q-item-label header>Get AL suggestions</q-item-label>
      <q-item>
        <q-btn color="secondary" label="Retrain Model" @click="retrainmodel" />
      </q-item>
      <q-item>
        <q-item-section>
          <q-select
            v-model="selectedstrategy"
            :options="strategyoptions"
            label="Select Strategy"
          />
        </q-item-section>
        <q-item-section>
          <q-btn color="amber" label="OK" @click="getcandidate" />
        </q-item-section>
      </q-item>
    </q-list>
    <hr class="dashed" />
    <div class="row justify-center">
      <LineChart :seriesdata="accdata" :width="width" :height="150" />
      <BarChart
        :seriesdata="labelledstat"
        :width="width"
        :height="150"
        :categories="labelnames"
      />
      <HorizontalBar
        :seriesdata="labelpercentage"
        :width="width"
        :height="80"
        :categories="['#']"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "@/stores/globalstore";
import LineChart from "./LineChart.vue";
import BarChart from "./BarChart.vue";
import HorizontalBar from "./HorizontalBar.vue";

export default {
  name: "ALSetting",
  components: { LineChart, BarChart, HorizontalBar },
  data() {
    return {
      width: 280,
    };
  },
  props: {
    switchleftDrawerOpen: Function,
  },
  setup() {
    const dataset = ref("MNIST");
    const initialN = ref(2);
    const model = ref("KNN");

    // const selectionmode = ref('new');
    const selectedstrategy = ref("uncertainty");

    const store = useStore();

    const loaddata = () => {
      const setting = {
        dataset: dataset.value,
        initialN: parseFloat(parseInt(10 * initialN.value) / 100),
        model: model.value,
      };
      store.initialAL(setting);
      // props.switchleftDrawerOpen();
    };

    const selectionmode = computed({
      get: () => store.selectionmode,
      set: (val) => store.changeselectionmode(val),
    });

    const retrainmodel = () => {
      store.itertrain();
    };

    const getcandidate = () => {
      store.getcandidate(selectedstrategy.value);
    };

    return {
      dataset,
      datasetoptions: ["MNIST"],
      initialN,
      fnMarkerLabel: {
        0: "0%",
        1: "10%",
        2: "20%",
        3: "30%",
        4: "40%",
        5: "50%",
      },
      model,
      modeloptions: ["KNN", "SVM"],
      selectionmode,
      selectedstrategy,
      strategyoptions: ["uncertainty", "density"],
      loaddata,
      retrainmodel,
      getcandidate,
      accdata: computed(() => store.acclinedata),
      labelnames: computed(() => store.labelnames),
      labelledstat: computed(() => store.labelledstat),
      labelpercentage: computed(() => store.labelpercentage),
      colors: computed(() => store.colors),
    };
  },
};
</script>