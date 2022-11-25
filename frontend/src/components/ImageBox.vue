<template>
<div>
    <span class="close" @click="removeImg(path.index)">&times;</span>
    <q-img  :src="getImgUrl(path.path)"
        spinner-color="red" loading="lazy"
        style="height: 50px; max-width: 50px">
        </q-img>
</div>
</template>

<script>
export default {
    props:{
        path: Object,
        removeImg: Function,
        getImgUrl: Function
    }
}
</script>

<style lang="scss" scoped>

.img-wrap .close {
    position: absolute;
    top: 2px;
    right: 2px;
    z-index: 100;
    background-color: #FFF;
    padding: 5px 2px 2px;
    color: #000;
    font-weight: bold;
    cursor: pointer;
    opacity: .2;
    text-align: center;
    font-size: 22px;
    line-height: 10px;
    border-radius: 50%;
}
.img-wrap:hover .close {
    opacity: 1;
}
</style>