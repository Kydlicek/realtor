<template>
  <div>
    <div v-if="!selectedProperty" class="grid-container grid is-gap-1 is-col-min-12">
      <div v-for="property in properties" :key="property.id" class="cell" @click="() => selectProperty(property)">
        <PropertyCard :property="property" :isSelected="selectedProperty === property" />
      </div>
      <div class="filler"></div>
      <div class="filler"></div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import PropertyCard from './PropertyCard.vue'
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  properties: Array
})

const emit = defineEmits(['property-selected'])

const selectedProperty = ref(null)

const selectProperty = (property) => {
  selectedProperty.value = property
  emit('property-selected', property)
}

const deselectProperty = () => {
  selectedProperty.value = null
}
</script>

<style scoped>
.filler {
  position: static;
  height: 100px;
  width: 200px;
}

.grid-container {
  height: 100%;
  position: relative
}

.selected-property-container {
  padding: 20px;
}

.detailed-view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detailed-view-body {
  margin-top: 20px;
}

.detailed-view-body img {
  max-width: 100%;
  height: auto;
}
</style>
