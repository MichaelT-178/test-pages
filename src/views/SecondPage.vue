<template>
  <p class="title">Second Page</p>
  <LinkBtn
    :path="'/'"
    :buttonText="'Go to Home page'">
  </LinkBtn>
</template>


<script setup>
import LinkBtn from '../components/RouterBtn.vue';
</script>


<style scoped>

.title {
  color: purple;
  font-family: Arial, sans-serif;
  padding-left: 20px;
}

</style>