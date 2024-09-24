<script setup>
import NavBar from './components/NavBar.vue'
</script>
<template>
  <section class="hero is-primary is-fullheight-with-navbar">
    <!-- Hero head: will stick at the top -->
    <div class="hero-head has-background-primary-40">
      <NavBar />
    </div>

    <!-- Hero content: will be in the middle -->
    <div class="hero-body has-background-white	p-0">
      <RouterView />

    </div>

    <!-- Hero footer: will stick at the bottom -->

  </section>
</template>

<style>
#app {
  overflow-x: hidden;
}
</style>