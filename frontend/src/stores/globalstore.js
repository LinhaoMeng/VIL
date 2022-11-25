import {
  defineStore
} from 'pinia';
import * as api from './api.js';
import {
  scaleOrdinal
} from 'd3';

export const useStore = defineStore('globalstore', {
  state: () => ({
    datatype: '',
    selectionmode: 'new',
    embedding: [],
    ylabel: [],
    datacount: 0,
    labeleddata: [],
    acc: [],
    labelnames: [],
    imagepaths: [],
    predictions: [],
    allprobs: [],
    prediction_probs: [],
    //for each model training iteration
    selectedindices: [],
    newlabelledlabels: [],
    labeltime: 0, // for projection canvas update
    //will change after each model retraining
    suggestedindices: [],
    colors: ['#FB4626', '#2A8DD3', '#FD9019', '#35D3B3', '#d7d650', '#624CDA', '#8EDE16', '#FC58A5', '#D98282', '#BD39BD', '#5DEB52', '#FFE926']
  }),
  getters: {
    classcolorscale(state) {
      return (id) => scaleOrdinal().domain(Array.from(Array(state.labelnames.length).keys())).range(state.colors)(id);
    },
    acclinedata(state) {
      return [{
        name: "acc",
        data: state.acc.map((iteracc, i) => {
          return [i, iteracc]
        })
      }]
    },
    classmap0(state) {
      const labelnames = state.labelnames;
      const num = labelnames.length;
      const labeleddata = state.labeleddata;
      let classmap0 = new Array(num).fill(0);
      for (const d of labeleddata) {
        if (d !== -1) {
          classmap0[d] += 1
        }
      }
      return {
        'num': classmap0.reduce(function (pv, cv) {
          return pv + cv;
        }, 0),
        'data': classmap0.map((d, i) => {
          return {
            "x": labelnames[i],
            "y": d,
            "fillColor": state.colors[i]
          }
        })
      };
    },
    classmap1(state) {
      const labelnames = state.labelnames;
      const num = labelnames.length;
      const newlabelledlabels = state.newlabelledlabels;
      let classmap1 = new Array(num).fill(0);
      for (const d of newlabelledlabels) {
        if (d !== -1) {
          classmap1[d] += 1
        }
      }
      return {
        'num': classmap1.reduce(function (pv, cv) {
          return pv + cv;
        }, 0),
        'data': classmap1.map((d, i) => {
          return {
            "x": labelnames[i],
            "y": d,
            "fillColor": '#444444'
          }
        })
      };
    },
    labelledstat(state) {
      return [{
          name: 'labeled',
          data: state.classmap0.data
        },
        {
          name: 'newly labeled',
          data: state.classmap1.data
        }
      ]
    },
    labelpercentage(state) {
      return [{
          name: 'labeled',
          data: [{
            'x': 'labeled',
            'y': state.classmap0.num,
            'fillColor': '#222222'
          }]
        },
        {
          name: 'new labeled',
          data: [{
            'x': 'new labeled',
            'y': state.classmap1.num,
            'fillColor': '#444444'
          }]
        },
        {
          name: 'unlabeled',
          data: [{
            'x': 'unlabeled',
            'y': state.datacount - state.classmap0.num - state.classmap1.num,
            'fillColor': '#bbbbbb'
          }]
        }
      ]
    }
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    updateselectedindices(indices) {
      if (this.selectionmode === 'new') {
        this.selectedindices = indices;
      } else if (this.selectionmode === 'union') {
        this.selectedindices = [...new Set([...this.selectedindices, ...indices])]
      } else if (this.selectionmode === 'intersection') {
        this.selectedindices = this.selectedindices.filter(x => indices.includes(x))
      } else {
        console.log('selection error')
      }
      console.log(this.selectedindices.map(i => this.prediction_probs[i]));
      this.getImages(this.selectedindices);
    },
    changeselectionmode(mode) {
      this.selectionmode = mode;
    },
    async initialAL(setting) {
      try {
        console.log(setting)
        api.initialApp(setting).then(response => {
          this.datatype = response.datatype;
          this.labelnames = response.labelnames;
          this.ylabel = response.ylabel;
          this.labeleddata = response.labeleddata;
          this.datacount = response.labeleddata.length;
          this.newlabelindicearr = new Array(this.datacount).fill(0);
          this.newlabelledlabels = new Array(this.datacount).fill(-1);
          this.acc = [response.acc];
          this.embedding = response.embedding;
          this.predictions = response.predictions;
          this.allprobs = response.allprobs;
          this.prediction_probs = response.prediction_probs;
          this.imagepaths = [];
        })
        // console.log(await api.initialApp(setting))
      } catch (error) {
        console.log('ServerError', await error.response.json())
        return error;
      }
    },
    async itertrain() {
      try {
        let count = this.datacount;
        let indexarr = [];
        let labelarr = [];
        let label;
        for (let i = 0; i < count; i++) {
          label = this.newlabelledlabels[i];
          if (label != -1) {
            indexarr.push(i);
            labelarr.push(label)
            this.labeleddata[i] = label;
          }
          this.newlabelledlabels[i] = -1;
        }
        api.iterTraining(indexarr, labelarr).then(response => {
          this.acc.push(response.acc);
          this.predictions = response.predictions;
          this.allprobs = response.allprobs;
          this.prediction_probs = response.prediction_probs;
          this.labeltime = 0;
        });
      } catch (error) {
        console.log('ServerError', await error.response.json())
        return error;
      }
    },
    async getImages(indices) {
      if (indices.length === 0) {
        this.imagepaths = [];
        return;
      }
      try {
        this.imagepaths = await api.getImagesData(indices);
      } catch (error) {
        console.log('ServerError', await error.response.json())
        return error;
      }
    },
    async labeldata(indices, label) {
      let len = indices.length;
      for (let i = 0; i < len; i++) {
        this.newlabelledlabels[indices[i]] = label;
      }
      this.labeltime++;
    },
    async getcandidate(strategyname) {
      try {
        this.suggestedindices = await api.getCandidates(strategyname);
      } catch (error) {
        console.log('ServerError', await error.response.json())
        return error;
      }
    },
  },
})