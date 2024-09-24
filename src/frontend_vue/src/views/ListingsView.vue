<script setup>
import { ref, onMounted } from 'vue';
import PropertiesGrid from '../components/PropertiesGrid.vue';
import Map from '../components/PropertyMap.vue';
import PropFilterDropDown from '../components/PropFilterDropDown.vue';
import PropertyDetail from '../components/PropertyDetail.vue';
import axios from 'axios';


// Reactive variable for current filter
let current_filter = ref('nejnovější');

// Get screen width
const screenWidth = window.innerWidth;

// Define props
const props = defineProps({
  query: String,
});

// Reactive variable for query
const query = ref(props.query);
const properties = ref([]); // To store fetched properties

// Define the function to fetch properties based on the query
const QueryProps = async () => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_FRONTEND_API}/search`, {
      query: query.value,
    });

    properties.value = response.data.properties; // Store fetched properties
    console.log('Fetched properties:', properties.value); // Log fetched properties
  } catch (error) {
    console.error('Error searching properties:', error);
  }
};




// Run QueryProps function when the component is mounted
onMounted(() => {
  QueryProps();
});
const selectedProperty = ref(null)

function update_filter(val) {
  current_filter.value = val;
}

function handlePropertySelected(property) {
  selectedProperty.value = property;
}

function deselectProperty() {
  selectedProperty.value = null;
}
</script>

<template>
  <div class="columns max_columns p-0 m-0">
    <div class="map column is-two-fifths p-0 m-0" :class="{ 'small-width': screenWidth < 769 }">
      <Map :properties="properties" :selectedProperty="selectedProperty" @property-selected="handlePropertySelected" />
      <PropFilterDropDown class="search-box" />
    </div>

    <div v-if="selectedProperty" class="listings column pl-0 pr-0 pt-0"
      :class="{ 'small-width-listings': screenWidth < 769 }">
      <PropertyDetail :property="selectedProperty" @deselect-property="deselectProperty" />
    </div>

    <div v-else class="listings column pl-1 pr-0 pt-2" :class="{ 'small-width-listings': screenWidth < 769 }">
      <p class="has-text-weight-semibold ml-2">Nalezené vysledky: 1 v oblasti Praha 4</p>
      <div class="dropdown is-hoverable">
        <div class="dropdown-trigger">
          <button class="button is-ghost pl-2 pt-1" aria-haspopup="true" aria-controls="dropdown-menu4">
            <span>řadit: {{ current_filter }}</span>
            <span class="icon is-small">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content">
            <a class="dropdown-item" @click="update_filter('nejlevnější')">nejlevnější</a>
            <a class="dropdown-item" @click="update_filter('nejdražší')">nejdražší</a>
            <a class="dropdown-item" @click="update_filter('nejnovější')">nejnovější</a>
            <a class="dropdown-item" @click="update_filter('relevance')">relevance</a>
          </div>
        </div>
      </div>

      <PropertiesGrid :properties="properties" @property-selected="handlePropertySelected" class="prop-grid m-0" />

    </div>
  </div>
</template>



<style scoped>
.max_columns {
  height: 100vh;
}

.search-box {
  position: absolute;
  top: 5%;
  left: 10%;
  z-index: 2;

  overflow: auto;
}

.prop-grid {
  height: 100%;
  overflow-y: scroll;
}


.map {
  height: 94vh;
  position: relative;
}

.small-width {
  height: 40vh;
  position: relative;
}

.small-width-listings {
  height: 48vh;
}

.columns {
  width: 100vw;

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