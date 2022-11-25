import { mande } from 'mande'

const baseURL = process.env.VUE_APP_ROOT_API
console.log(baseURL)
const ALsetting = mande(baseURL)


/**
 * @description: load initial data after initializing AL setting
 * @param {*} setting {dataset:String,initialN:Number,model:String}
 * @return {*}
 */
export const initialApp = (setting) => ALsetting.get(`ALsetting/${setting.dataset}/${setting.initialN}/${setting.model}`);

export const iterTraining = (indexarr,labelarr) => ALsetting.post('itertraining',{indexarr,labelarr});

export const getImagesData = (indices) => ALsetting.post('images',{indices});

export const getCandidates = (strategy) => ALsetting.get(`candidates/${strategy}`);

// export const setStrategy = (strategy) => ALsetting.post('setstrategy',{strategy});