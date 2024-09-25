<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const searchQuery = ref('')
const router = useRouter()
const handleSearch = async () => {
  router.push({
    name: 'listings',
    params: { query: searchQuery.value }
  })
}
</script>

<template>
  <div class="container is-centered">
    <div class="columns">
      <div class="column"></div>

      <div class="column is-centered">
        <div class="container">
          <p class="title is-block">Realtor App</p>
          <p class="subtitle is-block">Vyhledejte pronájem</p>

          <!-- Search Input -->
          <div class="field">
            <div class="control">
              <input
                class="input mt-1"
                type="text"
                v-model="searchQuery"
                placeholder="Enter house type, size, city, budget"
              />
            </div>
          </div>

          <!-- Search Button -->
          <button class="button mt-2" @click="handleSearch">Vyhledat</button>
        </div>
      </div>

      <div class="column"></div>
    </div>
  </div>
</template>

<style scoped>
/* Add any custom styles here */
.container {
  max-width: 600px;
  margin: 0 auto;
  padding-top: 50px;
}

.title {
  text-align: center;
}

.subtitle {
  text-align: center;
}

.input {
  width: 100%;
}

.button {
  width: 100%;
  background-color: #3273dc;
  color: white;
}
</style>
