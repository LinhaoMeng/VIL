<template>
    <div id="labelbuttons">
        <q-btn-toggle
            v-model="labelnumber"
            toggle-color="primary"
            :options="labellist"
            class="classlabelbtn"
        />
        <!-- <q-btn v-for="i in [...Array(10).keys()]" color="white" text-color="black" :key="i" :label="i" class="classlabelbtn"/> -->
        <q-btn color="primary" text-color="white" label="OK" @click="labeldatafn(labelnumber)"/>
    </div>
</template>

<script>

export default {
    name: "LabelOperation",
    data(){
        return{
            labelnumber: 1,
            labellist: Array(10).fill().map((_,i)=>{
                    return {'label': i, 'value': i}
                })
        }
    },
    props:{
        labeldatafn:Function
    },
}
</script>

<style lang="scss" scoped>
.classlabelbtn{
    margin: 1px;
    padding: 1px;
}
</style>