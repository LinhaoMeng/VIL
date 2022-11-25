<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="switchleftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title> Visual Interactive Labelling </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-grey-2">
      <ALSetting :switchleftDrawerOpen="switchleftDrawerOpen" />
    </q-drawer>

    <q-page-container>
      <q-page>
        <div class="fit" style="min-height: inherit; display: flex">
          <div class="row" style="width: 100%">
            <div class="col-8 panel">
              <ProjectionView />
            </div>
            <div class="col panel">
              <ImagePanel />
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from "vue";
import ProjectionView from "@/components/ProjectionView.vue";
import ALSetting from "@/components/ALSetting.vue";
import ImagePanel from "@/components/ImagePanel.vue";

export default {
  components: {
    ProjectionView,
    ALSetting,
    ImagePanel,
  },

  setup() {
    const leftDrawerOpen = ref(false);
    const switchleftDrawerOpen = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };
    return {
      leftDrawerOpen,
      switchleftDrawerOpen,
    };
  },
};
</script>

<style lang="scss" scoped>
.panel {
  margin: 1px;
  border: 2px solid;
}
</style>

