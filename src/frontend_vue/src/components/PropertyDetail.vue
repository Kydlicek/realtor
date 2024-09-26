<template>
  <div class="property-detail box">
    <!-- Main Image with Thumbnails -->
    <div class="image-container">
      <div class="columns is-vcentered is-gapless">
        <!-- Main Image (large) -->
        <div class="column is-three-fifths">
          <figure class="image main-image">
            <img :src="property.images[currentImageIndex]" alt="Property Image" />
            <button class="nav-button left-button" @click="prevImage">
              <i class="fas fa-chevron-left"></i>
            </button>
            <button class="nav-button right-button" @click="nextImage">
              <i class="fas fa-chevron-right"></i>
            </button>
          </figure>
        </div>

        <!-- Thumbnails (two stacked vertically) -->
        <div class="column is-two-fifths">
          <div class="columns is-multiline is-gapless">
            <div class="column is-full">
              <figure class="image is-4by3" @click="currentImageIndex = 0">
                <img :src="property.images[0]" alt="Thumbnail Image 1">
              </figure>
            </div>
            <div class="column is-full">
              <figure class="image is-4by3" @click="currentImageIndex = 1">
                <img :src="property.images[1]" alt="Thumbnail Image 2">
              </figure>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs and Content below -->
    <div class="tabs is-medium">
      <ul>
        <li :class="{ 'is-active': activeTab === 'basic' }">
          <a @click="activeTab = 'basic'">Basic Information</a>
        </li>
        <li :class="{ 'is-active': activeTab === 'finances' }">
          <a @click="activeTab = 'finances'">Finances</a>
        </li>
        <li :class="{ 'is-active': activeTab === 'contact' }">
          <a @click="activeTab = 'contact'">Contact</a>
        </li>
      </ul>
    </div>

    <!-- Basic Information -->
    <div class="basic-info" v-if="activeTab === 'basic'">
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
      activeTab: 'basic' // To manage tabs
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
.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}

.columns.is-gapless {
  margin-left: 0;
  margin-right: 0;
}

.column {
  padding: 0 !important;
}

figure.image {
  margin: 0;
}

.main-image img, 
figure img {
  object-fit: cover;
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
</style>
