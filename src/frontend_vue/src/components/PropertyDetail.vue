<template>
  <div class="property-detail box">
    <!-- Return to Grid Button -->
    <div class="return-button">
      <button class="button is-link" @click="$emit('deselect-property')">Return to Grid</button>
    </div>

    <!-- Main Image with Navigation -->
    <div class="main-image-container">
      <figure class="image is-16by9 main-image">
        <img :src="property.images[currentImageIndex]" alt="Property Image" />
        <button class="nav-button left-button" @click="prevImage">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button class="nav-button right-button" @click="nextImage">
          <i class="fas fa-chevron-right"></i>
        </button>
      </figure>
    </div>

    <!-- Thumbnails -->
    <div class="thumbnails">
      <div class="columns is-mobile is-multiline">
        <div class="column is-one-fifth" v-for="(image, index) in property.images" :key="index">
          <figure class="image is-4by3">
            <img :src="image" :alt="'Thumbnail ' + (index + 1)" @click="currentImageIndex = index" />
          </figure>
        </div>
      </div>
    </div>
    <div class="flex overflow-x-auto overflow-y-hidden border-b border-gray-200 whitespace-nowrap dark:border-gray-700">
    <button  @click="activeTab = 'basic'" class="inline-flex items-center h-10 px-4 -mb-px text-sm text-center text-blue-600 bg-transparent border-b-2 border-blue-500 sm:text-base dark:border-blue-400 dark:text-blue-300 whitespace-nowrap focus:outline-none">
        Basic Information
    </button>

    <button   @click="activeTab = 'finances'" class="inline-flex items-center h-10 px-4 -mb-px text-sm text-center text-gray-700 bg-transparent border-b-2 border-transparent sm:text-base dark:text-white whitespace-nowrap cursor-base focus:outline-none hover:border-gray-400">
        Finances
    </button>

    <button  @click="activeTab = 'contact'" class="inline-flex items-center h-10 px-4 -mb-px text-sm text-center text-gray-700 bg-transparent border-b-2 border-transparent sm:text-base dark:text-white whitespace-nowrap cursor-base focus:outline-none hover:border-gray-400">
        Contact
    </button>
</div>
  
    <!-- Basic Information -->
    <div  class="basic-info" v-if="activeTab === 'basic'">
      <h2 class="title is-4">Basic Information</h2>
      <div class="columns">
        <div class="column">
          <p><strong>Type:</strong> {{ property.prop_type }}</p>
          <p><strong>Rooms:</strong> {{ property.prop_size_kk }}+kk</p>
          <p><strong>Size:</strong> {{ property.prop_size_m2 }} m²</p>
        </div>
        <div class="column">
          <p><strong>Energy Class:</strong> {{ property.energy_class }}</p>
          <p><strong>Floor:</strong> {{ property.floor }}</p>
          <p><strong>Parking:</strong> {{ property.parking }}</p>
          <p><strong>Elevator:</strong> {{ property.elevator ? 'Yes' : 'No' }}</p>
        </div>
      </div>
    </div>

    <!-- Features -->
    <div class="features">
      <h2 class="title is-4">Features</h2>
      <ul>
        <li v-for="(feature, index) in property.features" :key="index">{{ feature }}</li>
      </ul>
    </div>

    <!-- Neighborhood -->
    <div class="neighborhood">
      <h2 class="title is-4">Neighborhood</h2>
      <p>{{ property.neighborhood_description }}</p>
      <h3 class="title is-5">Nearby Amenities</h3>
      <ul>
        <li v-for="(amenity, index) in property.amenities" :key="index">
          {{ amenity }}
        </li>
      </ul>
      <h3 class="title is-5">Transport Options</h3>
      <ul>
        <li v-for="(transport, index) in property.transport" :key="index">
          {{ transport }}
        </li>
      </ul>
    </div>

    <!-- Average Rent -->
    <div class="average-rent">
      <h2 class="title is-4">Average Rent in Neighborhood</h2>
      <p>{{ property.average_rent }} Kč/m</p>
    </div>

    <!-- Pricing Details -->
    <div class="pricing-details" v-if="activeTab === 'finances'">
      <h2 class="title is-4">Pricing Details</h2>
      <h3 class="title is-5">One-time Payments</h3>
      <ul>
        <li>{{ property.security_deposit }}</li>
        <li>{{ property.agency_fee }}</li>
      </ul>
      <h3 class="title is-5">Monthly Payments</h3>
      <ul>
        <li>{{ property.rent }}</li>
        <li>{{ property.utilities }}</li>
      </ul>
    </div>

    <!-- Contact Information -->
    <div class="contact-info" v-if="activeTab === 'contact'">
      <h2 class="title is-4">Contact Information</h2>
      <p><strong>Agent:</strong> {{"Jordan Pepe" }}</p>
      <p><strong>Phone:</strong> {{"420 74502345"}}</p>
      <p><strong>Email:</strong> {{"dkasdssa@sezban.cz" }}</p>
    </div>
  </div>

</template>

<script>
export default {
  name: 'PropertyDetail',
  props: {
    property: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      currentImageIndex: 0,
      activeTab: 'basic' // Add this to manage active tabs
    }
  },
  methods: {
    nextImage() {
      if (this.currentImageIndex < this.property.images.length - 1) {
        this.currentImageIndex++
      } else {
        this.currentImageIndex = 0
      }
    },
    prevImage() {
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--
      } else {
        this.currentImageIndex = this.property.images.length - 1
      }
    }
  }
}
</script>

<style scoped>
.property-detail {
  padding: 20px;
  max-height: 100vh;
  overflow-y: auto;
}

.return-button {
  text-align: right;
  margin-bottom: 20px;
}

.main-image-container {
  position: relative;
  margin-bottom: 20px;
}

.main-image img {
  width: 100%;
  height: auto;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 1.5em;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s;
}

.main-image-container:hover .nav-button {
  opacity: 1;
}

.left-button {
  left: 10px;
}

.right-button {
  right: 10px;
}

.thumbnails {
  margin-bottom: 20px;
}

.thumbnails .image {
  cursor: pointer;
}

.basic-info,
.features,
.neighborhood,
.average-rent,
.pricing-details,
.contact-info {
  margin-top: 20px;
}

.features ul,
.neighborhood ul,
.pricing-details ul {
  list-style-type: disc;
  padding-left: 20px;
}
</style>
